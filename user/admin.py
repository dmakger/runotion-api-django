from django.contrib import admin

from user.models import UserProfile, Department


#  Расширенные пользователи
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']


#  Расширенные пользователи
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'department', 'image']


admin.site.register(Department, DepartmentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
