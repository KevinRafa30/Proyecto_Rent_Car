from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('renta/nueva/', views.registrar_renta, name='registrar_renta'),
    path('renta/devolucion/<int:renta_id>/', views.procesar_devolucion, name='procesar_devolucion'),
    path('inspeccion/nueva/', views.registrar_inspeccion, name='registrar_inspeccion'),
]
