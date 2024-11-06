from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import BasePermission

class TokenValidationView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get('token')

        try:
            # Validate the token
            validated_token = AccessToken(token)
            return Response({'valid': True, 'token': str(validated_token)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'valid': False, 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

class CustomPermission(BasePermission):
    """
    Custom permission class to check user roles and specific resource access.
    """

    def has_permission(self, request, view):
        # Allow all admin users
        if request.user.role == 'admin':
            return True
        
        # Allow access to user-specific resources for regular users
        if request.user.role == 'user':
            # Check if the request is trying to access user-specific resources
            return view.action in ['retrieve', 'update', 'destroy']  # Adjust actions as needed
        
        return False

class PermissionCheckingView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, CustomPermission]

    def get(self, request):
        return Response({'message': 'You have permission to access this resource.'}, status=status.HTTP_200_OK)
