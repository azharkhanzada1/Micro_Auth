from django.urls import path
from .views import GatewayView

urlpatterns = [
    path('api/', GatewayView.as_view(), name='api_gateway'),
]
