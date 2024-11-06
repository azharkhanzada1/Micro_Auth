from django.urls import path
from .views import TokenValidationView, PermissionCheckingView

urlpatterns = [
    path('validate-token/', TokenValidationView.as_view(), name='validate-token'),
    path('check-permission/', PermissionCheckingView.as_view(), name='check-permission'),
]
