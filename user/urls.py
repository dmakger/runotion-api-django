from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import GetUserAPIView, UserListAPIView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    path('get/', GetUserAPIView.as_view(), name='get_user_api'),
    path('all/', UserListAPIView.as_view(), name='all_user_api'),

]
