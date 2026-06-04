from django.db.models import Subquery, OuterRef, Q
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import DestroyAPIView, UpdateAPIView, get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from project.models import UserToProject, Project, SectionProject
from service.error.error_view import TaskError, ChecklistError, SubtaskChecklistError
from service.filter.task import TaskFilter
from service.order_by.order_by import order_by
from service.pagination import Pagination
from service.task import get_new_code_task_by_project, get_new_position_checklist_by_user_to_task, \
    get_new_position_subtask_checklist_by_user_to_task
from service.validator import Validator
from task.models import Task, ChecklistTask, UserToTask, SubtaskChecklist, TaskToSection, TaskCategory, CommentTask, \
    Notification, TaskAttachment, CommentTaskAttachment
from task.notifications import notify_task_participants, send_notification
from task.serializers import TaskSerializer, DetailTaskSerializer, ChecklistTaskSerializer, SubtaskChecklistSerializer, \
    ChecklistTaskPreviewSerializer, TaskCategorySerializer, CommentTaskSerializer, NotificationSerializer, \
    TaskAttachmentSerializer
from task.service import get_collaborator_task, get_observer_task, get_responsible_task
from user.models import UserProfile


def can_edit_task(task, user):
    if task.director.user == user:
        return True

    return UserToTask.objects.filter(
        task=task,
        user__user=user,
        level__in=[get_responsible_task(), get_collaborator_task()],
    ).exists()


def can_view_task(task, user):
    if task.director.user == user:
        return True

    if task.project.admin.user == user:
        return True

    return UserToTask.objects.filter(task=task, user__user=user).exists() or UserToProject.objects.filter(
        project=task.project,
        user__user=user,
    ).exists()


def can_comment_task(task, user):
    return can_view_task(task, user)


def create_attachment(instance, uploaded_file, user=None):
    data = {
        'file': uploaded_file,
        'name': uploaded_file.name,
        'size': uploaded_file.size or 0,
        'content_type': getattr(uploaded_file, 'content_type', '') or '',
    }

    if isinstance(instance, Task):
        return TaskAttachment.objects.create(task=instance, user=user, **data)
    return CommentTaskAttachment.objects.create(comment=instance, **data)


