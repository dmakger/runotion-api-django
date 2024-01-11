from rest_framework import serializers

from core.serializers import ImportanceLevelSerializer
from project.models import Project, SectionProject, UserToProject, RoleProject
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
        qs = UserToProject.objects.filter(user=user, project=instance)
        if len(qs) == 0:
            return
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
