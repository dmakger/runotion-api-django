from rest_framework import serializers

from project.serializers import PreviewProjectSerializer, SectionProjectSerializer
from task.models import Task, UserToTask, SubtaskChecklist, ChecklistTask, TaskToSection
from task.service import get_responsible_task, get_collaborator_task, get_observer_task
from user.serializers import PreviewUserSerializer


# ========================
#    Задача в списке
# ========================
class TaskSerializer(serializers.ModelSerializer):
    director = PreviewUserSerializer()
    responsible = serializers.SerializerMethodField()
    project = PreviewProjectSerializer()

    class Meta:
        model = Task
        fields = ['id', 'name', 'deadline', 'code', 'director', 'responsible', 'project']

    @staticmethod
    def get_responsible(instance):
        user_to_task = UserToTask.objects.filter(task=instance, level=get_responsible_task())
        if len(user_to_task) == 0:
            return None
        return PreviewUserSerializer(user_to_task[0].user).data


# ========================
#    Детальная Задача
# ========================
class DetailTaskSerializer(serializers.ModelSerializer):
    director = PreviewUserSerializer()
    responsible = serializers.SerializerMethodField()
    collaborators = serializers.SerializerMethodField()
    observers = serializers.SerializerMethodField()
    project = PreviewProjectSerializer()

    class Meta:
        model = Task
        fields = '__all__'

    @staticmethod
    def get_responsible(instance):
        user_to_task = UserToTask.objects.filter(task=instance, level=get_responsible_task())
        if len(user_to_task) == 0:
            return None
        return PreviewUserSerializer(user_to_task[0].user).data

    @staticmethod
    def get_collaborators(instance):
        user_to_task = UserToTask.objects.filter(task=instance, level=get_collaborator_task())
        if len(user_to_task) == 0:
            return []
        users = [user.user for user in user_to_task]
        return PreviewUserSerializer(users, many=True).data

    @staticmethod
    def get_observers(instance):
        user_to_task = UserToTask.objects.filter(task=instance, level=get_observer_task())
        if len(user_to_task) == 0:
            return []
        users = [user.user for user in user_to_task]
        return PreviewUserSerializer(users, many=True).data


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
