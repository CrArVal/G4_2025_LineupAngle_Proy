from django.urls import path
from . import views

urlpatterns = [
    path('lineuphome/', views.lineuphome, name='lineuphome'),
    
    
]