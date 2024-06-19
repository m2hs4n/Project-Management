from rest_framework import serializers

from project_management.project.models import Project, Task


# Project Serializers
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
        ]


# Task Serializer
# List tasks serializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


# Detail, delete, update serializer
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'project',
            'title',
            'status',
            'due_date',
        ]
