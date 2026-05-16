from django.db.models import QuerySet
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.models import SectionProject
from project.serializers import SectionProjectSerializer, TaskForSectionProjectSerializer
from task.models import TaskToSection, Task
from task.serializers import TaskSerializer, TaskToSectionSerializer
from task.views.task import can_edit_task


def reorder_task_to_section(task_to_section, new_section_project, position):
    old_section_project = task_to_section.section_project
    requested_position = position

    if requested_position is None:
        requested_position = TaskToSection.objects.filter(section_project=new_section_project).count() + 1

    requested_position = max(1, int(requested_position))
    target_items = list(
        TaskToSection.objects
        .filter(section_project=new_section_project)
        .exclude(pk=task_to_section.pk)
        .order_by('position', 'created_at')
    )
    insert_index = min(requested_position - 1, len(target_items))

    task_to_section.section_project = new_section_project
    target_items.insert(insert_index, task_to_section)

    for index, item in enumerate(target_items, start=1):
        item.position = index
        item.section_project = new_section_project
        item.save(update_fields=['section_project', 'position'])

    task_to_section.task.completed_at = timezone.now() if new_section_project.is_final else None
    task_to_section.task.save(update_fields=['completed_at'])

    if old_section_project != new_section_project:
        old_items = TaskToSection.objects.filter(section_project=old_section_project).order_by('position', 'created_at')
        for index, item in enumerate(old_items, start=1):
            if item.position == index:
                continue
            item.position = index
            item.save(update_fields=['position'])

    return old_section_project


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
        task = get_object_or_404(Task, pk=self.kwargs.get('task_id'))
        if not can_edit_task(task, request.user):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        task_to_section = TaskToSection.objects.filter(task=task).first()
        if task_to_section is None:
            task_to_section = TaskToSection.objects.create(task=task, section_project=new_section_project)
        old_section_project = reorder_task_to_section(
            task_to_section,
            new_section_project,
            request.data.get('position'),
        )

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
