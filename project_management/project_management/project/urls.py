from django.urls import path

from project_management.project import views


urlpatterns = [
    path('projects/', views.ProjectListViewSet.as_view(), name='project'),
    path('projects/<int:pk>/', views.ProjectDetailUpdateDeleteView.as_view(), name='project_detail_update_delete'),
    # Task Urls
    path('tasks/', views.TaskListViewSet.as_view(), name='task'),
    path('tasks/<int:pk>/', views.TaskDetailUpdateDeleteView.as_view(), name='task_detail_update_delete'),
]