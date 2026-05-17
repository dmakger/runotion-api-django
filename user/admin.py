from django.contrib import admin

from django.contrib.auth.models import User

from user.models import UserProfile, Department, RegistrationRequest


#  Расширенные пользователи
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']


#  Расширенные пользователи
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'department', 'image']


class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'display_login', 'full_name', 'status', 'created_user', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['mts_login', 'username', 'full_name', 'comment']
    readonly_fields = ['created_user', 'created_at', 'updated_at']
    actions = ['approve_requests', 'reject_requests']

    @admin.display(description='Логин')
    def display_login(self, instance):
        return instance.mts_login or instance.username

    @admin.action(description='Принять выбранные заявки')
    def approve_requests(self, request, queryset):
        for registration_request in queryset.filter(status=RegistrationRequest.STATUS_PENDING):
            username = registration_request.mts_login or registration_request.username
            if not username:
                continue
            user, created = User.objects.get_or_create(username=username)
            if created and registration_request.password:
                user.set_password(registration_request.password)
                user.save(update_fields=['password'])

            profile = user.userprofile
            if registration_request.full_name:
                profile.name = registration_request.full_name
                profile.save(update_fields=['name'])

            registration_request.status = RegistrationRequest.STATUS_APPROVED
            registration_request.created_user = user
            registration_request.save(update_fields=['status', 'created_user', 'updated_at'])

    @admin.action(description='Отклонить выбранные заявки')
    def reject_requests(self, request, queryset):
        queryset.filter(status=RegistrationRequest.STATUS_PENDING).update(status=RegistrationRequest.STATUS_REJECTED)


admin.site.register(Department, DepartmentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(RegistrationRequest, RegistrationRequestAdmin)
