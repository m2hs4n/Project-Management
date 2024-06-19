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


# Task View
# List all tasks
class TaskListViewSet(generics.ListAPIView, generics.CreateAPIView):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskSerializer
        elif self.request.method == 'POST':
            return TaskCreateSerializer
        else:
            raise exceptions.MethodNotAllowed


# detail, delete, update with partial
class TaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        # Set partial=True to allow partial updates
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)