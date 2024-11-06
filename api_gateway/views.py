import requests
import logging
from django.conf import settings
from django.http import JsonResponse
from django.views import View

# Logging setup
logger = logging.getLogger(__name__)

class GatewayView(View):
    def dispatch(self, request, *args, **kwargs):
        # Extract JWT token from the request header
        token = request.META.get('HTTP_AUTHORIZATION')

        # Validate JWT token (Authorization Service ke liye request send karte hain)
        try:
            auth_response = requests.get(
                f'{settings.AUTHORIZATION_SERVICE_URL}/validate/', 
                headers={'Authorization': token}
            )
            auth_response.raise_for_status()  # Raise an error for bad responses
        except requests.exceptions.HTTPError as err:
            logger.error(f'Authorization failed: {err}')
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        except Exception as e:
            logger.error(f'Error validating token: {e}')
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

        # Route the request to the appropriate service based on the path
        if request.path.startswith('/api/users/'):
            try:
                response = requests.request(
                    request.method,
                    f'{settings.USER_SERVICE_URL}{request.path}',
                    headers={**request.headers, 'Authorization': token},  # Include the token in headers
                    json=request.body
                )
                response.raise_for_status()  # Raise an error for bad responses
                return JsonResponse(response.json(), status=response.status_code)
            except requests.exceptions.HTTPError as err:
                logger.error(f'Error communicating with User Service: {err}')
                return JsonResponse({'error': 'User Service error'}, status=response.status_code)
            except Exception as e:
                logger.error(f'Error: {e}')
                return JsonResponse({'error': 'Internal Server Error'}, status=500)

        logger.warning(f'Path not found: {request.path}')
        return JsonResponse({'error': 'Not found'}, status=404)
