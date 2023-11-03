from rest_framework import serializers

from project.serializers import PreviewProjectSerializer
from task.models import Task, UserToTask
from task.service import get_responsible_task, get_collaborator_task, get_observer_task
from user.serializers import PreviewUserSerializer


# ========================
#    Задача в списке
# ========================
class TaskSerializer(serializers.ModelSerializer):
    director = PreviewUserSerializer()
    responsible = serializers.SerializerMethodField()
    project = PreviewProjectSerializer()

    class Meta:
        model = Task
        fields = ['id', 'name', 'deadline', 'director', 'responsible', 'project']

    @staticmethod
    def get_responsible(instance):
        user_to_task = UserToTask.objects.filter(task=instance, position=get_responsible_task())
        if len(user_to_task) == 0:
            return None
        return PreviewUserSerializer(user_to_task[0].user).data


# ========================
#    Детальная Задача
# ========================
class DetailTaskSerializer(serializers.ModelSerializer):
    director = PreviewUserSerializer()
    responsible = serializers.SerializerMethodField()
    collaborators = serializers.SerializerMethodField()
    observers = serializers.SerializerMethodField()
    project = PreviewProjectSerializer()

    class Meta:
        model = Task
        fields = ['id', 'name', 'code', 'deadline', 'director', 'responsible', 'collaborators', 'observers', 'project']

    @staticmethod
    def get_responsible(instance):
        user_to_task = UserToTask.objects.filter(task=instance, position=get_responsible_task())
        if len(user_to_task) == 0:
            return None
        return PreviewUserSerializer(user_to_task[0].user).data

    @staticmethod
    def get_collaborators(instance):
        user_to_task = UserToTask.objects.filter(task=instance, position=get_collaborator_task())
        if len(user_to_task) == 0:
            return None
        users = [user.user for user in user_to_task]
        return PreviewUserSerializer(users, many=True).data

    @staticmethod
    def get_observers(instance):
        user_to_task = UserToTask.objects.filter(task=instance, position=get_observer_task())
        if len(user_to_task) == 0:
            return None
        users = [user.user for user in user_to_task]
        return PreviewUserSerializer(users, many=True).data
