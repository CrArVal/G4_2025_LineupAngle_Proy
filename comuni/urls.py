from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='comuni/login.html', 
        redirect_authenticated_user=True  
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('status/', views.status_view, name='status'),
    path('ajustes/cuenta/', views.editar_perfil_firebase, name='edit_profile'),
    path('perfil/', views.ver_perfil_propio, name='perfil_propio'),
    path('perfil/<str:username>/', views.ver_perfil_publico, name='perfil_publico'),
    
    path('buscar/', views.buscar_usuario, name='buscar_usuario'),

    path('api/check-username/', views.check_username_availability, name='check_username'),

    path('recuperar-contrasena/', views.forgot_password_view, name='forgot_password'),

    path('ajustes/password/', views.change_password_view, name='change_password'),

    path('comunidad/', views.comunidad_view, name='comunidad'), # PÁGINA 1
    path('comunidad/crear/', views.crear_grupo_view, name='crear_grupo'),
    
   
    path('comunidad/lobby/<str:grupo_id>/', views.grupo_detalle_view, name='grupo_detalle'),
    path('comunidad/codigo/<str:grupo_id>/', views.actualizar_codigo, name='actualizar_codigo'),
    
    path('comunidad/eliminar/<str:grupo_id>/', views.eliminar_grupo, name='eliminar_grupo'),
    path('comunidad/salir/<str:grupo_id>/', views.salir_grupo, name='salir_grupo'),
    path('comunidad/unirse/<str:grupo_id>/', views.unirse_grupo, name='unirse_grupo'),

]