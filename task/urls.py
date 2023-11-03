from django.urls import path, include
from rest_framework.routers import DefaultRouter

from task.views import TaskView, DetailTaskView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    # Все задачи
    path("all/", TaskView.as_view({'get': 'get_tasks'})),
    path("<slug:code>/", DetailTaskView.as_view({'get': 'get_detail_task'})),

]
