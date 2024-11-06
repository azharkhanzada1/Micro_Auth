
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from authorization.views import CustomPermission
from django_ratelimit.decorators import ratelimit
from .tasks import send_welcome_email

def get_token_for_user(user):
    """Generate JWT token for a given user."""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_welcome_email.delay(user.email)  # Send welcome email using Celery
            return Response({"message": _("User registered successfully!")}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    @ratelimit(key='ip', rate='5/m', method='POST', block=True)  # Allow 5 requests per minute
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        cached_token = cache.get(f'token_{email}')
        if cached_token:
            return Response({'token': cached_token}, status=status.HTTP_200_OK)

        user = authenticate(request, username=email, password=password)
        if user is not None:
            token = get_token_for_user(user)
            cache.set(f'token_{email}', token, timeout=300)  # Cache for 5 minutes
            return Response({'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': _("Invalid email or password.")}, status=status.HTTP_401_UNAUTHORIZED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, CustomPermission]

    def get_queryset(self):
        if self.request.user.role == 'user':
            return self.queryset.filter(id=self.request.user.id)
        return self.queryset  # Admins can see all users
