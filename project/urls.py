from django.urls import path, include
from rest_framework.routers import DefaultRouter

from project.views import ProjectView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    # Все проекты
    path("all/", ProjectView.as_view({'get': 'get_my_projects'})),
]
