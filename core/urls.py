from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import ColorView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    #  COLORS
    path("colors/update/section/", ColorView.as_view({'put': 'update_colors_section_projects'})),]
