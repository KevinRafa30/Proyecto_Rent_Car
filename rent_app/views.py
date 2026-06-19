from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models import ProtectedError
from decimal import Decimal
from .models import Vehiculo, Cliente, Empleado, RentaDevolucion, Inspeccion, TipoVehiculo, Marca, Modelo, TipoCombustible
from .forms import RentaForm, InspeccionForm, TipoVehiculoForm, MarcaForm, ModeloForm, TipoCombustibleForm, ClienteForm, EmpleadoForm, VehiculoForm

# Dashboard Principal Dinámico (Kpis, Alertas, Logs transaccionales)
@login_required
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
        if costo_renta >= (renta.cliente.limite_credito * Decimal('0.85')):
            clientes_en_riesgo.append({
                'cliente': renta.cliente,
                'vehiculo': renta.vehiculo,
                'costo': costo_renta,
                'limite': renta.cliente.limite_credito,
                'renta_id': renta.id
            })

    # Listas de datos para visualización
    # Vehículos rentados para el monitoreo
    rentas_activas_qs = RentaDevolucion.objects.filter(estado=RentaDevolucion.EstadoTransaccion.ACTIVO)
    vehiculos_rentados_ids = rentas_activas_qs.values_list('vehiculo_id', flat=True)

    try:
        ultimas_rentas = RentaDevolucion.objects.order_by('-id')[:5]
        vehiculos = Vehiculo.objects.filter(id__in=vehiculos_rentados_ids)
    except Exception:
        ultimas_rentas = RentaDevolucion.objects.all()[:5]
        vehiculos = Vehiculo.objects.filter(id__in=vehiculos_rentados_ids)

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
@login_required
def registrar_renta(request):
    if request.method == 'POST':
        form = RentaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _("¡Renta registrada con éxito y comisión del empleado calculada!"))
                return redirect('renta_list')
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            messages.error(request, _("Por favor, corrija los errores del formulario."))
    else:
        form = RentaForm()
    
    # Datos de apoyo para el Javascript dinámico de validación en la UI
    clientes_data = Cliente.objects.filter(estado='Activo')
    vehiculos_data = Vehiculo.objects.filter(estado=Vehiculo.EstadoVehiculo.DISPONIBLE)

    return render(request, 'rentas/rent_form.html', {
        'form': form,
        'clientes_data': clientes_data,
        'vehiculos_data': vehiculos_data,
        'title': _("Nueva Renta de Vehículo")
    })


@login_required
def renta_list(request):
    objects = RentaDevolucion.objects.all().order_by('-fecha_renta')
    return render(request, 'rentas/renta_list.html', {'objects': objects})

@login_required
def edit_renta(request, pk):
    obj = get_object_or_404(RentaDevolucion, pk=pk)
    if request.method == 'POST':
        form = RentaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Renta actualizada con éxito."))
            return redirect('renta_list')
    else:
        form = RentaForm(instance=obj)
    
    clientes_data = Cliente.objects.filter(estado='Activo')
    vehiculos_data = Vehiculo.objects.filter(estado=Vehiculo.EstadoVehiculo.DISPONIBLE)
    # Include current vehicle if it's not in the available ones
    if obj.vehiculo not in vehiculos_data:
        vehiculos_data = vehiculos_data | Vehiculo.objects.filter(pk=obj.vehiculo.pk)

    return render(request, 'rentas/rent_form.html', {
        'form': form, 
        'title': _("Editar Renta"),
        'clientes_data': clientes_data,
        'vehiculos_data': vehiculos_data,
    })

@login_required
def delete_renta(request, pk):
    obj = get_object_or_404(RentaDevolucion, pk=pk)
    if request.method == 'POST':
        try:
            if obj.estado == 'Rentado':
                vehiculo = obj.vehiculo
                vehiculo.estado = Vehiculo.EstadoVehiculo.DISPONIBLE
                vehiculo.save()
            obj.delete()
            messages.success(request, _("¡Renta eliminada con éxito!"))
        except ProtectedError:
            messages.error(request, _("No se puede eliminar este registro porque está referenciado en otra transacción."))
        return redirect('renta_list')
    return render(request, 'parametros/confirm_delete.html', {'object': obj, 'cancel_url': 'renta_list', 'title': _("Eliminar Renta")})

# Retornar/Devolver Renta
@login_required
def procesar_devolucion(request, renta_id):
    renta = get_object_or_404(RentaDevolucion, id=renta_id)
    if request.method == 'POST':
        renta.estado = RentaDevolucion.EstadoTransaccion.DEVUELTO
        renta.save()
        messages.success(request, _("Vehículo devuelto con éxito. Flota actualizada."))
        return redirect('inspeccion_list')
    return render(request, 'rentas/devolucion_confirm.html', {'renta': renta})

