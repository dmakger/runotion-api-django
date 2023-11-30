from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.decorators import action
# Количество  задач с отклонением
from rest_framework.response import Response

from project.models import Project
from service.list import get_records_from_model, get_parents_records, get_records_from_queryset
from task.models import Task, UserLevelTask, UserToTask
from task.service import get_director_task
from user.models import UserProfile
from service import difference


class NumberOfRejectedTasksChartView(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    # Получение проектов
    @staticmethod
    def get_projects(request):
        projects = request.data.get('projects', [])

        current_user = UserProfile.objects.get(user=request.user)
        projects_qs = Project.objects.filter(admin=current_user)
        if projects:
            projects_qs = projects_qs.filter(id__in=projects)
        return projects_qs

    def get_tasks(self, projects, request):
        users_id = request.data.get('users', [])
        levels_id = request.data.get('levels', [])

        task_to_project_qs = self.queryset.filter(project__in=projects)
        levels_qs = get_records_from_model(UserLevelTask, {'id__in': levels_id})
        print(levels_qs)
        user_to_task_qs = get_records_from_model(UserToTask, {
            'task__in': task_to_project_qs,
            'user__id__in': users_id,
            'level__in': levels_qs,
        })

        tasks = get_parents_records(user_to_task_qs, Task, ['task'])
        director_level_task = get_director_task()
        if director_level_task not in levels_qs:
            return tasks


        director_tasks = get_records_from_queryset(task_to_project_qs, {'director__in': users_id})
        print(director_tasks)
        return tasks.union(director_tasks)

    @staticmethod
    def sort_by_deadline(tasks: QuerySet):
        result = {}
        for task in tasks:
            key = difference.calculate_days(completed_at=task.completed_at, deadline_at=task.deadline)
            result[key] = result.get(key, 0) + 1
        return result


    @action(methods=['get'], detail=False)
    def get_chart(self, request):
        projects = self.get_projects(request)
        tasks = self.get_tasks(projects, request)
        serializer_data = self.sort_by_deadline(tasks)
        return Response(serializer_data, status=status.HTTP_200_OK)
