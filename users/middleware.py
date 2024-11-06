# # middleware.py
# from django.conf import settings
# from django.core.cache import cache
# from django.http import JsonResponse
# import json

# class TokenCachingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.redis_client = settings.redis_client  # Accessing redis_client from settings

#     def __call__(self, request):
#         # Middleware logic goes here

#         # Get token from the request headers
#         token = request.META.get('HTTP_AUTHORIZATION', None)

#         if token:
#             # Check if the token is already in Redis
#             cached_token = self.redis_client.get(token)

#             if cached_token:
#                 # If token is cached, you can use it or modify the request as needed
#                 request.user = json.loads(cached_token)  # Assuming you store user info in token

#             else:
#                 # If token is not cached, you might want to process it
#                 # (For example, verify the token or store it in Redis)
#                 # Here, we can add logic to store the token for a specific duration
#                 # This is just an example. Adjust as per your needs.
#                 user_info = self.verify_token(token)  # You need to implement this method
#                 if user_info:
#                     # Cache the token for 1 hour
#                     self.redis_client.set(token, json.dumps(user_info), ex=3600)
#                     request.user = user_info
#                 else:
#                     return JsonResponse({"error": "Unauthorized"}, status=401)

#         # Call the next middleware or view
#         response = self.get_response(request)

#         return response

#     def verify_token(self, token):
#         # Implement token verification logic here
#         # This is a placeholder method; you'll need to replace it with actual logic
#         # For example, decode the token and retrieve user information
#         try:
#             # Decode the token and get user info
#             # Example: payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#             # Here, we're just returning a dummy user info for demonstration
#             return {"user_id": 1, "username": "example_user"}  # Replace this with actual decoding logic
#         except Exception as e:
#             return None

# users/middleware.py
# users/middleware.py

from django.conf import settings

class YourMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Redis client ko access karna
        self.redis_client = settings.redis_client

