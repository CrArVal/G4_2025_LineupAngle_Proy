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

]