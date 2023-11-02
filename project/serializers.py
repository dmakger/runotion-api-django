from rest_framework import serializers

from project.models import Project, UserToProject
from project.service import get_admin_project
from user.serializers import PreviewUserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'admin']

    @staticmethod
    def get_admin(instance):
        user_to_project = UserToProject.objects.filter(project=instance, role=get_admin_project())
        if len(user_to_project) == 0:
            return None
        return PreviewUserSerializer(user_to_project[0].user).data
