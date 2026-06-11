import os

from rest_framework import serializers

from project.serializers import PreviewProjectSerializer, PreviewSectionProjectSerializer, SectionProjectSerializer
from task.models import Task, UserToTask, SubtaskChecklist, ChecklistTask, TaskToSection, TaskCategory, CommentTask, \
    Notification, TaskAttachment, CommentTaskAttachment, TaskHistory
from task.service import get_responsible_task, get_collaborator_task, get_observer_task
from user.serializers import PreviewUserSerializer


def fix_mojibake(value):
    if not isinstance(value, str) or not value:
        return value

    def restore_source_bytes(text):
        restored = bytearray()
        for char in text:
            code = ord(char)
            if code <= 255:
                restored.append(code)
                continue
            try:
                restored.extend(char.encode('cp1252'))
            except UnicodeEncodeError:
                return None
        return bytes(restored)

    candidates = [value]
    source_bytes = restore_source_bytes(value)
    if source_bytes is not None:
        for target_encoding in ['utf-8', 'cp1251']:
            try:
                candidates.append(source_bytes.decode(target_encoding))
            except UnicodeDecodeError:
                pass

    for source_encoding in ['latin1', 'cp1251', 'cp1252']:
        for target_encoding in ['utf-8', 'cp1251']:
            try:
                candidates.append(value.encode(source_encoding).decode(target_encoding))
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass

    def score(text):
        cyrillic_count = sum('А' <= char <= 'я' or char == 'ё' or char == 'Ё' for char in text)
        mojibake_count = sum(char in 'ÐÑÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß�' or 128 <= ord(char) <= 159 for char in text)
        marker_count = text.count('Р') + text.count('С')
        if marker_count > max(2, len(text) // 8):
            mojibake_count += marker_count * 2
        return cyrillic_count - mojibake_count

    return max(candidates, key=score)


class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = ['id', 'project', 'name', 'color', 'created_at']
        read_only_fields = ['project', 'created_at']


# ========================
#    Задача в списке
# ========================
class TaskSerializer(serializers.ModelSerializer):
    director = PreviewUserSerializer()
    responsible = serializers.SerializerMethodField()
    project = PreviewProjectSerializer()
    category = TaskCategorySerializer(read_only=True)
    section = serializers.SerializerMethodField()
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=TaskCategory.objects.all(),
        source='category',
        required=False,
        allow_null=True,
        write_only=True
    )

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'deadline', 'completed_at', 'code', 'director', 'responsible', 'project', 'category', 'category_id', 'section']

    @staticmethod
    def get_responsible(instance):
        user_to_task = UserToTask.objects.filter(task=instance, level=get_responsible_task()).first()
        if user_to_task is None:
            return None
        return PreviewUserSerializer(user_to_task.user).data

    def validate_category_id(self, value):
        if value is None:
            return value
        task = self.instance
        if task is not None and value.project_id != task.project_id:
            raise serializers.ValidationError('Категория должна принадлежать проекту задачи')
        return value

    @staticmethod
    def get_section(instance):
        task_to_section = TaskToSection.objects.filter(task=instance).select_related('section_project').first()
        if task_to_section is None:
            return None
        return PreviewSectionProjectSerializer(task_to_section.section_project).data


# ========================
#    Детальная Задача
# ========================
class DetailTaskSerializer(serializers.ModelSerializer):
    director = PreviewUserSerializer()
    responsible = serializers.SerializerMethodField()
    collaborators = serializers.SerializerMethodField()
    observers = serializers.SerializerMethodField()
    project = PreviewProjectSerializer()
    category = TaskCategorySerializer(read_only=True)
    section = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'

    @staticmethod
    def get_responsible(instance):
        user_to_task = UserToTask.objects.filter(task=instance, level=get_responsible_task()).first()
        if user_to_task is None:
            return None
        return PreviewUserSerializer(user_to_task.user).data

    @staticmethod
    def get_collaborators(instance):
        user_to_task = UserToTask.objects.filter(task=instance, level=get_collaborator_task())
        if not user_to_task.exists():
            return []
        users = [user.user for user in user_to_task]
        return PreviewUserSerializer(users, many=True).data

    @staticmethod
    def get_observers(instance):
        user_to_task = UserToTask.objects.filter(task=instance, level=get_observer_task())
        if not user_to_task.exists():
            return []
        users = [user.user for user in user_to_task]
        return PreviewUserSerializer(users, many=True).data

    @staticmethod
    def get_section(instance):
        task_to_section = TaskToSection.objects.filter(task=instance).select_related('section_project').first()
        if task_to_section is None:
            return None
        return PreviewSectionProjectSerializer(task_to_section.section_project).data

    def get_attachments(self, instance):
        attachments = TaskAttachment.objects.filter(task=instance).select_related('user', 'user__user')
        return TaskAttachmentSerializer(attachments, many=True, context=self.context).data


