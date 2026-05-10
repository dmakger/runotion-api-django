from rest_framework import serializers

from user.models import UserProfile, Department


class PreviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'image']


class UserSerializer(serializers.ModelSerializer):
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
