from django.contrib import admin

from project.models import RoleProject, Project, ActionProject, SectionProject, HistoryProject, UserToProject
from service.position import get_new_position, fix_positions


#  Проект
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'admin', 'image', 'created_at']


#  Роль в проекте
class RoleProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'level']


#  Пользователь к проекту
class UserToProjectAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'role', 'created_at']


#  Этапы в проекте (Канбан)
class SectionProjectAdmin(admin.ModelAdmin):
    list_display = ['project', 'name', 'position', 'created_at']

    def save_model(self, request, obj, form, change):
        sections = SectionProject.objects.filter(project=obj.project).order_by('position')
        obj.position = get_new_position(sections, obj.position)
        super().save_model(request, obj, form, change)
        fix_positions(sections)


#  Пользователь к проекту
class HistoryProjectAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'action', 'victim', 'created_at']


admin.site.register(Project, ProjectAdmin)
admin.site.register(RoleProject, RoleProjectAdmin)
admin.site.register(UserToProject, UserToProjectAdmin)
admin.site.register(SectionProject, SectionProjectAdmin)
admin.site.register(ActionProject)
admin.site.register(HistoryProject, HistoryProjectAdmin)
