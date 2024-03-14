from django.db.models import QuerySet
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Color
from core.service import get_color
from project.models import SectionProject, Project


class ColorView(viewsets.ModelViewSet):
    queryset = Color.objects.all().order_by('pk')
    permission_classes = [permissions.IsAdminUser]

    @action(methods=['put'], detail=False)
    def update_colors_section_projects(self, request):
        projects: QuerySet[Project] = Project.objects.all()
        sections: QuerySet[SectionProject] = SectionProject.objects.all().order_by('project', 'position')
        for project in projects:
            project_sections: QuerySet[SectionProject] = sections.filter(project=project)
            i = 0
            for section in project_sections:
                section.color = get_color(i, self.queryset)
                section.save()
                i += 1
        return Response(status=status.HTTP_200_OK)

