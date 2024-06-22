from rest_framework import generics, exceptions

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from project_management.project.models import Project, Task, Comment
from project_management.project.serializers import ProjectSerializer, ProjectCreateSerializer, TaskSerializer, \
    TaskCreateSerializer, CommentSerializer


# Project Views
class ProjectListViewSet(generics.ListAPIView, generics.CreateAPIView):
    queryset = Project.objects.all()

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectSerializer
        elif self.request.method == 'POST':
            return ProjectCreateSerializer
        else:
            raise exceptions.NotAcceptable
        
    def perform_create(self, serializer):
        project = serializer.save()
        cache.delete('project_list')  # Invalidate cache
        return project


class ProjectDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        # Set partial=True to allow partial updates
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


# Task View
# List all tasks
class TaskListViewSet(generics.ListAPIView, generics.CreateAPIView):
    queryset = Task.objects.all()

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskSerializer
        elif self.request.method == 'POST':
            return TaskCreateSerializer
        else:
            raise exceptions.MethodNotAllowed
        
    def perform_create(self, serializer):
        project = serializer.save()
        cache.delete('task_list')  # Invalidate cache
        return project


# detail, delete, update with partial
class TaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    lookup_field = 'pk'
    
    def put(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


# Comment for create and list all comment
class CommentView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # Filter comments by the task id from URL parameter
        task_id = self.kwargs.get('pk')
        return Comment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        # task instance for the comment based on URL parameter
        task_id = self.kwargs.get('pk')
        serializer.save(task_id=task_id)
        cache.delete(f'comment_list_{task_id}')