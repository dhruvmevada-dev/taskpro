from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import DashboardPage, LoginPage, RegisterView, TaskViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', LoginPage.as_view(), name='login-page'),
    path('dashboard/', DashboardPage.as_view(), name='dashboard-page'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/', include(router.urls)),
]
