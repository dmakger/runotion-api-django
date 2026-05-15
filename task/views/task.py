from django.db.models import Subquery, OuterRef, Q
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import DestroyAPIView, UpdateAPIView, get_object_or_404
from rest_framework.response import Response

from project.models import UserToProject, Project, SectionProject
from service.error.error_view import TaskError, ChecklistError, SubtaskChecklistError
from service.filter.task import TaskFilter
from service.order_by.order_by import order_by
from service.pagination import Pagination
from service.task import get_new_code_task_by_project, get_new_position_checklist_by_user_to_task, \
    get_new_position_subtask_checklist_by_user_to_task
from service.validator import Validator
from task.models import Task, ChecklistTask, UserToTask, SubtaskChecklist, TaskToSection, TaskCategory
from task.serializers import TaskSerializer, DetailTaskSerializer, ChecklistTaskSerializer, SubtaskChecklistSerializer, \
    ChecklistTaskPreviewSerializer, TaskCategorySerializer
from user.models import UserProfile


# ============================
#   Получение всех задач
# ============================
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    error = TaskError()
    filter = TaskFilter

    @action(methods=['post'], detail=False)
    def get_tasks(self, request):
        filter_data = self.filter(request)
        user = filter_data.result.pop('user')

        user_tasks = self.queryset.filter(usertotask__user__user=user, **filter_data.result)
        director_tasks = Task.objects.filter(director__user=user, **filter_data.result)

        if not request.data.get('has_section', True):
            user_tasks = user_tasks.exclude(
                id__in=Subquery(TaskToSection.objects.filter(task_id=OuterRef('pk')).values('task_id'))
            )
            director_tasks = director_tasks.exclude(
                id__in=Subquery(TaskToSection.objects.filter(task_id=OuterRef('pk')).values('task_id'))
            )

        all_tasks = user_tasks.union(director_tasks).order_by(order_by(request))

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

        serializer = self.serializer_class(task)
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

        user_to_project = UserToProject.objects.filter(user__user=request.user, project=task.project)
        if not user_to_project.exists():
            self.error.forbidden()

        result = self.serializer_class(task).data
        return Response(result, status=status.HTTP_200_OK)


#  Обновление данных у задачи
class TaskUpdateAPIView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# ==============================
#      Удаление таска
# ==============================
class TaskDeleteAPIView(DestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
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

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