# Registrar Inspección Física Técnica
@login_required
def registrar_inspeccion(request):
    if request.method == 'POST':
        form = InspeccionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Inspección física del vehículo completada con éxito."))
            return redirect('inspeccion_list')
    else:
        form = InspeccionForm()
    return render(request, 'inspecciones/inspection_form.html', {'form': form, 'title': _("Inspección Física de Vehículo")})

@login_required
def inspeccion_list(request):
    objects = Inspeccion.objects.all().order_by('-fecha_inspeccion')
    return render(request, 'inspecciones/inspeccion_list.html', {'objects': objects})

@login_required
def edit_inspeccion(request, pk):
    obj = get_object_or_404(Inspeccion, pk=pk)
    if request.method == 'POST':
        form = InspeccionForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("Inspección actualizada con éxito."))
            return redirect('inspeccion_list')
    else:
        form = InspeccionForm(instance=obj)
    return render(request, 'inspecciones/inspection_form.html', {'form': form, 'title': _("Editar Inspección")})

@login_required
def delete_inspeccion(request, pk):
    obj = get_object_or_404(Inspeccion, pk=pk)
    if request.method == 'POST':
        try:
            obj.delete()
            messages.success(request, _("¡Inspección eliminada con éxito!"))
        except ProtectedError:
            messages.error(request, _("No se puede eliminar este registro porque está referenciado en otra transacción (ej. un Vehículo o Renta)."))
        return redirect('inspeccion_list')
    return render(request, 'parametros/confirm_delete.html', {'object': obj, 'cancel_url': 'inspeccion_list', 'title': _("Eliminar Inspección")})



# CRUD for TipoVehiculo
@login_required
def list_tipo_vehiculo(request):
    objects = TipoVehiculo.objects.all().order_by('id')
    return render(request, 'parametros/tipo_vehiculo_list.html', {'objects': objects})

@login_required
def create_tipo_vehiculo(request):
    if request.method == 'POST':
        form = TipoVehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Tipo de vehículo creado con éxito!"))
            return redirect('tipo_vehiculo_list')
    else:
        form = TipoVehiculoForm()
    return render(request, 'parametros/tipo_vehiculo_form.html', {'form': form, 'title': _("Nuevo Tipo de Vehículo")})

@login_required
def edit_tipo_vehiculo(request, pk):
    obj = get_object_or_404(TipoVehiculo, pk=pk)
    if request.method == 'POST':
        form = TipoVehiculoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Tipo de vehículo actualizado con éxito!"))
            return redirect('tipo_vehiculo_list')
    else:
        form = TipoVehiculoForm(instance=obj)
    return render(request, 'parametros/tipo_vehiculo_form.html', {'form': form, 'title': _("Editar Tipo de Vehículo"), 'object': obj})

@login_required
def delete_tipo_vehiculo(request, pk):
    obj = get_object_or_404(TipoVehiculo, pk=pk)
    if request.method == 'POST':
        try:

            obj.delete()

            messages.success(request, _("¡Eliminado con éxito!"))

        except ProtectedError:

            messages.error(request, _("No se puede eliminar este registro porque está referenciado en otra transacción (ej. un Vehículo o Renta)."))
        return redirect('tipo_vehiculo_list')
    return render(request, 'parametros/confirm_delete.html', {'object': obj, 'cancel_url': 'tipo_vehiculo_list', 'title': _("Eliminar Tipo de Vehículo")})


# CRUD for Marca
@login_required
def list_marca(request):
    objects = Marca.objects.all().order_by('id')
    return render(request, 'parametros/marca_list.html', {'objects': objects})

