from rest_framework import permissions, status, generics
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from project.models import Project, SectionProject
from project.serializers import ProjectUpdateSerializer, \
    SectionProjectSerializer, SectionProjectUpdateSerializer
from service.error.error_view import ProjectError, SectionProjectError

# ==============================
#       СЕКЦИИ У ПРОЕКТОВ
# ==============================

# Получение всех секций
from service.position import fix_positions


class SectionProjectListView(generics.ListAPIView):
    serializer_class = SectionProjectSerializer

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        return SectionProject.objects.filter(project__pk=project_pk).order_by('position')


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
            # print(old_position, instance.position, qs.index(instance))
            # print(instance, qs)
            fix_positions(qs, instance, old_position)
            # fix_positions(qs, instance, )

        return Response(serializer.data, status=status.HTTP_200_OK)


#  Удаление этапа у проекта
class SectionProjectDeleteAPIView(DestroyAPIView):
    queryset = SectionProject.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()
