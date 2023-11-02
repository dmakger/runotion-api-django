from django.contrib import admin

from project.models import RoleProject, Project, ActionProject, SectionProject, HistoryProject

admin.site.register(Project)
admin.site.register(RoleProject)
admin.site.register(SectionProject)
admin.site.register(ActionProject)
admin.site.register(HistoryProject)
