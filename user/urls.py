from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import GetUserAPIView, RegistrationRequestAPIView, UserDetailAPIView, UserListAPIView, UserUpdateAPIView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    path('get/', GetUserAPIView.as_view(), name='get_user_api'),
    path('all/', UserListAPIView.as_view(), name='all_user_api'),
    path('registration-request/', RegistrationRequestAPIView.as_view(), name='registration_request_api'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='update_user_api'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='detail_user_api'),

]
