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
        print('Пришли на аутентификацию')

        if request.method == 'GET' or request.method == 'DELETE':
            print('Пришел delete')
            # Если get или delete, ключ приходит в params запроса
            api_key = request.query_params.get("API_KEY_VER_G")
            print(f'api_key = {api_key}')
        elif request.method == 'POST':
            # Если метод POST, то api_key находится в теле запроса
            api_key = request.data.get("API_KEY_VER_G")
            print(api_key)
        if api_key != API_KEY_VER_G:
            raise AuthenticationFailed('Invalid API key')
        else:
            return None, None
