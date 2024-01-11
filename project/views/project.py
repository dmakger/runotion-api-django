from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from project.models import Project
from project.serializers import ProjectSerializer, PreviewProjectSerializer, ProjectUpdateSerializer, \
    ProjectWithRoleSerializer
from service.error.error_view import ProjectError
from service.filter.project import ProjectFilter
from service.order_by.order_by import order_by
from service.pagination import Pagination
from service.validator import Validator
from user.models import UserProfile


# =====================
#       ПРОЕКТЫ
# =====================
class ProjectView(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter = ProjectFilter
    error = ProjectError()

    # Получение всех проектов
    @action(methods=['get'], detail=False)
    def get_projects(self, request):
        filter_data = self.filter(request)
        user = filter_data.result.pop('user')

        user_projects = self.queryset.filter(usertoproject__user__user=user, **filter_data.result)
        admin_projects = self.queryset.filter(admin__user=user, **filter_data.result)
        all_projects = user_projects.union(admin_projects).order_by(order_by(request))
        print(user)

        result = Pagination(request=request, queryset=all_projects).get()
        result['results'] = ProjectWithRoleSerializer(result.get('results'), context={'user': user}, many=True).data
        return Response(result, status=status.HTTP_200_OK)

    # Создание проекта
    @action(methods=['post'], detail=False)
    def create_project(self, request):
        validator = Validator(request=request)
        if not validator.has_content(['name', 'code']):
            return self.error.is_not_content_form()

        name = request.data['name']
        code = request.data['code']
        current_user = UserProfile.objects.get(user=request.user)
        result = self.queryset.filter(code=code, admin=current_user)
        if len(result) > 0:
            return self.error.is_exists()

        project = Project.objects.create(name=name, code=code, admin=current_user)
        serializer = self.serializer_class(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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