from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from .models import Vehiculo, Cliente, Empleado, RentaDevolucion, Inspeccion
from .forms import RentaForm, InspeccionForm

# Dashboard Principal Dinámico (Kpis, Alertas, Logs transaccionales)
def dashboard(request):
    # KPIs Clave
    total_vehiculos = Vehiculo.objects.count()
    vehiculos_disponibles = Vehiculo.objects.filter(estado=Vehiculo.EstadoVehiculo.DISPONIBLE).count()
    rentas_activas = RentaDevolucion.objects.filter(estado=RentaDevolucion.EstadoTransaccion.ACTIVO).count()
    total_clientes = Cliente.objects.count()

    # Alertas Dinámicas del Negocio (Requerimiento de UX Proactiva)
    hoy = timezone.now().date()
    rentas_hoy = RentaDevolucion.objects.filter(estado=RentaDevolucion.EstadoTransaccion.ACTIVO, fecha_devolucion=hoy)
    
    # Alertas de Clientes cerca de superar el Límite de Crédito
    clientes_en_riesgo = []
    rentas_vigentes = RentaDevolucion.objects.filter(estado=RentaDevolucion.EstadoTransaccion.ACTIVO)
    for renta in rentas_vigentes:
        costo_renta = renta.monto_x_dia * renta.cantidad_dias
        # Alerta si la renta actual consume el 85% o más del límite del cliente
        if costo_renta >= (renta.cliente.limite_credito * 0.85):
            clientes_en_riesgo.append({
                'cliente': renta.cliente,
                'vehiculo': renta.vehiculo,
                'costo': costo_renta,
                'limite': renta.cliente.limite_credito,
                'renta_id': renta.id
            })

    # Listas de datos para visualización
    ultimas_rentas = RentaDevolucion.objects.all().order_by('-id')[:5] if hasattr(RentaDevolucion.objects, 'order_by') else RentaDevolucion.objects.all()[:5]
    # En caso de que no haya registros, evitamos errores usando un listado sencillo:
    try:
        ultimas_rentas = RentaDevolucion.objects.order_by('-id')[:5]
        vehiculos = Vehiculo.objects.all()
    except Exception:
        ultimas_rentas = RentaDevolucion.objects.all()[:5]
        vehiculos = Vehiculo.objects.all()

    context = {
        'total_vehiculos': total_vehiculos,
        'vehiculos_disponibles': vehiculos_disponibles,
        'rentas_activas': rentas_activas,
        'total_clientes': total_clientes,
        'rentas_hoy': rentas_hoy,
        'clientes_en_riesgo': clientes_en_riesgo,
        'ultimas_rentas': ultimas_rentas,
        'vehiculos': vehiculos,
        'current_lang': request.LANGUAGE_CODE,
    }
    return render(request, 'dashboard.html', context)

# Crear Renta
def registrar_renta(request):
    if request.method == 'POST':
        form = RentaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _("¡Renta registrada con éxito y comisión del empleado calculada!"))
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            messages.error(request, _("Por favor, corrija los errores del formulario."))
    else:
        form = RentaForm()
    
    # Datos de apoyo para el Javascript dinámico de validación en la UI
    clientes_data = Cliente.objects.filter(estado='Activo')
    vehiculos_data = Vehiculo.objects.filter(estado=Vehiculo.EstadoVehiculo.DISPONIBLE)

    return render(request, 'rent_form.html', {
        'form': form,
        'clientes_data': clientes_data,
        'vehiculos_data': vehiculos_data,
        'title': _("Nueva Renta de Vehículo")
    })

# Retornar/Devolver Renta
def procesar_devolucion(request, renta_id):
    renta = get_object_or_404(RentaDevolucion, id=renta_id)
    if request.method == 'POST':
        renta.estado = RentaDevolucion.EstadoTransaccion.DEVUELTO
        renta.save()
        messages.success(request, _("Vehículo devuelto con éxito. Flota actualizada."))
        return redirect('dashboard')
    return render(request, 'devolucion_confirm.html', {'renta': renta})

# Registrar Inspección Física Técnica
def registrar_inspeccion(request):
    if request.method == 'POST':
        form = InspeccionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Inspección física del vehículo completada con éxito."))
            return redirect('dashboard')
    else:
        form = InspeccionForm()
    return render(request, 'inspection_form.html', {'form': form, 'title': _("Inspección Física de Vehículo")})
