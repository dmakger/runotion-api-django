from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from project.models import Project
from project.serializers import ProjectSerializer
from service.pagination import Pagination


# ============================
#   Получение всех проектов
# ============================

class ProjectView(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def get_my_projects(self, request):
        user_projects = self.queryset.filter(usertoproject__user__user=request.user).order_by('created_at')
        result = Pagination(request=request, queryset=user_projects).get()
        result['results'] = self.serializer_class(result.get('results'), many=True).data
        return Response(result, status=status.HTTP_200_OK)