@login_required
def create_marca(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Marca creada con éxito!"))
            return redirect('marca_list')
    else:
        form = MarcaForm()
    return render(request, 'parametros/marca_form.html', {'form': form, 'title': _("Nueva Marca")})

@login_required
def edit_marca(request, pk):
    obj = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        form = MarcaForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Marca actualizada con éxito!"))
            return redirect('marca_list')
    else:
        form = MarcaForm(instance=obj)
    return render(request, 'parametros/marca_form.html', {'form': form, 'title': _("Editar Marca"), 'object': obj})

@login_required
def delete_marca(request, pk):
    obj = get_object_or_404(Marca, pk=pk)
    if request.method == 'POST':
        try:

            obj.delete()

            messages.success(request, _("¡Eliminado con éxito!"))

        except ProtectedError:

            messages.error(request, _("No se puede eliminar este registro porque está referenciado en otra transacción (ej. un Vehículo o Renta)."))
        return redirect('marca_list')
    return render(request, 'parametros/confirm_delete.html', {'object': obj, 'cancel_url': 'marca_list', 'title': _("Eliminar Marca")})


# CRUD for Modelo
@login_required
def list_modelo(request):
    objects = Modelo.objects.all().order_by('id')
    return render(request, 'parametros/modelo_list.html', {'objects': objects})

@login_required
def create_modelo(request):
    if request.method == 'POST':
        form = ModeloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Modelo creado con éxito!"))
            return redirect('modelo_list')
    else:
        form = ModeloForm()
    return render(request, 'parametros/modelo_form.html', {'form': form, 'title': _("Nuevo Modelo")})

@login_required
def edit_modelo(request, pk):
    obj = get_object_or_404(Modelo, pk=pk)
    if request.method == 'POST':
        form = ModeloForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Modelo actualizado con éxito!"))
            return redirect('modelo_list')
    else:
        form = ModeloForm(instance=obj)
    return render(request, 'parametros/modelo_form.html', {'form': form, 'title': _("Editar Modelo"), 'object': obj})

@login_required
def delete_modelo(request, pk):
    obj = get_object_or_404(Modelo, pk=pk)
    if request.method == 'POST':
        try:

            obj.delete()

            messages.success(request, _("¡Eliminado con éxito!"))

        except ProtectedError:

            messages.error(request, _("No se puede eliminar este registro porque está referenciado en otra transacción (ej. un Vehículo o Renta)."))
        return redirect('modelo_list')
    return render(request, 'parametros/confirm_delete.html', {'object': obj, 'cancel_url': 'modelo_list', 'title': _("Eliminar Modelo")})


# CRUD for TipoCombustible
@login_required
def list_tipo_combustible(request):
    objects = TipoCombustible.objects.all().order_by('id')
    return render(request, 'parametros/tipo_combustible_list.html', {'objects': objects})

@login_required
def create_tipo_combustible(request):
    if request.method == 'POST':
        form = TipoCombustibleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Tipo de combustible creado con éxito!"))
            return redirect('tipo_combustible_list')
    else:
        form = TipoCombustibleForm()
    return render(request, 'parametros/tipo_combustible_form.html', {'form': form, 'title': _("Nuevo Tipo de Combustible")})

@login_required
def edit_tipo_combustible(request, pk):
    obj = get_object_or_404(TipoCombustible, pk=pk)
    if request.method == 'POST':
        form = TipoCombustibleForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Tipo de combustible actualizado con éxito!"))
            return redirect('tipo_combustible_list')
    else:
        form = TipoCombustibleForm(instance=obj)
    return render(request, 'parametros/tipo_combustible_form.html', {'form': form, 'title': _("Editar Tipo de Combustible"), 'object': obj})

@login_required
def delete_tipo_combustible(request, pk):
    obj = get_object_or_404(TipoCombustible, pk=pk)
    if request.method == 'POST':
        try:

            obj.delete()

            messages.success(request, _("¡Eliminado con éxito!"))

        except ProtectedError:

            messages.error(request, _("No se puede eliminar este registro porque está referenciado en otra transacción (ej. un Vehículo o Renta)."))
        return redirect('tipo_combustible_list')
    return render(request, 'parametros/confirm_delete.html', {'object': obj, 'cancel_url': 'tipo_combustible_list', 'title': _("Eliminar Tipo de Combustible")})


# CRUD for Cliente
@login_required
def list_cliente(request):
    objects = Cliente.objects.all().order_by('id')
    return render(request, 'clientes/cliente_list.html', {'objects': objects})

@login_required
def create_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Cliente creado con éxito!"))
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'clientes/cliente_form.html', {'form': form, 'title': _("Nuevo Cliente")})

@login_required
def edit_cliente(request, pk):
    obj = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Cliente actualizado con éxito!"))
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=obj)
    return render(request, 'clientes/cliente_form.html', {'form': form, 'title': _("Editar Cliente"), 'object': obj})

@login_required
def delete_cliente(request, pk):
    obj = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        try:

            obj.delete()

            messages.success(request, _("¡Eliminado con éxito!"))

        except ProtectedError:

            messages.error(request, _("No se puede eliminar este registro porque está referenciado en otra transacción (ej. un Vehículo o Renta)."))
        return redirect('cliente_list')
    return render(request, 'parametros/confirm_delete.html', {'object': obj, 'cancel_url': 'cliente_list', 'title': _("Eliminar Cliente")})


# CRUD for Empleado
@login_required
def list_empleado(request):
    objects = Empleado.objects.all().order_by('id')
    return render(request, 'empleados/empleado_list.html', {'objects': objects})

@login_required
def create_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Empleado creado con éxito!"))
            return redirect('empleado_list')
    else:
        form = EmpleadoForm()
    return render(request, 'empleados/empleado_form.html', {'form': form, 'title': _("Nuevo Empleado")})

