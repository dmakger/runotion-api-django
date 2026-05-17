from rest_framework import serializers

from core.models import Color
from core.serializers import ImportanceLevelSerializer, ColorSerializer
from project.models import Project, SectionProject, UserToProject, RoleProject
from project.service import get_admin_project
from task.models import TaskToSection, Task, UserToTask
from task.service import get_responsible_task
from user.models import UserProfile
from user.serializers import PreviewUserSerializer, UserSerializer


# =====================
#    РОЛИ В ПРОЕКТАХ
# =====================

class RoleProjectSerializer(serializers.ModelSerializer):
    level = ImportanceLevelSerializer()

    class Meta:
        model = RoleProject
        fields = '__all__'


# ====================
#       ПРОЕКТЫ
# ====================

class ProjectSerializer(serializers.ModelSerializer):
    admin = PreviewUserSerializer()

    class Meta:
        model = Project
        fields = ['id', 'name', 'code', 'admin', 'image']


class ProjectWithRoleSerializer(serializers.ModelSerializer):
    admin = PreviewUserSerializer()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'code', 'admin', 'image', 'role']

    def get_role(self, instance):
        user = self.context.get('user')
        if user is None:
            return

        qs = UserToProject.objects.filter(user__user=user, project=instance)
        user_to_project = qs.first()
        if user_to_project is None:
            if instance.admin.user != user:
                return
            return RoleProjectSerializer(get_admin_project()).data
        return RoleProjectSerializer(user_to_project.role).data


class PreviewProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'image']


class ProjectUpdateSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'admin', 'image']

    def update(self, instance, validated_data):
        instance.admin = validated_data.get('admin', instance.admin)
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance


# ==============================
#       РЈР§РђРЎРўРќРРљР РџР РћР•РљРўРђ
# ==============================
class UserToProjectSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = RoleProjectSerializer()

    class Meta:
        model = UserToProject
        fields = ['id', 'user', 'project', 'role', 'created_at']


# ==============================
#       СЕКЦИИ У ПРОЕКТОВ
# ==============================
class SectionProjectSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    color_value = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = SectionProject
        fields = ['id', 'name', 'position', 'color', 'color_value', 'is_final']

    def create(self, validated_data):
        color_value = validated_data.pop('color_value', None)
        if color_value:
            color, _ = Color.objects.get_or_create(
                value=color_value,
                defaults={'name': color_value},
            )
            validated_data['color'] = color
        return super().create(validated_data)


class PreviewSectionProjectSerializer(serializers.ModelSerializer):
    color = ColorSerializer()

    class Meta:
        model = SectionProject
        fields = ['id', 'name', 'position', 'color', 'is_final']


# ========================
#    Задача в списке
# ========================
class TaskForSectionProjectSerializer(serializers.ModelSerializer):
    director = PreviewUserSerializer()
    responsible = serializers.SerializerMethodField()
    project = PreviewProjectSerializer()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'name', 'code', 'deadline', 'completed_at', 'director', 'responsible', 'project', 'category']

    @staticmethod
    def get_responsible(instance):
        user_to_task = UserToTask.objects.filter(task=instance, level=get_responsible_task()).first()
        if user_to_task is None:
            return None
        return PreviewUserSerializer(user_to_task.user).data

    @staticmethod
    def get_category(instance):
        if instance.category is None:
            return None
        return {
            'id': instance.category.id,
            'project': instance.category.project_id,
            'name': instance.category.name,
            'color': instance.category.color,
            'created_at': instance.category.created_at,
        }


class SectionProjectWithTaskSerializer(serializers.ModelSerializer):
    body = serializers.SerializerMethodField()
    color = ColorSerializer()

    class Meta:
        model = SectionProject
        fields = '__all__'

    def get_body(self, instance):
        tasks = [
            task_to_section.task
            for task_to_section in TaskToSection.objects.filter(section_project=instance).order_by('position', 'created_at')
        ]
        return TaskForSectionProjectSerializer(tasks, many=True).data


class SectionProjectUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    position = serializers.IntegerField(required=False)
    is_final = serializers.BooleanField(required=False)

    class Meta:
        model = SectionProject
        fields = ['id', 'name', 'position', 'is_final']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.position = validated_data.get('position', instance.position)
        instance.is_final = validated_data.get('is_final', instance.is_final)

        instance.save()
        return instance
