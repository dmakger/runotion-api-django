from django.contrib import admin

from project.models import RoleProject, Project, ActionProject, SectionProject, HistoryProject, UserToProject
from service.position import get_new_position, fix_positions


class SectionProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'project', 'created_at']

    def save_model(self, request, obj, form, change):
        sections = SectionProject.objects.filter(project=obj.project).order_by('position')
        obj.position = get_new_position(sections, obj.position)
        super().save_model(request, obj, form, change)
        fix_positions(SectionProject.objects.filter(project=obj.project).order_by('position'))


admin.site.register(SectionProject, SectionProjectAdmin)

admin.site.register(Project)
admin.site.register(RoleProject)
admin.site.register(UserToProject)
admin.site.register(ActionProject)
admin.site.register(HistoryProject)