# ============================
#   Получение всех задач
# ============================
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    error = TaskError()
    filter = TaskFilter

    @staticmethod
    def apply_search(queryset, search):
        if not search:
            return queryset

        return queryset.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search) |
            Q(project__name__icontains=search) |
            Q(project__code__icontains=search) |
            Q(description__icontains=search) |
            Q(director__name__icontains=search) |
            Q(director__user__username__icontains=search) |
            Q(category__name__icontains=search) |
            Q(tasktosection__section_project__name__icontains=search) |
            Q(usertotask__user__name__icontains=search) |
            Q(usertotask__user__user__username__icontains=search) |
            Q(usertotask__level__name__icontains=search)
        ).distinct()

    @action(methods=['post'], detail=False)
    def get_tasks(self, request):
        filter_data = self.filter(request)
        user = filter_data.result.pop('user', None)
        search = request.data.get('search') or request.query_params.get('search')

        if user is not None:
            user_tasks = self.queryset.filter(usertotask__user__user=user, **filter_data.result)
            director_tasks = Task.objects.filter(director__user=user, **filter_data.result)
            user_tasks = self.apply_search(user_tasks, search)
            director_tasks = self.apply_search(director_tasks, search)

            if not request.data.get('has_section', True):
                user_tasks = user_tasks.exclude(
                    id__in=Subquery(TaskToSection.objects.filter(task_id=OuterRef('pk')).values('task_id'))
                )
                director_tasks = director_tasks.exclude(
                    id__in=Subquery(TaskToSection.objects.filter(task_id=OuterRef('pk')).values('task_id'))
                )

            all_tasks = user_tasks.union(director_tasks).order_by(order_by(request))
        else:
            user_projects = Project.objects.filter(
                Q(admin__user=request.user) | Q(usertoproject__user__user=request.user)
            ).distinct()
            all_tasks = self.queryset.filter(project__in=user_projects, **filter_data.result)
            all_tasks = self.apply_search(all_tasks, search)

            if not request.data.get('has_section', True):
                all_tasks = all_tasks.exclude(
                    id__in=Subquery(TaskToSection.objects.filter(task_id=OuterRef('pk')).values('task_id'))
                )

            all_tasks = all_tasks.order_by(order_by(request))

        result = Pagination(request=request, queryset=all_tasks).get()
        result['results'] = self.serializer_class(result.get('results'), many=True).data
        return Response(result, status=status.HTTP_200_OK)

    # Создание задачи
    @action(methods=['post'], detail=False)
    def create_task(self, request):
        validator = Validator(request=request)
        if not validator.has_content(['project_id']):
            return self.error.is_not_content_form()
        name = request.data.get('name', 'Новая задача')
        project_id = request.data['project_id']

        current_user = UserProfile.objects.get(user=request.user)
        project = Project.objects.filter(pk=project_id).first()
        if project is None:
            return self.error.is_not_found()

        name = request.data.get('name')
        if name is None:
            name = f'Новая задача #{Task.objects.filter(project=project).count() + 1}'

        code = get_new_code_task_by_project(project)
        category = None
        category_id = request.data.get('category_id')
        if category_id is not None:
            category = get_object_or_404(TaskCategory, pk=category_id, project=project)

        task = Task.objects.create(name=name, code=code, director=current_user, project=project, category=category)

        section = None
        if request.data.get('section_id') is not None:
            section_id = request.data.get('section_id')
            section = get_object_or_404(SectionProject, pk=section_id)
        else:
            section = SectionProject.objects.filter(project=project).order_by('position', 'created_at').first()

        if section is not None:
            task_to_section = TaskToSection.objects.create(task=task, section_project=section)
            task_to_section.save()
            if section.is_final:
                task.completed_at = timezone.now()
                task.save(update_fields=['completed_at'])

        serializer = self.serializer_class(task, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskCategoryView(viewsets.ModelViewSet):
    serializer_class = TaskCategorySerializer
    queryset = TaskCategory.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            Q(project__admin__user=self.request.user) |
            Q(project__usertoproject__user__user=self.request.user) |
            Q(project__task__director__user=self.request.user) |
            Q(project__task__usertotask__user__user=self.request.user)
        ).distinct()

    def get_project(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        has_project_access = project.admin.user == request.user or UserToProject.objects.filter(
            user__user=request.user,
            project=project
        ).exists()
        has_task_access = Task.objects.filter(
            Q(director__user=request.user) | Q(usertotask__user__user=request.user),
            project=project
        ).exists()
        if not has_project_access and not has_task_access:
            return None
        return project

    @action(methods=['get'], detail=False)
    def get_categories(self, request, project_id):
        project = self.get_project(request, project_id)
        if project is None:
            return Response(status=status.HTTP_403_FORBIDDEN)

        search = request.GET.get('search')
        categories = self.get_queryset().filter(project=project).order_by('name')
        if search:
            categories = categories.filter(name__icontains=search)

        return Response(self.serializer_class(categories, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def create_category(self, request, project_id):
        project = self.get_project(request, project_id)
        if project is None:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.queryset.filter(project=project, name=serializer.validated_data['name']).exists():
            return Response({'name': ['Категория с таким названием уже существует']},
                            status=status.HTTP_400_BAD_REQUEST)
        category = serializer.save(project=project)
        return Response(self.serializer_class(category).data, status=status.HTTP_201_CREATED)


# ==============================
#   Детальная страница задачи
# ==============================-+
class DetailTaskView(viewsets.ModelViewSet):
    serializer_class = DetailTaskSerializer
    queryset = Task.objects.all()
    error = TaskError()
    permission_classes = [permissions.IsAuthenticated]

    # Получение данных о задаче
    @action(methods=['get'], detail=False)
    def get_detail_task(self, request, task_id):
        task = self.queryset.filter(pk=task_id).first()
        if task is None:
            self.error.is_not_found()

        if not can_view_task(task, request.user):
            self.error.forbidden()

        result = self.serializer_class(task, context={'request': request}).data
        return Response(result, status=status.HTTP_200_OK)


#  Обновление данных у задачи
class TaskUpdateAPIView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if not can_edit_task(task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        self.changed_fields = []
        for field in ['name', 'description', 'deadline', 'completed_at', 'category_id']:
            if field in request.data:
                model_field = 'category_id' if field == 'category_id' else field
                old_value = getattr(task, model_field)
                new_value = request.data.get(field)
                if str(old_value or '') != str(new_value or ''):
                    self.changed_fields.append(field)

        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        task = serializer.save()
        current_user = UserProfile.objects.get(user=self.request.user)
        if getattr(self, 'changed_fields', []):
            notify_task_participants(
                task=task,
                notification_type='task_changed',
                title=f'Изменена задача {task.code}',
                text=task.name,
                actor=current_user,
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get_level(level_name):
        if level_name == 'responsible':
            return get_responsible_task()
        if level_name == 'collaborator':
            return get_collaborator_task()
        if level_name == 'observer':
            return get_observer_task()
        return None

    @staticmethod
    def can_manage_task(task, user):
        return can_edit_task(task, user)

    @staticmethod
    def is_project_member(task, user_profile):
        if task.project.admin_id == user_profile.id:
            return True
        return UserToProject.objects.filter(project=task.project, user=user_profile).exists()

    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if not self.can_manage_task(task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        level = self.get_level(request.data.get('level'))
        if user_id is None or level is None:
            return Response({'detail': 'user_id and level are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(UserProfile, pk=user_id)
        if not self.is_project_member(task, user):
            return Response({'detail': 'User is not a project member'}, status=status.HTTP_400_BAD_REQUEST)

        if level == get_responsible_task():
            UserToTask.objects.filter(task=task, level=level).exclude(user=user).update(level=get_collaborator_task())

        current_user = UserProfile.objects.get(user=request.user)
        user_to_task = UserToTask.objects.filter(task=task, user=user).select_related('level').first()
        if user_to_task is None:
            UserToTask.objects.create(task=task, user=user, level=level)
            send_notification(
                user=user,
                notification_type='task_member_added',
                title=f'Вас добавили в задачу {task.code}',
                text=task.name,
                actor=current_user,
                project=task.project,
                task=task,
            )
        else:
            old_level = user_to_task.level
            user_to_task.level = level
            user_to_task.save(update_fields=['level'])
            if old_level_id := getattr(old_level, 'id', None):
                if old_level_id != level.id:
                    send_notification(
                        user=user,
                        notification_type='task_role_changed',
                        title=f'Изменена роль в задаче {task.code}',
                        text=f'{task.name}: {level.name}',
                        actor=current_user,
                        project=task.project,
                        task=task,
                    )

        return Response(DetailTaskSerializer(task, context={'request': request}).data, status=status.HTTP_200_OK)

    def delete(self, request, task_id, user_id=None):
        task = get_object_or_404(Task, pk=task_id)
        if not self.can_manage_task(task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        if user_id is None:
            return Response({'detail': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        user_to_task = UserToTask.objects.filter(task=task, user_id=user_id).select_related('level').first()
        if user_to_task is None:
            return Response(DetailTaskSerializer(task, context={'request': request}).data, status=status.HTTP_200_OK)
        if user_to_task.level == get_responsible_task():
            return Response({'detail': 'Responsible user cannot be removed'}, status=status.HTTP_400_BAD_REQUEST)

        removed_user = user_to_task.user
        user_to_task.delete()
        current_user = UserProfile.objects.get(user=request.user)
        send_notification(
            user=removed_user,
            notification_type='task_member_removed',
            title=f'Вас удалили из задачи {task.code}',
            text=task.name,
            actor=current_user,
            project=task.project,
            task=task,
        )
        return Response(DetailTaskSerializer(task, context={'request': request}).data, status=status.HTTP_200_OK)


class TaskCommentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if not can_view_task(task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        comments = CommentTask.objects.filter(user__task=task).select_related('user__user').prefetch_related(
            'attachments'
        ).order_by('created_at', 'id')
        return Response(CommentTaskSerializer(comments, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if not can_comment_task(task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        text = (request.data.get('text') or '').strip()
        files = request.FILES.getlist('attachments') or request.FILES.getlist('files')
        if not text and not files:
            return Response({'detail': 'text or attachments are required'}, status=status.HTTP_400_BAD_REQUEST)

        current_user = get_object_or_404(UserProfile, user=request.user)
        user_to_task = UserToTask.objects.filter(task=task, user=current_user).first()
        if user_to_task is None:
            user_to_task = UserToTask.objects.create(task=task, user=current_user, level=get_collaborator_task())

        comment = CommentTask.objects.create(user=user_to_task, text=text)
        for uploaded_file in files:
            create_attachment(comment, uploaded_file)

        notify_task_participants(
            task=task,
            notification_type='task_comment',
            title=f'Новый комментарий в задаче {task.code}',
            text=task.name,
            actor=current_user,
        )
        serialized_comment = CommentTaskSerializer(comment, context={'request': request}).data
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'task_comments_{task_id}',
            {
                'type': 'comment.created',
                'comment': serialized_comment,
            },
        )
        return Response(serialized_comment, status=status.HTTP_201_CREATED)


class TaskAttachmentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if not can_view_task(task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        attachments = TaskAttachment.objects.filter(task=task).select_related('user', 'user__user')
        return Response(TaskAttachmentSerializer(attachments, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if not can_view_task(task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        files = request.FILES.getlist('attachments') or request.FILES.getlist('files')
        if not files:
            return Response({'detail': 'attachments are required'}, status=status.HTTP_400_BAD_REQUEST)

        current_user = get_object_or_404(UserProfile, user=request.user)
        attachments = [create_attachment(task, uploaded_file, current_user) for uploaded_file in files]
        notify_task_participants(
            task=task,
            notification_type='task_attachment',
            title=f'РќРѕРІРѕРµ РІР»РѕР¶РµРЅРёРµ РІ Р·Р°РґР°С‡Рµ {task.code}',
            text=task.name,
            actor=current_user,
        )
        return Response(TaskAttachmentSerializer(attachments, many=True, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)


class TaskAttachmentDeleteAPIView(DestroyAPIView):
    queryset = TaskAttachment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        attachment = self.get_object()
        is_owner = attachment.user is not None and attachment.user.user == request.user
        if not is_owner and not can_edit_task(attachment.task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if instance.file:
            instance.file.delete(save=False)
        instance.delete()


class NotificationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        current_user = get_object_or_404(UserProfile, user=request.user)
        notifications = Notification.objects.filter(user=current_user).select_related(
            'actor', 'actor__user', 'project', 'project__admin', 'project__admin__user', 'task',
        )[:50]
        return Response(NotificationSerializer(notifications, many=True).data, status=status.HTTP_200_OK)

    def patch(self, request):
        current_user = get_object_or_404(UserProfile, user=request.user)
        ids = request.data.get('ids') or []
        if request.data.get('all'):
            Notification.objects.filter(user=current_user, is_read=False).update(is_read=True)
        else:
            Notification.objects.filter(user=current_user, id__in=ids).update(is_read=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==============================
#      Удаление таска
# ==============================
class TaskDeleteAPIView(DestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if not can_edit_task(self.get_object(), request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        user_to_tasks = UserToTask.objects.filter(task=instance)
        CommentTask.objects.filter(user__in=user_to_tasks).delete()
        SubtaskChecklist.objects.filter(checklist__user__in=user_to_tasks).delete()
        ChecklistTask.objects.filter(user__in=user_to_tasks).delete()
        TaskToSection.objects.filter(task=instance).delete()
        user_to_tasks.delete()
        instance.delete()


# ==============================
#       Чеклист у задачи
# ==============================
class ChecklistTaskView(viewsets.ModelViewSet):
    serializer_class = ChecklistTaskSerializer
    queryset = ChecklistTask.objects.all()
    error = ChecklistError()
    permission_classes = [permissions.IsAuthenticated]

    # Получение всех чеклистов по задаче
    @action(methods=['get'], detail=False)
    def get_checklists(self, request, task_id):
        checklists = self.queryset.filter(user__task__id=task_id, user__user__user=request.user) \
            .order_by(order_by(request))
        if not checklists.exists():
            self.error.is_not_found()

        result = self.serializer_class(checklists, many=True).data
        return Response(result, status=status.HTTP_200_OK)

    # Создание чеклиста
    @action(methods=['post'], detail=False)
    def create_checklist(self, request, task_id):
        current_user = UserProfile.objects.get(user=request.user)
        task = Task.objects.filter(pk=task_id).first()
        if task is None:
            return self.error.is_not_found()
        if not can_edit_task(task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        user_to_task = UserToTask.objects.filter(user=current_user, task=task).first()
        if user_to_task is None:
            return self.error.is_not_found()

        new_position = get_new_position_checklist_by_user_to_task(user_to_task)
        name = request.data.get('name')
        if name is None:
            name = f'Чек-лист {new_position}'
        checklist = ChecklistTask.objects.create(user=user_to_task, name=name, position=new_position)
        serializer = self.serializer_class(checklist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#  Обновление данных у подзадачи чек-листа
class ChecklistUpdateAPIView(UpdateAPIView):
    queryset = ChecklistTask.objects.all()
    serializer_class = ChecklistTaskPreviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if not can_edit_task(self.get_object().user.task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.instance
        new_position = serializer.validated_data.get('position')
        if new_position is not None and new_position != instance.position:
            user_to_task = instance.user
            other_checklist = ChecklistTask.objects.filter(user=user_to_task, position__gte=new_position)

            for checklist in other_checklist:
                checklist.position += 1
                checklist.save()

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


#  Удаление чеклиста
class ChecklistTaskDeleteAPIView(DestroyAPIView):
    queryset = ChecklistTask.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if not can_edit_task(self.get_object().user.task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()


# ==============================
#     Подзадачи у чеклистов
# ==============================
class SubtaskChecklistTaskView(viewsets.ModelViewSet):
    serializer_class = SubtaskChecklistSerializer
    queryset = SubtaskChecklist.objects.all()
    error = SubtaskChecklistError()
    permission_classes = [permissions.IsAuthenticated]

    # Получение всех чеклистов по задаче
    @action(methods=['get'], detail=False)
    def get_subtasks_checklist(self, request, checklist_id):
        subtasks = self.queryset.filter(checklist__id=checklist_id, checklist__user__user__user=request.user) \
            .order_by(order_by(request))
        if not subtasks.exists():
            self.error.is_not_found()

        result = self.serializer_class(subtasks, many=True).data
        return Response(result, status=status.HTTP_200_OK)

    # Создание подзадач у чеклистов
    @action(methods=['post'], detail=False)
    def create_subtask(self, request, checklist_id):
        current_user = UserProfile.objects.get(user=request.user)
        checklist = ChecklistTask.objects.filter(pk=checklist_id, user__user=current_user).first()
        if checklist is None:
            return self.error.is_not_found()
        if not can_edit_task(checklist.user.task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        new_position = get_new_position_subtask_checklist_by_user_to_task(checklist)
        name = request.data.get('name')
        if name is None:
            name = f'Подзадача {new_position}'
        subtask = SubtaskChecklist.objects.create(checklist=checklist, name=name, position=new_position)
        serializer = self.serializer_class(subtask)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#  Обновление данных у подзадачи чек-листа
class SubtaskChecklistUpdateAPIView(UpdateAPIView):
    queryset = SubtaskChecklist.objects.all()
    serializer_class = SubtaskChecklistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if not can_edit_task(self.get_object().checklist.user.task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.instance
        new_position = serializer.validated_data.get('position')

        if new_position is not None and new_position != instance.position:
            checklist = instance.checklist
            other_subtasks = SubtaskChecklist.objects.filter(checklist=checklist, position__gte=new_position)

            for subtask in other_subtasks:
                subtask.position += 1
                subtask.save()

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


#  Удаление подзадачи у чек-листа
class SubtaskChecklistTaskDeleteAPIView(DestroyAPIView):
    queryset = SubtaskChecklist.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if not can_edit_task(self.get_object().checklist.user.task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
