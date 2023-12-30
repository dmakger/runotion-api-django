from django.shortcuts import get_object_or_404
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import UserProfile
from user.serializers import UserSerializer


# ПОЛУЧЕНИЕ ПОЛЬЗОВАТЕЛЯ

class GetUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)

        serializer = UserSerializer(profile)
        return Response(serializer.data)
