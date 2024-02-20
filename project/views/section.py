from rest_framework import permissions, status, generics
from rest_framework.generics import DestroyAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project.models import Project, SectionProject
from project.serializers import ProjectUpdateSerializer, \
    SectionProjectSerializer, SectionProjectUpdateSerializer, SectionProjectWithTaskSerializer
from service.error.error_view import ProjectError, SectionProjectError

from service.position import fix_positions


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
        old_position = instance.position

        # Проверяем, что пользователь является админом
        if self.request.user != instance.project.admin.user:
            return self.error.forbidden()

        serializer.save()

        if old_position != instance.position:
            qs = self.queryset.filter(project=instance.project).order_by('position')
            fix_positions(qs, instance, old_position)

        return Response(serializer.data, status=status.HTTP_200_OK)


#  Удаление этапа у проекта
class SectionProjectDeleteAPIView(DestroyAPIView):
    queryset = SectionProject.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()
