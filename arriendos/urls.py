from django.urls import path
from . import views

urlpatterns = [
    path('catalogo/', views.catalogo, name='catalogo'),
    path('arrendar/<int:maquina_id>/', views.solicitar_arriendo, name='solicitar_arriendo'),
]
