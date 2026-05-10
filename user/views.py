from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from service.pagination import Pagination
from user.models import UserProfile
from user.serializers import UserSerializer


# ПОЛУЧЕНИЕ ПОЛЬЗОВАТЕЛЯ

class GetUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)

        serializer = UserSerializer(profile)
        return Response(serializer.data)


class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.query_params.get('search', '').strip()
        profiles = UserProfile.objects.select_related('user', 'department').order_by('name', 'user__username')
        if search:
            profiles = profiles.filter(
                Q(name__icontains=search) |
                Q(user__username__icontains=search) |
                Q(department__name__icontains=search)
            )

        result = Pagination(request=request, queryset=profiles).get()
        result['results'] = UserSerializer(result.get('results'), many=True).data
        return Response(result)
