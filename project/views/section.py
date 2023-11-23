from rest_framework import permissions, status, generics
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from project.models import Project, SectionProject
from project.serializers import ProjectUpdateSerializer, \
    SectionProjectSerializer
from service.error.error_view import ProjectError


# ==============================
#       СЕКЦИИ У ПРОЕКТОВ
# ==============================

# Получение всех секций
class SectionProjectListView(generics.ListAPIView):
    serializer_class = SectionProjectSerializer

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        return SectionProject.objects.filter(project__pk=project_pk).order_by('position')


#  Обновление данных у подзадачи чек-листа
class ProjectUpdateAPIView(UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    error = ProjectError()

    def perform_update(self, serializer):
        instance = serializer.instance

        # Проверяем, что пользователь является админом
        if self.request.user != instance.admin.user:
            return self.error.forbidden()

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


#  Удаление таска
class ProjectDeleteAPIView(DestroyAPIView):
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()
