from django.db.models import QuerySet, Count, Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chart.core.service import get_projects, get_tasks
from project.models import Project
from project.serializers import ProjectSerializer
from service import difference
from service.difference import get_all_keys
from task.models import Task, UserToTask
from user.models import UserProfile
from user.serializers import UserSerializer


# Количество  задач с отклонением
class NumberOfRejectedTasksChartView(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    @staticmethod
    def sort_by_deadline(tasks: QuerySet):
        result = get_all_keys()
        for task in tasks:
            key = difference.calculate_days(completed_at=task.completed_at, deadline_at=task.deadline)
            result[key] = result.get(key, 0) + 1
        return result

    @action(methods=['post'], detail=False)
    def get_chart(self, request):
        projects = get_projects(request)
        tasks = get_tasks(projects, request)
        serializer_data = self.sort_by_deadline(tasks)
        return Response(serializer_data, status=status.HTTP_200_OK)


# Количество cозданных задач по кварталам
class TaskByQuarterChartView(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    @staticmethod
    def serialize(tasks: QuerySet):
        data = []
        for task in tasks.order_by('created_at'):
            year = task.created_at.year
            quarter = -(-task.created_at.month // 3)
            if len(data) == 0 or data[-1]['year'] != year or data[-1]['quarter'] != quarter:
                data.append({
                    'year': year,
                    'quarter': quarter,
                    'amount': 1
                })
            else:
                data[-1]['amount'] = data[-1]['amount'] + 1
        return data

    @action(methods=['post'], detail=False)
    def get_chart(self, request):
        projects = get_projects(request)
        tasks = get_tasks(projects, request)
        serializer_data = self.serialize(tasks)
        return Response(serializer_data, status=status.HTTP_200_OK)


# Количество задач к исполнителям
class TaskToPerformersChartView(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    @staticmethod
    def serialize(tasks: QuerySet):
        data = {}
        for task in tasks:
            username = task.director.name
            data[username] = data.get(username, 0) + 1
        user_to_tasks = UserToTask.objects.filter(task__in=tasks)

        for user_to_task in user_to_tasks:
            username = user_to_task.user.name
            data[username] = data.get(username, 0) + 1
        return data

    @action(methods=['post'], detail=False)
    def get_chart(self, request):
        projects = get_projects(request)
        tasks = get_tasks(projects, request)
        serializer_data = self.serialize(tasks)
        return Response(serializer_data, status=status.HTTP_200_OK)


class TaskStatusChartView(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    @staticmethod
    def serialize(tasks: QuerySet):
        return {
            'completed': tasks.filter(completed_at__isnull=False).count(),
            'active': tasks.filter(completed_at__isnull=True).count(),
            'overdue': tasks.filter(completed_at__isnull=True, deadline__lt=timezone.now()).count(),
            'without_deadline': tasks.filter(deadline__isnull=True).count(),
        }

    @action(methods=['post'], detail=False)
    def get_chart(self, request):
        projects = get_projects(request)
        tasks = get_tasks(projects, request)
        return Response(self.serialize(tasks), status=status.HTTP_200_OK)


class TasksByProjectChartView(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    @staticmethod
    def serialize(tasks: QuerySet):
        data = tasks.values('project__name').annotate(amount=Count('id')).order_by('-amount')
        return [{'name': it['project__name'], 'amount': it['amount']} for it in data]

    @action(methods=['post'], detail=False)
    def get_chart(self, request):
        projects = get_projects(request)
        tasks = get_tasks(projects, request)
        return Response(self.serialize(tasks), status=status.HTTP_200_OK)


class TasksByDirectorChartView(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    @staticmethod
    def serialize(tasks: QuerySet):
        data = tasks.values('director__name', 'director__user__username').annotate(amount=Count('id')).order_by('-amount')
        return [
            {
                'name': it['director__name'] or it['director__user__username'],
                'amount': it['amount']
            } for it in data
        ]

    @action(methods=['post'], detail=False)
    def get_chart(self, request):
        projects = get_projects(request)
        tasks = get_tasks(projects, request)
        return Response(self.serialize(tasks), status=status.HTTP_200_OK)


class ChartFiltersView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_available_projects(request):
        current_user = UserProfile.objects.get(user=request.user)
        return Project.objects.filter(
            Q(admin=current_user) | Q(usertoproject__user=current_user)
        ).distinct()

    @staticmethod
    def apply_user_filter(projects, users_id):
        if not users_id:
            return projects
        task_projects = Task.objects.filter(
            Q(director__id__in=users_id) | Q(usertotask__user__id__in=users_id)
        ).values_list('project_id', flat=True)
        return projects.filter(
            Q(admin__id__in=users_id) |
            Q(usertoproject__user__id__in=users_id) |
            Q(id__in=task_projects)
        ).distinct()

    @staticmethod
    def get_available_users(projects, projects_id):
        filtered_projects = projects
        if projects_id:
            filtered_projects = projects.filter(id__in=projects_id)

        task_users = UserToTask.objects.filter(task__project__in=filtered_projects).values_list('user_id', flat=True)
        directors = Task.objects.filter(project__in=filtered_projects).values_list('director_id', flat=True)
        members = filtered_projects.values_list('usertoproject__user_id', flat=True)
        admins = filtered_projects.values_list('admin_id', flat=True)

        return UserProfile.objects.filter(
            Q(id__in=task_users) |
            Q(id__in=directors) |
            Q(id__in=members) |
            Q(id__in=admins)
        ).select_related('user', 'department').distinct()

    @staticmethod
    def add_selected_projects(projects, base_projects, projects_id):
        if not projects_id:
            return projects
        return (projects | base_projects.filter(id__in=projects_id)).distinct()

    @staticmethod
    def add_selected_users(users, users_id):
        if not users_id:
            return users
        return (users | UserProfile.objects.filter(id__in=users_id)).select_related('user', 'department').distinct()

    @action(methods=['post'], detail=False)
    def get_filters(self, request):
        projects_id = request.data.get('projects', [])
        users_id = request.data.get('users', [])
        project_search = request.data.get('project_search', '').strip()
        user_search = request.data.get('user_search', '').strip()

        base_projects = self.get_available_projects(request)
        projects = self.apply_user_filter(base_projects, users_id)
        users = self.get_available_users(base_projects, projects_id)

        if project_search:
            projects = projects.filter(
                Q(name__icontains=project_search) |
                Q(code__icontains=project_search)
            )

        if user_search:
            users = users.filter(
                Q(name__icontains=user_search) |
                Q(user__username__icontains=user_search) |
                Q(department__name__icontains=user_search)
            )

        projects = self.add_selected_projects(projects, base_projects, projects_id)
        users = self.add_selected_users(users, users_id)

        return Response({
            'projects': ProjectSerializer(projects.order_by('name')[:50], many=True).data,
            'users': UserSerializer(users.order_by('name', 'user__username')[:50], many=True).data,
        }, status=status.HTTP_200_OK)
