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
from task.serializers import TaskSerializer, TaskToSectionSerializer


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
        new_section_project = get_object_or_404(SectionProject, pk=self.kwargs.get('section_project_id'))
        task_to_section = get_object_or_404(TaskToSection, task__pk=self.kwargs.get('task_id'))

        old_section_project = task_to_section.section_project
        task_to_section.section_project = new_section_project
        task_to_section.save()

        return JsonResponse({
            "new_section_id": task_to_section.section_project.id,
            "old_section_id": old_section_project.id,
        }, status=status.HTTP_200_OK)


class AddTaskToSectionProject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        section_project = get_object_or_404(SectionProject, pk=self.kwargs.get('section_project_id'))
        task = get_object_or_404(Task, pk=self.kwargs.get('task_id'))

        if TaskToSection.objects.filter(task=task).exists():
            return JsonResponse({'is_exists': True}, status=status.HTTP_302_FOUND)

        task_to_section = TaskToSection.objects.create(task=task, section_project=section_project)
        task_to_section.save()

        return JsonResponse(TaskToSectionSerializer(task_to_section).data, status=status.HTTP_200_OK)
