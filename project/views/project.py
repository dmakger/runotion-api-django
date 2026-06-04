from django.db.models import Count, Q
from django.http import Http404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import ImportanceLevel
from project.models import Project, RoleProject, SectionProject, UserToProject
from project.serializers import ProjectSerializer, ProjectUpdateSerializer, \
    ProjectWithRoleSerializer, RoleProjectSerializer, UserToProjectSerializer
from project.service import get_admin_project
from service.error.error_view import ProjectError
from service.filter.project import ProjectFilter
from service.order_by.order_by import order_by
from service.pagination import Pagination
from service.validator import Validator
from task.models import ChecklistTask, CommentTask, SubtaskChecklist, Task, TaskToSection, UserToTask
from task.notifications import send_notification
from user.models import UserProfile


# =====================
#       ПРОЕКТЫ
# =====================
class ProjectView(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter = ProjectFilter
    error = ProjectError()

    @staticmethod
    def apply_search(queryset, search):
        if not search:
            return queryset

        return queryset.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search) |
            Q(admin__name__icontains=search) |
            Q(admin__user__username__icontains=search) |
            Q(usertoproject__user__name__icontains=search) |
            Q(usertoproject__user__user__username__icontains=search) |
            Q(usertoproject__role__name__icontains=search)
        ).distinct()

    # Получение всех проектов
    @action(methods=['get'], detail=False)
    def get_projects(self, request):
        filter_data = self.filter(request)
        user = filter_data.result.pop('user', request.user)
        search = request.query_params.get('search')

        user_projects = self.queryset.filter(usertoproject__user__user=user, **filter_data.result)
        admin_projects = self.queryset.filter(admin__user=user, **filter_data.result)
        user_projects = self.apply_search(user_projects, search)
        admin_projects = self.apply_search(admin_projects, search)
        all_projects = user_projects.union(admin_projects).order_by(order_by(request))

        result = Pagination(request=request, queryset=all_projects).get()
        result['results'] = ProjectWithRoleSerializer(result.get('results'), context={'user': user}, many=True).data
        return Response(result, status=status.HTTP_200_OK)

    # Получение проекта по id
    @action(methods=['get'], detail=True)
    def get_project_by_id(self, request, pk=None):
        try:
            project = self.get_object()
            serializer = self.get_serializer(project)
            return Response(serializer.data)
        except Http404:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    # Создание проекта
    @action(methods=['post'], detail=False)
    def create_project(self, request):
        validator = Validator(request=request)
        if not validator.has_content(['name', 'code']):
            return self.error.is_not_content_form()

        name = request.data['name']
        code = request.data['code']
        current_user = UserProfile.objects.get(user=request.user)
        result = self.queryset.filter(code=code, admin=current_user)
        if result.exists():
            return self.error.is_exists()

        project = Project.objects.create(name=name, code=code, admin=current_user)
        serializer = self.serializer_class(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#  Обновление данных у подзадачи чек-листа
class ProjectUpdateAPIView(UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    error = ProjectError()

    def perform_update(self, serializer):
        instance = serializer.instance

        if self.request.user != instance.admin.user:
            return self.error.forbidden()

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


#  Удаление таска
class ProjectDeleteAPIView(DestroyAPIView):
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    error = ProjectError()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.admin.user:
            return self.error.forbidden()
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        tasks = Task.objects.filter(project=instance)
        user_to_tasks = UserToTask.objects.filter(task__in=tasks)
        CommentTask.objects.filter(user__in=user_to_tasks).delete()
        SubtaskChecklist.objects.filter(checklist__user__in=user_to_tasks).delete()
        ChecklistTask.objects.filter(user__in=user_to_tasks).delete()
        TaskToSection.objects.filter(task__in=tasks).delete()
        user_to_tasks.delete()
        instance.delete()


class RoleProjectListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        roles = RoleProject.objects.select_related('level').order_by('level__value', 'name')
        serializer = RoleProjectSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectUserListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_project(self, project_pk):
        return Project.objects.filter(pk=project_pk).first()

    @staticmethod
    def can_manage_users(project, user):
        if project.admin.user == user:
            return True

        user_to_project = UserToProject.objects.filter(
            project=project,
            user__user=user,
        ).select_related('role', 'role__level').first()
        if user_to_project is None:
            return False

        role_name = (user_to_project.role.name or '').casefold()
        if 'manager' in role_name or '\u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440' in role_name:
            return True

        role_values = list(ImportanceLevel.objects.order_by('-value').values_list('value', flat=True)[:2])
        if len(role_values) < 2:
            return False
        return user_to_project.role.level.value >= role_values[-1]

    def get(self, request, project_pk):
        project = self.get_project(project_pk)
        if project is None:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        is_admin = project.admin.user == request.user
        is_member = UserToProject.objects.filter(project=project, user__user=request.user).exists()
        if not is_admin and not is_member:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        search = request.query_params.get('search', '').strip()
        users_to_project = UserToProject.objects.filter(project=project).select_related(
            'user', 'user__user', 'role', 'role__level'
        ).order_by('user__name', 'user__user__username')
        if search:
            users_to_project = users_to_project.filter(
                Q(user__name__icontains=search) |
                Q(user__user__username__icontains=search) |
                Q(role__name__icontains=search)
            )

        result = Pagination(request=request, queryset=users_to_project).get()
        result['results'] = UserToProjectSerializer(result.get('results'), many=True).data

        current_page = int(request.query_params.get('page', 1))
        admin_role = get_admin_project()
        admin_matches_search = (
            not search or
            search.casefold() in (project.admin.name or '').casefold() or
            search.casefold() in project.admin.user.username.casefold() or
            search.casefold() in (admin_role.name or '').casefold()
        )
        if current_page == 1 and admin_matches_search:
            result['results'].insert(0, {
                'id': None,
                'user': ProjectSerializer(project).data['admin'],
                'project': project.id,
                'role': RoleProjectSerializer(admin_role).data,
                'created_at': project.created_at.isoformat(),
            })
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request, project_pk):
        project = self.get_project(project_pk)
        if project is None:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        if not self.can_manage_users(project, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        role_id = request.data.get('role_id')
        if not user_id or not role_id:
            return Response({'detail': 'user_id and role_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = UserProfile.objects.filter(pk=user_id).first()
        role = RoleProject.objects.filter(pk=role_id).first()
        if user_profile is None or role is None:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        if user_profile == project.admin:
            return Response({'detail': 'Project admin already has a role'}, status=status.HTTP_400_BAD_REQUEST)

        current_user = UserProfile.objects.get(user=request.user)
        old_user_to_project = UserToProject.objects.filter(project=project, user=user_profile).select_related('role').first()
        user_to_project, created = UserToProject.objects.update_or_create(
            project=project,
            user=user_profile,
            defaults={'role': role},
        )
        if created:
            send_notification(
                user=user_profile,
                notification_type='project_member_added',
                title=f'Вас добавили в проект {project.name}',
                actor=current_user,
                project=project,
            )
        elif old_user_to_project is not None and old_user_to_project.role_id != role.id:
            send_notification(
                user=user_profile,
                notification_type='project_role_changed',
                title=f'Изменена роль в проекте {project.name}',
                text=role.name,
                actor=current_user,
                project=project,
            )
        serializer = UserToProjectSerializer(user_to_project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, project_pk, user_pk=None):
        project = self.get_project(project_pk)
        if project is None:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        if not self.can_manage_users(project, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        if user_pk is None:
            return Response({'detail': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        if project.admin_id == user_pk:
            return Response({'detail': 'Project admin cannot be removed'}, status=status.HTTP_400_BAD_REQUEST)

        user_to_project = UserToProject.objects.filter(project=project, user_id=user_pk).select_related('user').first()
        if user_to_project is not None:
            removed_user = user_to_project.user
            user_to_project.delete()
            current_user = UserProfile.objects.get(user=request.user)
            send_notification(
                user=removed_user,
                notification_type='project_member_removed',
                title=f'Вас удалили из проекта {project.name}',
                actor=current_user,
                project=project,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
