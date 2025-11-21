from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from firebase_admin import firestore
def register(request):
    return render(request, 'comuni/register.html')

def login(request):
    return render(request, 'comuni/login.html')

def register_view(request):
    if request.method == 'POST':
        # Usa tu formulario personalizado
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Registro exitoso! Bienvenido.")
            return redirect('home')
        else:
            # Si hay errores (ej. usuario ya existe), se mostrarán
            messages.error(request, "Hubo un error en el registro. Revisa los campos.")
    else:
        # Muestra un formulario vacío
        form = CustomUserCreationForm() 
        
    # Pasa el formulario (ya sea vacío o con errores) a la plantilla
    return render(request, 'comuni/register.html', {'form': form})

@login_required  # <-- Este es el "guardia de seguridad"
def perfil_view(request):
    # Gracias a @login_required, podemos estar 100% seguros
    # de que request.user es el usuario que ha iniciado sesión.

    # Simplemente renderizamos una plantilla.
    # Django pasa automáticamente el objeto 'user' a la plantilla.
    return render(request, 'users/perfil.html')

def prueba_token_view(request):
    """
    Esta vista prueba si el middleware de Firebase creó una sesión válida.
    El middleware lee el token del header 'Authorization'.
    """

    # user.is_authenticated será True si el middleware hizo su trabajo.
    if request.user.is_authenticated:
        return JsonResponse({
            'status': 'success',
            'message': '¡Autenticación con Firebase exitosa!',
            'django_user': request.user.username,
            'email': request.user.email,
            'uid_firebase': request.user.username, # Recuerda que usamos el UID como username
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'No se encontró un token válido o el usuario no está autenticado.',
        }, status=401) # Código 401: No autorizado
    
    from django.shortcuts import render

def status_view(request):
    """Muestra el estado de autenticación de Django."""
    context = {
        'is_logged_in': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else 'Invitado'
    }
    return render(request, 'comuni/status.html', context)

db = firestore.client()
@login_required
def editar_perfil_firebase(request):
    # Usamos el UID de Firebase como identificador (guardado en username)
    uid = request.user.username
    user_doc_ref = db.collection('users').document(uid)

    if request.method == 'POST':
        # --- LÓGICA DE GUARDADO NO DESTRUCTIVA ---
        datos_a_actualizar = {}
        
        # Lista de campos que esperamos del formulario
        campos_posibles = ['riot_id', 'rango', 'region', 'servidor', 'bio']
        
        for campo in campos_posibles:
            valor = request.POST.get(campo)
            # Solo guardamos si el valor no está vacío
            if valor and valor.strip() != "":
                datos_a_actualizar[campo] = valor

        if datos_a_actualizar:
            # merge=True es la clave: actualiza sin borrar lo que no envíes
            user_doc_ref.set(datos_a_actualizar, merge=True)
            messages.success(request, '¡Perfil actualizado correctamente!')
        
        return redirect('home') 

    else:
        # --- CARGAR DATOS PARA MOSTRAR ---
        doc = user_doc_ref.get()
        user_data = doc.to_dict() if doc.exists else {}

    context = {
        'user_data': user_data,
        'rangos': [
            'Unranked', 'Hierro', 'Bronce', 'Plata', 'Oro', 
            'Platino', 'Diamante', 'Ascendente', 'Inmortal', 'Radiante'
        ],
        'regiones': ['NA', 'LATAM', 'BR', 'EU', 'KR', 'AP'],
    }
    
    # Nota la ruta: 'comuni/profile_edit.html'
    return render(request, 'comuni/profile_edit.html', context)


@login_required
def ver_perfil(request):
    # 1. Obtenemos el UID
    uid = request.user.username 
    
    # 2. Leemos de Firestore
    user_doc_ref = db.collection('users').document(uid)
    doc = user_doc_ref.get()
    
    # 3. Preparamos los datos
    if doc.exists:
        user_data = doc.to_dict()
    else:
        user_data = {} # Perfil vacío

    context = {
        'user_data': user_data,
    }
    
    return render(request, 'comuni/perfil.html', context)