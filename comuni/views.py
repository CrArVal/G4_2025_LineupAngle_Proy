from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from firebase_admin import firestore
from django.contrib.auth.models import User
import datetime


def login(request):
    return render(request, 'comuni/login.html')

# comuni/views.py
from django.shortcuts import render, redirect

def register_view(request):
    
    if request.user.is_authenticated:
        return redirect('home') 

    
    if request.method == 'POST':
        return redirect('home')

    
    return render(request, 'comuni/register.html')

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


def ver_perfil_publico(request, username):
    # 1. BÚSQUEDA POR NOMBRE VISIBLE (first_name)
    perfil_user = User.objects.filter(first_name__iexact=username).first()

    # 2. BÚSQUEDA POR UID (Si no se encontró por nombre)
    if not perfil_user:
        # En lugar de get_object_or_404, usamos filter().first() que devuelve None si no existe
        perfil_user = User.objects.filter(username=username).first()
    
    # 3. 🚨 SI NO EXISTE EL USUARIO (CONTROL DE ERROR) 🚨
    if not perfil_user:
        # Agregamos un mensaje de error
        messages.error(request, f"El agente '{username}' no fue encontrado en la base de datos.")
        # Redirigimos al inicio (o a donde quieras)
        return redirect('home')

    # --- Si llegamos aquí, el usuario EXISTE ---
    uid_real = perfil_user.username
    
    user_doc_ref = db.collection('users').document(uid_real)
    doc = user_doc_ref.get()
    
    if doc.exists:
        user_data = doc.to_dict()
    else:
        user_data = {}

    context = {
        'perfil_user': perfil_user, 
        'user_data': user_data,     
    }
    
    return render(request, 'comuni/profile_detail.html', context)
# --- VISTA DE ACCESO RÁPIDO ("MI PERFIL") ---
def ver_perfil_propio(request):
    if request.user.is_authenticated:
        # Redirige a la vista pública usando el ID del usuario actual
        return redirect('perfil_publico', username=request.user.username)
    else:
        return redirect('login')
    
def buscar_usuario(request):
    query = request.GET.get('q') # 'q' es lo que escriben en la caja
    if query:
        # Redirige a la vista de perfil usando lo que escribieron
        return redirect('perfil_publico', username=query)
    else:
        # Si buscaron vacío, vuelve al inicio
        return redirect('home')
    
def check_username_availability(request):
    username = request.GET.get('username', '').strip()
    
    if not username:
        return JsonResponse({'exists': False})

    # Buscamos en la base de datos de Django si alguien ya tiene ese 'first_name'
    # Usamos __iexact para que no importe mayúsculas/minúsculas (Cris == cris)
    exists = User.objects.filter(first_name__iexact=username).exists()
    
    return JsonResponse({'exists': exists})

def forgot_password_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'comuni/forgot_password.html')
@login_required
def change_password_view(request):
    return render(request, 'comuni/change_password.html')

@login_required
def comunidad_view(request):
    grupos_ref = db.collection('lfg_groups')
    query = grupos_ref.where('estado', '==', 'abierto').order_by('creado_el', direction=firestore.Query.DESCENDING)
    results = query.stream()

    lista_grupos = []
    for doc in results:
        data = doc.to_dict()
        data['id'] = doc.id
        lista_grupos.append(data)

    context = {
        'grupos': lista_grupos,
        'rangos': ['Hierro', 'Bronce', 'Plata', 'Oro', 'Platino', 'Diamante', 'Ascendente', 'Inmortal'],
        'regiones': ['LATAM', 'BR', 'NA', 'EU'],
        'servidores': ['Santiago', 'Mexico City', 'Miami', 'Sao Paulo']
    }
    return render(request, 'comuni/comunidad_lista.html', context) # Nota el cambio de nombre del template

# --- PÁGINA 2: LOBBY DEL GRUPO ---
@login_required
def grupo_detalle_view(request, grupo_id):
    doc_ref = db.collection('lfg_groups').document(grupo_id)
    doc = doc_ref.get()

    if not doc.exists:
        messages.error(request, "Ese grupo ya no existe.")
        return redirect('comunidad')

    grupo_data = doc.to_dict()
    grupo_data['id'] = doc.id

    return render(request, 'comuni/grupo_lobby.html', {'grupo': grupo_data})

# --- ACCIONES ACTUALIZADAS (Redirecciones) ---

@login_required
def unirse_grupo(request, grupo_id):
    # ... (Tu lógica de unirse igual que antes) ...
    # ... (código de firebase update) ...
    
    # 🚨 CAMBIO: Al unirse, te lleva ADENTRO del lobby
    return redirect('grupo_detalle', grupo_id=grupo_id)

@login_required
def salir_grupo(request, grupo_id):
    # ... (Tu lógica de salir/eliminar igual que antes) ...
    
    # 🚨 CAMBIO: Al salir, te devuelve a la LISTA
    return redirect('comunidad')

@login_required
def eliminar_grupo(request, grupo_id):
    # Solo permitimos POST para acciones destructivas (Seguridad)
    if request.method == 'POST':
        uid_usuario = request.user.username
        
        # Referencia al documento
        doc_ref = db.collection('lfg_groups').document(grupo_id)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            host_real = data.get('host_uid')
            
            # --- DEBUG (Mira esto en tu terminal negra) ---
            print(f"Usuario intentando borrar: {uid_usuario}")
            print(f"Dueño real del grupo: {host_real}")
            # ---------------------------------------------

            # Verificar si es el Host
            if host_real == uid_usuario:
                doc_ref.delete()
                messages.success(request, 'Grupo eliminado correctamente.')
            else:
                messages.error(request, 'No tienes permiso. No eres el líder.')
        else:
            messages.error(request, 'El grupo no existe o ya fue borrado.')
    
    return redirect('comunidad')
@login_required
def crear_grupo_view(request):
    if request.method == 'POST':
        uid_creador = request.user.username 

        # Recopilar datos del formulario
        nuevo_grupo = {
            'titulo': request.POST.get('titulo'),
            'host_uid': uid_creador,
            'region': request.POST.get('region'),
            'servidor': request.POST.get('servidor'),
            'rango_min': request.POST.get('rango'),
            'miembros': [uid_creador], # El creador entra automáticamente
            'cupos_max': 5,
            'cupos_actuales': 1,
            'codigo_party': '', # Se puede llenar después en el lobby
            'creado_el': datetime.datetime.now(),
            'estado': 'abierto'
        }

        try:
            # Guardar en Firebase y OBTENER LA REFERENCIA (para saber el ID nuevo)
            update_time, group_ref = db.collection('lfg_groups').add(nuevo_grupo)
            
            messages.success(request, '¡Sesión creada con éxito!')
            
            # 🚀 MEJORA DE UX: Redirigir directamente al Lobby del grupo creado
            return redirect('grupo_detalle', grupo_id=group_ref.id)

        except Exception as e:
            messages.error(request, f'Error al crear la sesión: {e}')
            return redirect('comunidad')
    
    # Si no es POST, volver a la lista
    return redirect('comunidad')