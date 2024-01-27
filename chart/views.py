from django.db import models
from django.db.models import Count, Case, When
from django.db.models import QuerySet
from django.db.models.functions import ExtractYear
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from chart.core.service import get_projects, get_tasks
from service import difference
from service.difference import get_all_keys
from task.models import Task, UserToTask


# Количество  задач с отклонением
class NumberOfRejectedTasksChartView(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    @staticmethod
    def sort_by_deadline(tasks: QuerySet):
        result = get_all_keys()
        for task in tasks:
            key = difference.calculate_days(completed_at=task.completed_at, deadline_at=task.deadline)
            result[key] = result.get(key, 0) + 1
        return result

    @action(methods=['post'], detail=False)
    def get_chart(self, request):
        projects = get_projects(request)
        tasks = get_tasks(projects, request)
        serializer_data = self.sort_by_deadline(tasks)
        return Response(serializer_data, status=status.HTTP_200_OK)


# Количество cозданных задач по кварталам
class TaskByQuarterChartView(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    @staticmethod
    def serialize(tasks: QuerySet):
        data = []
        for task in tasks.order_by('created_at'):
            year = task.created_at.year
            quarter = -(-task.created_at.month // 3)
            if len(data) == 0 or data[-1]['year'] != year or data[-1]['quarter'] != quarter:
                data.append({
                    'year': year,
                    'quarter': quarter,
                    'amount': 1
                })
            else:
                data[-1]['amount'] = data[-1]['amount'] + 1
        return data

    @action(methods=['post'], detail=False)
    def get_chart(self, request):
        projects = get_projects(request)
        tasks = get_tasks(projects, request)
        serializer_data = self.serialize(tasks)
        return Response(serializer_data, status=status.HTTP_200_OK)


# Количество задач к исполнителям
class TaskToPerformersChartView(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    @staticmethod
    def serialize(tasks: QuerySet):
        data = {}
        for task in tasks:
            username = task.director.name
            data[username] = data.get(username, 0) + 1
        user_to_tasks_queries = [UserToTask.objects.filter(task=task) for task in tasks]

        # Объединяем результаты в один QuerySet
        user_to_tasks = user_to_tasks_queries[0].union(*user_to_tasks_queries[1:])
        for task in user_to_tasks:
            username = task.user.name
            data[username] = data.get(username, 0) + 1
        return data

    @action(methods=['post'], detail=False)
    def get_chart(self, request):
        projects = get_projects(request)
        tasks = get_tasks(projects, request)
        serializer_data = self.serialize(tasks)
        return Response(serializer_data, status=status.HTTP_200_OK)
