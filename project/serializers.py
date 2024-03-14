from rest_framework import serializers

from core.serializers import ImportanceLevelSerializer, ColorSerializer
from project.models import Project, SectionProject, UserToProject, RoleProject
from project.service import get_admin_project
from task.models import TaskToSection, Task, UserToTask
from task.service import get_responsible_task
from user.models import UserProfile
from user.serializers import PreviewUserSerializer


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
        if len(qs) == 0:
            if instance.admin.user != user:
                return
            return RoleProjectSerializer(get_admin_project()).data
        return RoleProjectSerializer(qs[0].role).data


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
#       СЕКЦИИ У ПРОЕКТОВ
# ==============================
class SectionProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionProject
        fields = ['id', 'name', 'position']


# ========================
#    Задача в списке
# ========================
class TaskForSectionProjectSerializer(serializers.ModelSerializer):
    director = PreviewUserSerializer()
    responsible = serializers.SerializerMethodField()
    project = PreviewProjectSerializer()

    class Meta:
        model = Task
        fields = ['id', 'name', 'code', 'deadline', 'director', 'responsible', 'project']

    @staticmethod
    def get_responsible(instance):
        user_to_task = UserToTask.objects.filter(task=instance, level=get_responsible_task())
        if len(user_to_task) == 0:
            return None
        return PreviewUserSerializer(user_to_task[0].user).data


class SectionProjectWithTaskSerializer(serializers.ModelSerializer):
    body = serializers.SerializerMethodField()
    color = ColorSerializer()

    class Meta:
        model = SectionProject
        fields = '__all__'

    def get_body(self, instance):
        tasksToSection = TaskToSection.objects.filter(section_project=instance)
        tasks = []
        for task in tasksToSection:
            tasks.append(task.task)
        serializer = TaskForSectionProjectSerializer(data=tasks, many=True)
        serializer.is_valid()
        return serializer.data


class SectionProjectUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    position = serializers.IntegerField(required=False)

    class Meta:
        model = SectionProject
        fields = ['id', 'name', 'position']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.position = validated_data.get('position', instance.position)

        instance.save()
        return instance
