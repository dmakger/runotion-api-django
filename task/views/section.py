from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project.models import SectionProject
from project.serializers import SectionProjectSerializer
from task.models import TaskToSection
from task.serializers import TaskSerializer


class SectionProjectDetailAPIView(RetrieveAPIView):
    queryset = SectionProject.objects.all()
    serializer_class = SectionProjectSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        section = self.get_object()
        tasks = TaskToSection.objects.filter(section_project=section)
        serializer = TaskSerializer(tasks, many=True)
        print(response.data)
        return Response(serializer.data)
