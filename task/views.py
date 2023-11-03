from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from project.models import UserToProject
from service.error.error_view import TaskError, ChecklistError
from service.filter.task import TaskFilter
from service.order_by.order_by import order_by
from service.pagination import Pagination
from task.models import Task, ChecklistTask
from task.serializers import TaskSerializer, DetailTaskSerializer, ChecklistTaskSerializer


# ============================
#   Получение всех задач
# ============================
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter = TaskFilter

    @action(methods=['get'], detail=False)
    def get_tasks(self, request):
        filter_data = self.filter(request)
        user = filter_data.result.pop('user')

        user_tasks = self.queryset.filter(usertotask__user__user=user, **filter_data.result)
        director_tasks = Task.objects.filter(director__user=user, **filter_data.result)
        all_tasks = user_tasks.union(director_tasks).order_by(order_by(request))

        result = Pagination(request=request, queryset=all_tasks).get()
        result['results'] = self.serializer_class(result.get('results'), many=True).data
        return Response(result, status=status.HTTP_200_OK)


# ==============================
#   Детальная страница задачи
# ==============================
class DetailTaskView(viewsets.ModelViewSet):
    serializer_class = DetailTaskSerializer
    queryset = Task.objects.all()
    error = TaskError()
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def get_detail_task(self, request, code):
        tasks = self.queryset.filter(code=code)
        if len(tasks) == 0:
            self.error.is_not_found()

        task = tasks[0]
        user_to_project = UserToProject.objects.filter(user__user=request.user, project=task.project)
        if len(user_to_project) == 0:
            self.error.forbidden()

        result = self.serializer_class(task).data
        return Response(result, status=status.HTTP_200_OK)


# ==============================
#       Чеклист у задачи
# ==============================
class ChecklistTaskView(viewsets.ModelViewSet):
    serializer_class = ChecklistTaskSerializer
    queryset = ChecklistTask.objects.all()
    error = ChecklistError()
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def get_checklists(self, request, code):
        checklists = self.queryset.filter(user__task__code=code, user__user__user=request.user)\
            .order_by(order_by(request))
        if len(checklists) == 0:
            self.error.is_not_found()

        result = self.serializer_class(checklists, many=True).data
        return Response(result, status=status.HTTP_200_OK)
