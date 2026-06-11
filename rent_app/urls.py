from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('renta/nueva/', views.registrar_renta, name='registrar_renta'),
    path('renta/devolucion/<int:renta_id>/', views.procesar_devolucion, name='procesar_devolucion'),
    path('inspecciones/', views.inspeccion_list, name='inspeccion_list'),
    path('inspeccion/nueva/', views.registrar_inspeccion, name='registrar_inspeccion'),
    path('inspeccion/editar/<int:pk>/', views.edit_inspeccion, name='edit_inspeccion'),
    path('inspeccion/eliminar/<int:pk>/', views.delete_inspeccion, name='delete_inspeccion'),


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

    # Cliente URLs
    path('clientes/', views.list_cliente, name='cliente_list'),
    path('clientes/nuevo/', views.create_cliente, name='cliente_create'),
    path('clientes/editar/<int:pk>/', views.edit_cliente, name='cliente_edit'),
    path('clientes/eliminar/<int:pk>/', views.delete_cliente, name='cliente_delete'),

    # Empleado URLs
    path('empleados/', views.list_empleado, name='empleado_list'),
    path('empleados/nuevo/', views.create_empleado, name='empleado_create'),
    path('empleados/editar/<int:pk>/', views.edit_empleado, name='empleado_edit'),
    path('empleados/eliminar/<int:pk>/', views.delete_empleado, name='empleado_delete'),

    # Vehiculo URLs
    path('vehiculos/', views.list_vehiculo, name='vehiculo_list'),
    path('vehiculos/nuevo/', views.create_vehiculo, name='vehiculo_create'),
    path('vehiculos/editar/<int:pk>/', views.edit_vehiculo, name='vehiculo_edit'),
    path('vehiculos/eliminar/<int:pk>/', views.delete_vehiculo, name='vehiculo_delete'),

    # Consultas y Reportes
    path('consultas/', views.consulta_rentas, name='consulta_rentas'),
    path('reportes/', views.reporte_rentas, name='reporte_rentas'),
]
