from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import logging

logger = logging.getLogger('api')

API_KEY_VER_G = settings.API_KEY_VER_G

class VergAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = None

        logger.info(request)

        if request.method == 'GET' or request.method == 'DELETE':
            # Если get или delete, ключ приходит в params запроса
            api_key = request.query_params.get("API_KEY_VER_G")
        elif request.method == 'POST':
            # Если метод POST, то api_key находится в теле запроса
            api_key = request.data.get("API_KEY_VER_G")
        if api_key != API_KEY_VER_G:
            raise AuthenticationFailed('Invalid API key')
        else:
            return None, None
