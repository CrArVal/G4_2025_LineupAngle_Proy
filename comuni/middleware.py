

import firebase_admin
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from django.contrib.auth import login, get_user_model
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import os # Necesario para manejar rutas

# Obtenemos el modelo de usuario de Django
User = get_user_model()

# -------------------------------------------------------------------
# LÓGICA DE INICIALIZACIÓN DE FIREBASE ADMIN SDK
# -------------------------------------------------------------------
# Usaremos una verificación simple para asegurar que el SDK Admin se inicie
if not firebase_admin._apps:
    try:
        # Asegúrate de que settings.FIREBASE_CERTIFICATE_PATH esté definido
        cert_path = settings.FIREBASE_CERTIFICATE_PATH 
        
        cred = firebase_admin.credentials.Certificate(cert_path)
        firebase_admin.initialize_app(cred)
        print("INFO: Firebase Admin SDK inicializado en comuni/middleware.")
    except Exception as e:
        print(f"ERROR: No se pudo inicializar Firebase Admin SDK. Detalle: {e}")
        
class FirebaseAuthenticationMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        # 1. Obtener el token de la cookie
        id_token = request.COOKIES.get('firebaseToken')
        
        if not id_token:
            return None # No hay token, continúa el flujo normal

        try:
            # 2. Verificar el token con Google
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            
            # ⭐️ LECTURA DEL NOMBRE: Leemos el nombre que el usuario estableció ('displayName') ⭐️
            display_name = decoded_token.get('name') 
            
            # 3. Buscar o crear el usuario de Django
            user, created = User.objects.get_or_create(
                username=uid, # El UID de Firebase es la clave única en Django
                defaults={
                    'email': email, 
                    'is_active': True,
                    'first_name': display_name if display_name else '', # ⭐️ Usamos display_name aquí ⭐️
                }
            )
            
            # 4. Actualizar campos si el usuario ya existía (solo email o nombre si está vacío)
            if not created:
                needs_save = False
                if user.email != email:
                    user.email = email
                    needs_save = True
                
                # Si el usuario no tiene nombre y el token sí lo trae, lo asignamos
                if not user.first_name and display_name:
                    user.first_name = display_name
                    needs_save = True
                
                if needs_save:
                    user.save()
            
            # 5. Iniciar la sesión de Django (CRÍTICO)
            if user:
                login(request, user)
            
        except FirebaseError as e:
            # Token expiró o es inválido. El usuario necesitará iniciar sesión de nuevo.
            print(f"Error de verificación de token de Firebase: {e}")
            
            # Devolvemos None para que el flujo continúe, y luego usaremos process_response
            # para borrar la cookie si es necesario (ver nota abajo).
            return None
            
        except Exception as e:
            print(f"Error desconocido en el middleware (Comuni): {e}")
            return None 
            
        return None # Continúa el procesamiento normal de la solicitud

    # 🚨 process_response para borrar la cookie si hay un error de Firebase 🚨
    def process_response(self, request, response):
        # Esta es la forma correcta de borrar la cookie, fuera del try/except
        if request.user.is_authenticated:
            # Si el usuario está autenticado, la cookie es válida, no hacemos nada.
            return response
        
        # Si el usuario NO está autenticado pero la cookie existe (indica un token expirado/inválido), la borramos
        if request.COOKIES.get('firebaseToken'):
            response.delete_cookie('firebaseToken')
            # Opcional: Redirigir al login si el token expiró en una página protegida
        
        return response