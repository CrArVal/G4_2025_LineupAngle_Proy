from django.urls import path
from . import views

urlpatterns = [
    path('lineuphome/', views.lineuphome, name='lineuphome'),
    path('lineupsovahave/', views.lineupsovahave, name='lineupsovahave'),
    path('gekkolineup/', views.gekkolineup, name='gekkolineup'),
    path('breachlineup/', views.breachlineup, name='breachlineup'),
    path('kayolineup/', views.kayolineup, name='kayolineup'),
    path('phoenixlineup/', views.phoenixlineup, name='phoenixlineup'),
    path('neonlineup/', views.neonlineup, name='neonlineup'),
    path('reynalineup/', views.reynalineup, name='reynalineup'),
    path('clovelineup/', views.clovelineup, name='clovelineup'),
    path('tejolineup/', views.tejolineup, name='tejolineup'),
    path('vetolineup/', views.vetolineup, name='vetolineup'),
    
    # Columna 2
    path('harborlineup/', views.harborlineup, name='harborlineup'),
    path('razelineup/', views.razelineup, name='razelineup'),
    path('skyelineup/', views.skyelineup, name='skyelineup'),
    path('killjoylineup/', views.killjoylineup, name='killjoylineup'),
    path('astralineup/', views.astralineup, name='astralineup'),
    path('yorulineup/', views.yorulineup, name='yorulineup'),
    path('omenlineup/', views.omenlineup, name='omenlineup'),
    path('deadlocklineup/', views.deadlocklineup, name='deadlocklineup'),
    path('waylaylineup/', views.waylaylineup, name='waylaylineup'),
    
    # Columna 3
    path('fadelineup/', views.fadelineup, name='fadelineup'),
    path('chamberlineup/', views.chamberlineup, name='chamberlineup'),
    path('cypherlineup/', views.cypherlineup, name='cypherlineup'),
    path('viperlineup/', views.viperlineup, name='viperlineup'),
    path('brimstonelineup/', views.brimstonelineup, name='brimstonelineup'),
    path('sagelineup/', views.sagelineup, name='sagelineup'),
    path('jettlineup/', views.jettlineup, name='jettlineup'),
    path('isolineup/', views.isolineup, name='isolineup'),
    path('vyselineup/', views.vyselineup, name='vyselineup'),
    
]