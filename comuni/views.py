from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

def registro(request):
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