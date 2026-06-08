from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('renta/nueva/', views.registrar_renta, name='registrar_renta'),
    path('renta/devolucion/<int:renta_id>/', views.procesar_devolucion, name='procesar_devolucion'),
    path('inspeccion/nueva/', views.registrar_inspeccion, name='registrar_inspeccion'),

    # TipoVehiculo URLs
    path('parametros/tipos/', views.list_tipo_vehiculo, name='tipo_vehiculo_list'),
    path('parametros/tipos/nuevo/', views.create_tipo_vehiculo, name='tipo_vehiculo_create'),
    path('parametros/tipos/editar/<int:pk>/', views.edit_tipo_vehiculo, name='tipo_vehiculo_edit'),
    path('parametros/tipos/eliminar/<int:pk>/', views.delete_tipo_vehiculo, name='tipo_vehiculo_delete'),

    # Marca URLs
    path('parametros/marcas/', views.list_marca, name='marca_list'),
    path('parametros/marcas/nueva/', views.create_marca, name='marca_create'),
    path('parametros/marcas/editar/<int:pk>/', views.edit_marca, name='marca_edit'),
    path('parametros/marcas/eliminar/<int:pk>/', views.delete_marca, name='marca_delete'),

    # Modelo URLs
    path('parametros/modelos/', views.list_modelo, name='modelo_list'),
    path('parametros/modelos/nuevo/', views.create_modelo, name='modelo_create'),
    path('parametros/modelos/editar/<int:pk>/', views.edit_modelo, name='modelo_edit'),
    path('parametros/modelos/eliminar/<int:pk>/', views.delete_modelo, name='modelo_delete'),

    # TipoCombustible URLs
    path('parametros/combustibles/', views.list_tipo_combustible, name='tipo_combustible_list'),
    path('parametros/combustibles/nuevo/', views.create_tipo_combustible, name='tipo_combustible_create'),
    path('parametros/combustibles/editar/<int:pk>/', views.edit_tipo_combustible, name='tipo_combustible_edit'),
    path('parametros/combustibles/eliminar/<int:pk>/', views.delete_tipo_combustible, name='tipo_combustible_delete'),
]
