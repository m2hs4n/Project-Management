from rest_framework import generics, exceptions

from project_management.project.models import Project, Task
from project_management.project.serializers import ProjectSerializer, ProjectCreateSerializer, TaskSerializer, TaskCreateSerializer


# Project Views
class ProjectListViewSet(generics.ListAPIView, generics.CreateAPIView):
    queryset = Project.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectSerializer
        elif self.request.method == 'POST':
            return ProjectCreateSerializer
        else:
            raise exceptions.NotAcceptable


class ProjectDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