class AttachmentFileUrlMixin:
    download_path_template = ''

    def get_file_url(self, instance):
        if not instance.file:
            return ''

        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(instance.file.url)
        return instance.file.url

    @staticmethod
    def get_stored_name(instance):
        if not instance.file:
            return ''
        return os.path.basename(instance.file.name)

    @staticmethod
    def get_display_name(instance):
        return instance.name

    def get_download_url(self, instance):
        if not self.download_path_template:
            return self.get_file_url(instance)

        url = self.download_path_template.format(pk=instance.pk)
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(url)
        return url


class TaskAttachmentSerializer(AttachmentFileUrlMixin, serializers.ModelSerializer):
    download_path_template = '/api/task/attachment/{pk}/download/'

    user = PreviewUserSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()
    stored_name = serializers.SerializerMethodField()

    class Meta:
        model = TaskAttachment
        fields = ['id', 'user', 'name', 'display_name', 'stored_name', 'size', 'content_type', 'file', 'file_url',
                  'download_url', 'created_at']
        read_only_fields = fields


class CommentTaskAttachmentSerializer(AttachmentFileUrlMixin, serializers.ModelSerializer):
    download_path_template = '/api/task/comment-attachment/{pk}/download/'

    file_url = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()
    stored_name = serializers.SerializerMethodField()

    class Meta:
        model = CommentTaskAttachment
        fields = ['id', 'name', 'display_name', 'stored_name', 'size', 'content_type', 'file', 'file_url',
                  'download_url', 'created_at']
        read_only_fields = fields


class CommentTaskSerializer(serializers.ModelSerializer):
    item_type = serializers.SerializerMethodField()
    user = PreviewUserSerializer(source='user.user', read_only=True)
    attachments = CommentTaskAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = CommentTask
        fields = ['item_type', 'id', 'user', 'text', 'attachments', 'created_at']

    @staticmethod
    def get_item_type(instance):
        return 'comment'


class TaskHistorySerializer(serializers.ModelSerializer):
    item_type = serializers.SerializerMethodField()
    user = PreviewUserSerializer(source='actor', read_only=True)

    class Meta:
        model = TaskHistory
        fields = ['item_type', 'id', 'user', 'type', 'title', 'text', 'field', 'old_value', 'new_value', 'created_at']

    @staticmethod
    def get_item_type(instance):
        return 'history'


class NotificationSerializer(serializers.ModelSerializer):
    actor = PreviewUserSerializer(read_only=True)
    project = PreviewProjectSerializer(read_only=True)
    task = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'type', 'title', 'text', 'is_read', 'created_at', 'actor', 'project', 'task']

    @staticmethod
    def get_task(instance):
        if instance.task is None:
            return None
        return {
            'id': instance.task.id,
            'name': fix_mojibake(instance.task.name),
            'code': instance.task.code,
            'project': instance.task.project_id,
        }

    @staticmethod
    def get_title(instance):
        return fix_mojibake(instance.title)

    @staticmethod
    def get_text(instance):
        return fix_mojibake(instance.text)


# ========================
#   Подзадачи у чеклиста
# ========================
class SubtaskChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubtaskChecklist
        fields = ['id', 'name', 'position', 'completed_at']
        extra_kwargs = {
            'name': {'required': False},
        }


# ========================
#        Чеклисты
# ========================
class ChecklistTaskSerializer(serializers.ModelSerializer):
    infoCompletedSubtask = serializers.SerializerMethodField()
    subtasks = serializers.SerializerMethodField()

    class Meta:
        model = ChecklistTask
        fields = ['id', 'name', 'position', 'infoCompletedSubtask', 'subtasks']

    @staticmethod
    def get_infoCompletedSubtask(instance):
        all_subtask = SubtaskChecklist.objects.filter(checklist=instance).order_by('position')
        count_completed_subtask = 0
        completed_subtask = []
        for it in all_subtask:
            is_none = it.completed_at is not None
            completed_subtask.append(is_none)
            count_completed_subtask += is_none
        return {
            'all': len(all_subtask),
            'completed': count_completed_subtask,
            'completedList': completed_subtask,
        }

    @staticmethod
    def get_subtasks(instance):
        all_subtask = SubtaskChecklist.objects.filter(checklist=instance).order_by('position', 'completed_at')
        return SubtaskChecklistSerializer(all_subtask, many=True).data


#  Чек-лист основные данные
class ChecklistTaskPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistTask
        fields = ['id', 'name', 'position']
        extra_kwargs = {
            'name': {'required': False},
        }


class TaskToSectionSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    section_project = SectionProjectSerializer()

    class Meta:
        model = TaskToSection
        fields = '__all__'
