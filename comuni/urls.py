from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='comuni/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('status/', views.status_view, name='status'),
    path('perfil/editar/', views.editar_perfil_firebase, name='edit_profile'),
   
    path('perfil/<str:username>/', views.ver_perfil_publico, name='perfil_publico'),
    
    
    path('perfil/', views.ver_perfil_propio, name='perfil_propio'),
    path('buscar/', views.buscar_usuario, name='buscar_usuario'),
]