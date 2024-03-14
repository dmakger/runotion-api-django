from django.db.models import QuerySet
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.models import SectionProject
from project.serializers import SectionProjectSerializer, TaskForSectionProjectSerializer
from task.models import TaskToSection, Task
from task.serializers import TaskSerializer


class SectionProjectDetailAPIView(RetrieveAPIView):
    queryset = SectionProject.objects.all()
    serializer_class = SectionProjectSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        section = self.get_object()
        tasks: QuerySet = TaskToSection.objects.filter(section_project=section).values('task')
        serializer = TaskSerializer(Task.objects.filter(id__in=tasks), many=True)
        return Response(serializer.data)


class UpdateTaskSectionProject(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        section_project_id = get_object_or_404(SectionProject, pk=self.kwargs.get('section_project_id'))
        task_to_section = get_object_or_404(TaskToSection, task__pk=self.kwargs.get('task_id'))

        task_to_section.section_project_id = section_project_id
        task_to_section.save()

        serializer = TaskSerializer(task_to_section.task)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

