from rest_framework import serializers

from task.models import Task


class NumberOfRejectedTasksChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'position']
