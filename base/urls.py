from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path("api/agents/", views.agents_json, name="agents_json"),
    path("agents/", views.agents_page, name="agents_page"),

    path("api/weapons/", views.weapons_json, name="weapons_json"),
    path("weapons/", views.weapons_page, name="weapons_page"),

    path("api/maps/", views.maps_json, name="maps_json"),
    path("maps/", views.maps_page, name="maps_page"),
]