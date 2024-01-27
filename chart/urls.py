from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chart.views import NumberOfRejectedTasksChartView, TaskByQuarterChartView, TaskToPerformersChartView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    #  Задачи
    path("number_of_rejected_tasks/", NumberOfRejectedTasksChartView.as_view({'post': 'get_chart'})),
    path("task_by_quarter/", TaskByQuarterChartView.as_view({'post': 'get_chart'})),
    path("task_to_performers/", TaskToPerformersChartView.as_view({'post': 'get_chart'})),
]
