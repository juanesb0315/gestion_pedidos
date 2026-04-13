import base64
import hashlib
import hmac
import json
import time

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# codifica bytes a base64 url sin relleno
def _b64url_encode(data: bytes) -> str:
    """Codifica bytes a base64 URL-safe sin rellenos."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


# decodifica texto base64 url con padding
def _b64url_decode(data: str) -> bytes:
    """Decodifica una cadena base64 URL-safe agregando padding si es necesario."""
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


# crea token jwt firmado con hs256
def create_jwt_token(user, expires_in=15):
    """Crea un JWT simple con HS256, exp y algunos claims básicos."""
    header = {'alg': 'HS256', 'typ': 'JWT'}
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': int(time.time()) + expires_in,
    }

    header_b64 = _b64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    payload_b64 = _b64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))

    signature = hmac.new(
        settings.SECRET_KEY.encode('utf-8'),
        f'{header_b64}.{payload_b64}'.encode('utf-8'),
        hashlib.sha256,
    ).digest()

    signature_b64 = _b64url_encode(signature)
    return f'{header_b64}.{payload_b64}.{signature_b64}'


# valida token jwt y retorna usuario
def verify_jwt_token(token):
    """Verifica el formato, firma, expiración y devuelve el usuario si todo está OK."""
    if not token or token.count('.') != 2:
        return None

    header_b64, payload_b64, signature_b64 = token.split('.')

    try:
        json.loads(_b64url_decode(header_b64))
        payload_raw = json.loads(_b64url_decode(payload_b64))
    except Exception:
        return None

    expected_signature = _b64url_encode(
        hmac.new(
            settings.SECRET_KEY.encode('utf-8'),
            f'{header_b64}.{payload_b64}'.encode('utf-8'),
            hashlib.sha256,
        ).digest()
    )

    if not hmac.compare_digest(expected_signature, signature_b64):
        return None

    exp = payload_raw.get('exp')
    if not isinstance(exp, int) or exp < int(time.time()):
        return None

    user_id = payload_raw.get('user_id')
    if not user_id:
        return None

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


# gestiona inicio de sesion con jwt
def login_view(request):
    """Muestra y procesa el formulario de inicio de sesión.

    - Valida usuario / contraseña.
    - Crea sesión con login(request, user).
    - Genera JWT y pone cookie httponly.
    - Redirige a listar o next.
    """
    next_url = request.GET.get('next', None)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            context = {'error': 'Ingrese usuario y contraseña.'}
            if next_url:
                context['next'] = next_url
            return render(request, 'pedidos/login.html', context)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # No usamos sesión de Django para login; solo JWT.
            jwt_token = create_jwt_token(user)

            redirect_to = next_url or 'listar'
            response = redirect(redirect_to)
            response.set_cookie(
                'jwt_token',
                jwt_token,
                httponly=True,
                samesite='Lax',
                max_age=3600,
            )
            return response

        context = {'error': 'Credenciales inválidas'}
        if next_url:
            context['next'] = next_url
        return render(request, 'pedidos/login.html', context)

    context = {}
    if next_url:
        context['next'] = next_url
    return render(request, 'pedidos/login.html', context)


# cierra sesion y limpia cookie jwt
def logout_view(request):
    """Limpiar autenticación y cookie JWT."""
    # Mantener logout(request) para limpiar posibles datos de sesión anteriores.
    logout(request)
    response = redirect('login')
    response.delete_cookie('jwt_token')
    return response


# registra un nuevo usuario del sistema
def register_view(request):
    """Formulario simple de registro de usuario con validaciones básicas."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        errors = []

        # validaciones simples recomendadas
        if not username or len(username) < 3:
            errors.append('El nombre de usuario debe tener al menos 3 caracteres.')
        if not email or '@' not in email:
            errors.append('Ingrese un email válido.')
        if not password or len(password) < 6:
            errors.append('La contraseña debe tener al menos 6 caracteres.')
        if password != confirm_password:
            errors.append('Las contraseñas no coinciden.')

        # comprobación de unicidad en DB
        UserModel = get_user_model()
        if UserModel.objects.filter(username=username).exists():
            errors.append('El usuario ya existe.')
        if UserModel.objects.filter(email=email).exists():
            errors.append('El email ya está registrado.')

        if errors:
            return render(request, 'pedidos/register.html', {
                'errors': errors,
                'username': username,
                'email': email,
            })

        # creación segura usando create_user (hash de contraseña)
        user = UserModel.objects.create_user(username=username, email=email, password=password)
        user.save()

        # envío a login para acceso inmediato
        return redirect('login')

    return render(request, 'pedidos/register.html')


# redirige segun estado de autenticacion
def home_view(request):
    """Redirige al usuario.

    - si está autenticado, va a la lista de pedidos
    - si no, va a login
    """
    if request.user.is_authenticated:
        return redirect('listar')
    return redirect('login')
