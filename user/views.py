from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView

from service.pagination import Pagination
from user.models import UserProfile
from user.serializers import RegistrationRequestSerializer, UserProfileDetailSerializer, UserProfileUpdateSerializer, UserSerializer


# ПОЛУЧЕНИЕ ПОЛЬЗОВАТЕЛЯ

class GetUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)

        serializer = UserSerializer(profile)
        return Response(serializer.data)


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        profile = get_object_or_404(
            UserProfile.objects.select_related('user', 'department'),
            pk=pk
        )

        serializer = UserProfileDetailSerializer(profile)
        return Response(serializer.data)


class UserUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileUpdateSerializer
    queryset = UserProfile.objects.all()

    def update(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            return Response({'detail': 'Forbidden'}, status=403)
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


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


class RegistrationRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        registration_request = serializer.save()
        return Response(
            RegistrationRequestSerializer(registration_request).data,
            status=201
        )
