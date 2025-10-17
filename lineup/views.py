from django.shortcuts import render
from django.http import JsonResponse, HttpResponseServerError
import requests


def lineuphome(request):
    return render(request, 'lineup/lineuphome.html')
def lineupsovahave(request):
    return render(request, 'lineup/lineupsovahave.html')
