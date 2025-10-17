from django.shortcuts import render
from django.http import JsonResponse, HttpResponseServerError
import requests


def registro(request):
    return render(request, 'comuni/registro.html')

def login(request):
    return render(request, 'comuni/login.html')

