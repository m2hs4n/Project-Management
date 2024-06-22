from django.urls import reverse
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase
from project_management.project.models import Project, Task, Comment

class ProjectTests(APITestCase):
    def setUp(self):
        self.project1 = Project.objects.create(name='Project 1', description='Description 1')
        self.project2 = Project.objects.create(name='Project 2', description='Description 2')

    def test_list_projects(self):
        url = reverse('project')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_project(self):
        url = reverse('project')
        data = {'name': 'Project 3', 'description': 'Description 3'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 3)
        self.assertEqual(Project.objects.last().name, 'Project 3')

    def test_create_project_invalid(self):
        url = reverse('project')
        data = {'name': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_project(self):
        url = reverse('project_detail_update_delete', args=[self.project1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Project 1')

    def test_update_project(self):
        url = reverse('project_detail_update_delete', args=[self.project1.pk])
        data = {'name': 'Updated Project 1', 'description': 'Updated Description 1'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.name, 'Updated Project 1')

    def test_partial_update_project(self):
        url = reverse('project_detail_update_delete', args=[self.project1.pk])
        data = {'name': 'Partially Updated Project 1'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.name, 'Partially Updated Project 1')

    def test_delete_project(self):
        url = reverse('project_detail_update_delete', args=[self.project1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 1)

    def test_cache_invalidation_on_create(self):
        url = reverse('project')
        data = {'name': 'Project 3', 'description': 'Description 3'}
        self.client.post(url, data, format='json')
        self.assertIsNone(cache.get('project_list'))

class TaskTests(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(name='Project', description='Description')
        self.task1 = Task.objects.create(title='Task 1', project=self.project, status=Task.Status.PENDING, due_date='2024-06-30')
        self.task2 = Task.objects.create(title='Task 2', project=self.project, status=Task.Status.APPROVED, due_date='2024-07-01')

    def test_list_tasks(self):
        url = reverse('task')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_task(self):
        url = reverse('task')
        data = {'title': 'Task 3', 'project': self.project.id, 'status': Task.Status.PENDING, 'due_date': '2024-07-02'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(Task.objects.last().title, 'Task 3')

    def test_create_task_invalid(self):
        url = reverse('task')
        data = {'title': '', 'project': self.project.id, 'status': Task.Status.PENDING, 'due_date': '2024-07-02'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_task(self):
        url = reverse('task_detail_update_delete', args=[self.task1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Task 1')

    def test_update_task(self):
        url = reverse('task_detail_update_delete', args=[self.task1.pk])
        data = {'title': 'Updated Task 1', 'status': Task.Status.APPROVED, 'due_date': '2024-07-03'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task 1')
        self.assertEqual(self.task1.status, Task.Status.APPROVED)

    def test_partial_update_task(self):
        url = reverse('task_detail_update_delete', args=[self.task1.pk])
        data = {'title': 'Partially Updated Task 1'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Partially Updated Task 1')

    def test_delete_task(self):
        url = reverse('task_detail_update_delete', args=[self.task1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)

    def test_cache_invalidation_on_create(self):
        url = reverse('task')
        data = {'title': 'Task 3', 'project': self.project.id, 'status': Task.Status.PENDING, 'due_date': '2024-07-02'}
        self.client.post(url, data, format='json')
        self.assertIsNone(cache.get('task_list'))

class CommentTests(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(name='Project', description='Description')
        self.task = Task.objects.create(title='Task', project=self.project, status=Task.Status.PENDING, due_date='2024-06-30')
        self.comment1 = Comment.objects.create(task=self.task, author='Author 1', content='Comment 1')
        self.comment2 = Comment.objects.create(task=self.task, author='Author 2', content='Comment 2')

    def test_list_comments(self):
        url = reverse('task_comments', args=[self.task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_comment(self):
        url = reverse('task_comments', args=[self.task.pk])
        data = {'author': 'Author 3', 'content': 'Comment 3'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 3)
        self.assertEqual(Comment.objects.last().content, 'Comment 3')
        self.assertEqual(Comment.objects.last().task, self.task)

    def test_create_comment_invalid(self):
        url = reverse('task_comments', args=[self.task.pk])
        data = {'author': '', 'content': 'Comment 3'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cache_invalidation_on_create(self):
        url = reverse('task_comments', args=[self.task.pk])
        data = {'author': 'Author 3', 'content': 'Comment 3'}
        self.client.post(url, data, format='json')
        self.assertIsNone(cache.get(f'comment_list_{self.task.pk}'))
