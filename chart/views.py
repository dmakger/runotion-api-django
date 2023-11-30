from rest_framework import viewsets, status
from rest_framework.decorators import action


# Количество  задач с отклонением
from rest_framework.response import Response

from project.models import Project
from task.models import Task
from user.models import UserProfile


class NumberOfRejectedTasksChartView(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    @staticmethod
    def get_projects(request):
        projects = request.data.get('projects', [])

        current_user = UserProfile.objects.get(user=request.user)
        projects_qs = Project.objects.filter(admin=current_user)
        if projects:
            projects_qs = projects_qs.filter(id__in=projects)
        return projects_qs

    def get_tasks(self, projects, request):
        users = request.data.get('users', [])
        levels = request.data.get('levels', [])

        current_user = UserProfile.objects.get(user=request.user)
        self.queryset.filter()


    @action(methods=['get'], detail=False)
    def get_chart(self, request):
        users = request.data.get('users', [])

        current_user = UserProfile.objects.get(user=request.user)
        projects = self.get_projects(request)
        print(projects)

        return Response({}, status=status.HTTP_200_OK)
