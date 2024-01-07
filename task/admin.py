from django.contrib import admin

from service.position import get_new_position, fix_positions
from task.models import Task, UserLevelTask, UserToTask, CommentTask, ChecklistTask, SubtaskChecklist, TaskToSection


#  Задачи
class TaskAdmin(admin.ModelAdmin):
    list_display = ['project', 'name', 'code', 'director', 'created_at', 'deadline', 'completed_at']


#  Задачи к Секции
class TaskToSectionAdmin(admin.ModelAdmin):
    list_display = ['task', 'section_project', 'position', 'created_at']

    def save_model(self, request, obj, form, change):
        qs = TaskToSection.objects.filter(section_project=obj.section_project).order_by('position')
        obj.position = get_new_position(qs, obj.position)
        super().save_model(request, obj, form, change)
        fix_positions(qs)


#  Задачи к Секции
class UserLevelTaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'level']


#  Задачи к Секции
class UserToTaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'task', 'level', 'created_at']


#  Задачи к Секции
class CommentTaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'created_at']


#  Задачи к Секции
class ChecklistTaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'position', 'completed_at', 'created_at']

    def save_model(self, request, obj, form, change):
        qs = ChecklistTask.objects.filter(user=obj.user).order_by('position')
        obj.position = get_new_position(qs, obj.position)
        super().save_model(request, obj, form, change)
        fix_positions(qs)


#  Задачи к Секции
class SubtaskChecklistAdmin(admin.ModelAdmin):
    list_display = ['checklist', 'name', 'position', 'completed_at', 'created_at']

    def save_model(self, request, obj, form, change):
        qs = SubtaskChecklist.objects.filter(checklist=obj.checklist).order_by('position')
        obj.position = get_new_position(qs, obj.position)
        super().save_model(request, obj, form, change)
        fix_positions(qs)


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskToSection, TaskToSectionAdmin)
admin.site.register(UserLevelTask, UserLevelTaskAdmin)
admin.site.register(UserToTask, UserToTaskAdmin)
admin.site.register(CommentTask, CommentTaskAdmin)
admin.site.register(ChecklistTask, ChecklistTaskAdmin)
admin.site.register(SubtaskChecklist, SubtaskChecklistAdmin)
