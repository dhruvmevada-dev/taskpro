from django.contrib.auth.models import User
from django.views.generic import TemplateView
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny

from .models import Task
from .serializers import RegisterSerializer, TaskSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        qs = Task.objects.filter(owner=self.request.user)
        params = self.request.query_params
        if params.get('status') in ('pending', 'completed'):
            qs = qs.filter(status=params['status'])
        if params.get('priority') in ('low', 'medium', 'high'):
            qs = qs.filter(priority=params['priority'])
        if params.get('search'):
            qs = qs.filter(title__icontains=params['search'])
        return qs.order_by('due_date', 'id')  # due date ascending

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LoginPage(TemplateView):
    template_name = 'login.html'


class DashboardPage(TemplateView):
    template_name = 'dashboard.html'
