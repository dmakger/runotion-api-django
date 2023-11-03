from django.urls import path, include
from rest_framework.routers import DefaultRouter

from project.views import ProjectView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    # Все проекты
    path("all/", ProjectView.as_view({'get': 'get_projects'})),
    # Создание проекта
    path("create/", ProjectView.as_view({'post': 'create_project'})),
]
