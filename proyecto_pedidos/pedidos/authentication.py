from rest_framework import authentication, exceptions

from .views.auth import verify_jwt_token


# autenticacion jwt para endpoints de la api
class JWTAuthentication(authentication.BaseAuthentication):
    """Autenticacion JWT por header Bearer o cookie jwt_token."""

    # obtiene usuario desde bearer o cookie
    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).decode('utf-8')
        token = None
        token_desde_header = False

        if auth_header.startswith('Bearer '):
            token = auth_header[7:].strip()
            token_desde_header = True

        if not token:
            token = request.COOKIES.get('jwt_token')

        if not token:
            return None

        user = verify_jwt_token(token)
        if user is None:
            # Si el token viene en Authorization Bearer, reportamos error.
            # Si viene por cookie y es invalido, lo ignoramos para no bloquear
            # endpoints publicos de solo lectura.
            if token_desde_header:
                raise exceptions.AuthenticationFailed('Token JWT invalido o expirado.')
            return None

        return (user, None)
