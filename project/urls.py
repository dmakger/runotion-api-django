from django.urls import path, include
from rest_framework.routers import DefaultRouter

from project.views.project import ProjectView, ProjectUpdateAPIView, ProjectDeleteAPIView
from project.views.section import SectionProjectListView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    #  Проекты
    path("all/", ProjectView.as_view({'get': 'get_projects'})),
    path("create/", ProjectView.as_view({'post': 'create_project'})),
    path("<int:pk>/update/", ProjectUpdateAPIView.as_view()),
    path("<int:pk>/delete/", ProjectDeleteAPIView.as_view()),

    #  Секции по проектам
    path("<int:project_pk>/section/all/", SectionProjectListView.as_view()),
]
