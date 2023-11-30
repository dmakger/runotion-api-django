from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chart.views import NumberOfRejectedTasksChartView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    #  Проекты
    path("number_of_rejected_tasks/", NumberOfRejectedTasksChartView.as_view({'get': 'get_chart'}))
]
