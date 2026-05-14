from rest_framework import permissions, status, generics
from rest_framework.generics import DestroyAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project.models import Project, SectionProject
from project.serializers import ProjectUpdateSerializer, \
    SectionProjectSerializer, SectionProjectUpdateSerializer, SectionProjectWithTaskSerializer
from service.error.error_view import ProjectError, SectionProjectError

from service.position import fix_positions


def move_section_project(instance, position):
    requested_position = max(1, int(position))
    sections = list(
        SectionProject.objects
        .filter(project=instance.project)
        .exclude(pk=instance.pk)
        .order_by('position', 'created_at')
    )
    insert_index = min(requested_position - 1, len(sections))
    sections.insert(insert_index, instance)

    for index, section in enumerate(sections, start=1):
        if section.position == index:
            continue
        section.position = index
        section.save(update_fields=['position'])


# ==============================
#       СЕКЦИИ У ПРОЕКТОВ
# ==============================


# Получение всех секций
class SectionProjectListView(generics.ListAPIView):
    serializer_class = SectionProjectWithTaskSerializer

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        return SectionProject.objects.filter(project__pk=project_pk).order_by('position')


# Создание секций
class SectionProjectCreateAPIView(CreateAPIView):
    queryset = SectionProject.objects.all()
    serializer_class = SectionProjectSerializer
    permission_classes = [IsAuthenticated]
    error = SectionProjectError()

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(id=project_id)

        # Проверяем, что пользователь является админом проекта
        if self.request.user != project.admin.user:
            return self.error.forbidden()

        serializer.save(project=project)
        qs = self.queryset.filter(project=project).order_by('position', 'created_at')
        fix_positions(qs)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


#  Обновление данных у подзадачи чек-листа
class SectionProjectUpdateAPIView(UpdateAPIView):
    queryset = SectionProject.objects.all()
    serializer_class = SectionProjectUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    error = SectionProjectError()

    def perform_update(self, serializer):
        instance = serializer.instance
        new_position = serializer.validated_data.get('position')

        # Проверяем, что пользователь является админом
        if self.request.user != instance.project.admin.user:
            return self.error.forbidden()

        serializer.save(position=instance.position if new_position is not None else instance.position)

        if new_position is not None:
            move_section_project(instance, new_position)

        return Response(serializer.data, status=status.HTTP_200_OK)


#  Удаление этапа у проекта
class SectionProjectDeleteAPIView(DestroyAPIView):
    queryset = SectionProject.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()
