from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegisterView, UserLoginView, UserViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


# Create a router and register the UserViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # User registration and login endpoints
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Include the router URLs for user management
    path('', include(router.urls)),
]
