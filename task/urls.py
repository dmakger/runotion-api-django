from django.urls import path, include
from rest_framework.routers import DefaultRouter

from task.views import TaskView, DetailTaskView, ChecklistTaskView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    # Все задачи
    path("all/", TaskView.as_view({'get': 'get_tasks'})),
    path("create/", TaskView.as_view({'post': 'create_task'})),

    # Детальная страница задачи
    path("<int:task_id>/", DetailTaskView.as_view({'get': 'get_detail_task'})),
    # Чеклист у задачи
    path("<int:task_id>/checklist/", ChecklistTaskView.as_view({'get': 'get_checklists'})),

]
