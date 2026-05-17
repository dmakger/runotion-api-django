from rest_framework import serializers
from django.db.models import Q

from project.models import Project
from task.models import Task, UserToTask
from user.models import UserProfile, Department, RegistrationRequest


class PreviewUserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'username', 'department', 'image']

    @staticmethod
    def get_username(instance: UserProfile):
        return instance.user.username

    @staticmethod
    def get_department(instance: UserProfile):
        if instance.department is None:
            return None
        return instance.department.name


class UserSerializer(PreviewUserSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'username', 'department', 'image']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'image']
        read_only_fields = ['id']


class UserProfileDetailSerializer(PreviewUserSerializer):
    projects = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'username', 'department', 'image', 'projects', 'stats']

    @staticmethod
    def get_projects(instance: UserProfile):
        projects = Project.objects.filter(
            Q(admin=instance) | Q(usertoproject__user=instance)
        ).select_related('admin', 'admin__user', 'admin__department').distinct().order_by('-created_at')[:8]
        return [
            {
                'id': project.id,
                'name': project.name,
                'code': project.code,
                'image': project.image.url if project.image else None,
                'admin': PreviewUserSerializer(project.admin).data,
            }
            for project in projects
        ]

    @staticmethod
    def get_stats(instance: UserProfile):
        member_projects = Project.objects.filter(admin=instance) | Project.objects.filter(usertoproject__user=instance)
        tasks = Task.objects.filter(project__in=member_projects.distinct()).distinct()
        user_tasks = UserToTask.objects.filter(user=instance)
        return {
            'projects': member_projects.distinct().count(),
            'directed_tasks': Task.objects.filter(director=instance).count(),
            'assigned_tasks': user_tasks.count(),
            'completed_tasks': tasks.filter(completed_at__isnull=False).count(),
            'active_tasks': tasks.filter(completed_at__isnull=True).count(),
        }


class RegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationRequest
        fields = ['id', 'mts_login', 'username', 'password', 'full_name', 'comment', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False, 'allow_blank': True},
        }

    def validate(self, attrs):
        mts_login = (attrs.get('mts_login') or '').strip()
        username = (attrs.get('username') or '').strip()
        password = attrs.get('password') or ''

        if not mts_login and not username:
            raise serializers.ValidationError('Укажите логин МТС или логин для регистрации')
        if username and not password:
            raise serializers.ValidationError('Для регистрации по учетным данным нужен пароль')

        attrs['mts_login'] = mts_login
        attrs['username'] = username
        return attrs
