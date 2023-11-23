from django.contrib import admin

from task.models import Task, UserLevelTask, UserToTask, CommentTask, ChecklistTask, SubtaskChecklist, TaskToSection

admin.site.register(Task)
admin.site.register(TaskToSection)
admin.site.register(UserLevelTask)
admin.site.register(UserToTask)
admin.site.register(CommentTask)
admin.site.register(ChecklistTask)
admin.site.register(SubtaskChecklist)
