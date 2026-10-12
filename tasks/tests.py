from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task


class TaskProTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', password='pass12345')
        self.other = User.objects.create_user('bob', password='pass12345')
        res = self.client.post(reverse('login'), {'username': 'alice', 'password': 'pass12345'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])
        Task.objects.create(owner=self.user, title='Later', due_date='2026-12-20', priority='low')
        Task.objects.create(owner=self.user, title='Soon', due_date='2026-11-01', priority='high', status='completed')
        Task.objects.create(owner=self.other, title='Not mine', due_date='2026-11-01')

    def test_register(self):
        res = self.client.post(reverse('register'), {'username': 'new', 'password': 'secret123'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_auth_required(self):
        self.client.credentials()
        self.assertEqual(self.client.get(reverse('task-list')).status_code, 401)

    def test_only_own_tasks_sorted_by_due_date(self):
        res = self.client.get(reverse('task-list'))
        self.assertEqual([t['title'] for t in res.data], ['Soon', 'Later'])

    def test_filter_status_priority_search(self):
        url = reverse('task-list')
        self.assertEqual(len(self.client.get(url, {'status': 'completed'}).data), 1)
        self.assertEqual(len(self.client.get(url, {'priority': 'low'}).data), 1)
        self.assertEqual(len(self.client.get(url, {'search': 'soo'}).data), 1)

    def test_create_edit_complete_delete(self):
        data = {'title': 'New', 'description': '', 'due_date': '2026-12-01', 'priority': 'medium', 'status': 'pending'}
        res = self.client.post(reverse('task-list'), data)
        self.assertEqual(res.status_code, 201)
        url = reverse('task-detail', args=[res.data['id']])
        self.assertEqual(self.client.put(url, {**data, 'title': 'Edited'}).status_code, 200)
        self.client.patch(url, {'status': 'completed'})
        self.assertEqual(Task.objects.get(pk=res.data['id']).status, 'completed')
        self.assertEqual(self.client.delete(url).status_code, 204)

    def test_validation_error(self):
        res = self.client.post(reverse('task-list'), {'title': ' ', 'due_date': '2026-12-01'})
        self.assertEqual(res.status_code, 400)
