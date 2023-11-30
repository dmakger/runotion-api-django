from rest_framework import serializers

from project.models import Project, SectionProject
from user.models import UserProfile
from user.serializers import PreviewUserSerializer


# ====================
#       ПРОЕКТЫ
# ====================

class ProjectSerializer(serializers.ModelSerializer):
    admin = PreviewUserSerializer()

    class Meta:
        model = Project
        fields = ['id', 'name', 'code', 'admin', 'image']


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
