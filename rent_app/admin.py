from django.contrib import admin
from .models import TipoVehiculo, Marca, Modelo, TipoCombustible, Vehiculo, Cliente, Empleado, Inspeccion, RentaDevolucion

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'no_placa', 'tipo_vehiculo', 'marca', 'precio_por_dia', 'estado')
    list_filter = ('estado', 'marca', 'tipo_combustible')
    search_fields = ('descripcion', 'no_placa', 'no_chasis')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula_rnc', 'limite_credito', 'tipo_persona', 'estado')
    search_fields = ('nombre', 'cedula_rnc')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'tanda_labor', 'porc_comision', 'estado')

@admin.register(RentaDevolucion)
class RentaDevolucionAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'cliente', 'fecha_renta', 'fecha_devolucion', 'comision_calculada', 'estado')
    readonly_fields = ('comision_calculada',)

admin.site.register(TipoVehiculo)
admin.site.register(Marca)
admin.site.register(Modelo)
admin.site.register(TipoCombustible)
admin.site.register(Inspeccion)