@login_required
def edit_empleado(request, pk):
    obj = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Empleado actualizado con éxito!"))
            return redirect('empleado_list')
    else:
        form = EmpleadoForm(instance=obj)
    return render(request, 'empleados/empleado_form.html', {'form': form, 'title': _("Editar Empleado"), 'object': obj})

@login_required
def delete_empleado(request, pk):
    obj = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        try:

            obj.delete()

            messages.success(request, _("¡Eliminado con éxito!"))

        except ProtectedError:

            messages.error(request, _("No se puede eliminar este registro porque está referenciado en otra transacción (ej. un Vehículo o Renta)."))
        return redirect('empleado_list')
    return render(request, 'parametros/confirm_delete.html', {'object': obj, 'cancel_url': 'empleado_list', 'title': _("Eliminar Empleado")})


# CRUD for Vehiculo
@login_required
def list_vehiculo(request):
    objects = Vehiculo.objects.all().order_by('id')
    return render(request, 'vehiculos/vehiculo_list.html', {'objects': objects})

@login_required
def create_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Vehículo creado con éxito!"))
            return redirect('vehiculo_list')
    else:
        form = VehiculoForm()
    return render(request, 'vehiculos/vehiculo_form.html', {'form': form, 'title': _("Nuevo Vehículo")})

@login_required
def edit_vehiculo(request, pk):
    obj = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _("¡Vehículo actualizado con éxito!"))
            return redirect('vehiculo_list')
    else:
        form = VehiculoForm(instance=obj)
    return render(request, 'vehiculos/vehiculo_form.html', {'form': form, 'title': _("Editar Vehículo"), 'object': obj})

@login_required
def delete_vehiculo(request, pk):
    obj = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        try:

            obj.delete()

            messages.success(request, _("¡Eliminado con éxito!"))

        except ProtectedError:

            messages.error(request, _("No se puede eliminar este registro porque está referenciado en otra transacción (ej. un Vehículo o Renta)."))
        return redirect('vehiculo_list')
    return render(request, 'parametros/confirm_delete.html', {'object': obj, 'cancel_url': 'vehiculo_list', 'title': _("Eliminar Vehículo")})


# Consulta de Rentas
@login_required
def consulta_rentas(request):
    rentas = RentaDevolucion.objects.all()
    
    # Get parameters
    cliente_id = request.GET.get('cliente')
    vehiculo_id = request.GET.get('vehiculo')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    if cliente_id:
        rentas = rentas.filter(cliente_id=cliente_id)
    if vehiculo_id:
        rentas = rentas.filter(vehiculo_id=vehiculo_id)
    if fecha_inicio:
        rentas = rentas.filter(fecha_renta__gte=fecha_inicio)
    if fecha_fin:
        rentas = rentas.filter(fecha_renta__lte=fecha_fin)
        
    rentas = rentas.order_by('-id')
    
    clientes = Cliente.objects.filter(estado='Activo')
    vehiculos = Vehiculo.objects.all()
    
    context = {
        'rentas': rentas,
        'clientes': clientes,
        'vehiculos': vehiculos,
        'selected_cliente': int(cliente_id) if cliente_id else None,
        'selected_vehiculo': int(vehiculo_id) if vehiculo_id else None,
        'selected_fecha_inicio': fecha_inicio,
        'selected_fecha_fin': fecha_fin,
    }
    return render(request, 'rentas/consulta_rentas.html', context)


# Reporte de Rentas para Exportación
@login_required
def reporte_rentas(request):
    rentas = RentaDevolucion.objects.all()
    
    # Get parameters
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    tipo_vehiculo_id = request.GET.get('tipo_vehiculo')
    
    if fecha_inicio:
        rentas = rentas.filter(fecha_renta__gte=fecha_inicio)
    if fecha_fin:
        rentas = rentas.filter(fecha_renta__lte=fecha_fin)
    if tipo_vehiculo_id:
        rentas = rentas.filter(vehiculo__tipo_vehiculo_id=tipo_vehiculo_id)
        
    rentas = rentas.order_by('-id')
    
    # Calculate sum total
    total_monto = 0
    for r in rentas:
        total_monto += r.monto_x_dia * r.cantidad_dias
        
    tipos_vehiculo = TipoVehiculo.objects.filter(estado='Activo')
    
    context = {
        'rentas': rentas,
        'total_monto': total_monto,
        'tipos_vehiculo': tipos_vehiculo,
        'selected_fecha_inicio': fecha_inicio,
        'selected_fecha_fin': fecha_fin,
        'selected_tipo_vehiculo': int(tipo_vehiculo_id) if tipo_vehiculo_id else None,
    }
    return render(request, 'rentas/reporte_rentas.html', context)
