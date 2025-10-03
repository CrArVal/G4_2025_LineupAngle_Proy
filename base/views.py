from django.shortcuts import render
from django.http import JsonResponse, HttpResponseServerError
import requests
from .valorant_client import get_agents, get_weapons, get_maps

def home(request):
    return render(request, 'base/home.html')

def agents_json(request):
    """Endpoint que devuelve agentes en JSON"""
    try:
        data = get_agents()
        return JsonResponse(data, safe=False)
    except requests.RequestException as e:
        return HttpResponseServerError(f"Error al conectar con Valorant API: {e}")

def agents_page(request):
    try:
        # Aquí elijo español latino
        data = get_agents(language="es-MX")
        agents = data.get("data", [])
    except requests.RequestException:
        agents = []
    return render(request, "base/agents.html", {"agents": agents})

# --- ARMAS ---
def weapons_json(request):
    try:
        data = get_weapons(language="es-ES")
        return JsonResponse(data, safe=False)
    except requests.RequestException as e:
        return HttpResponseServerError(f"Error en API: {e}")

def weapons_page(request):
    lang = request.GET.get("lang", "es-ES")
    try:
        data = get_weapons(language=lang)
        weapons = data.get("data", [])
    except requests.RequestException:
        weapons = []
    return render(request, "base/weapons.html", {"weapons": weapons, "lang": lang})

# --- MAPAS ---
def maps_json(request):
    try:
        data = get_maps(language="es-ES")
        return JsonResponse(data, safe=False)
    except requests.RequestException as e:
        return HttpResponseServerError(f"Error en API: {e}")

def maps_page(request):
    lang = request.GET.get("lang", "es-ES")
    try:
        data = get_maps(language=lang)
        maps = data.get("data", [])
    except requests.RequestException:
        maps = []
    return render(request, "base/maps.html", {"maps": maps, "lang": lang})