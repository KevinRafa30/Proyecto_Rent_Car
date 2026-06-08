from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class EstadoActivo(models.TextChoices):
    ACTIVO = 'Activo', _('Activo')
    INACTIVO = 'Inactivo', _('Inactivo')

# 1. Tipos de Vehículos
class TipoVehiculo(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name=_("Descripción"))
    estado = models.CharField(max_length=10, choices=EstadoActivo.choices, default=EstadoActivo.ACTIVO)

    def __str__(self):
        return self.descripcion

# 2. Marcas de Vehículos
class Marca(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name=_("Descripción"))
    estado = models.CharField(max_length=10, choices=EstadoActivo.choices, default=EstadoActivo.ACTIVO)

    def __str__(self):
        return self.descripcion

# 3. Modelos de Vehículos (Relacionado con Marcas)
class Modelo(models.Model):
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, verbose_name=_("Marca"))
    descripcion = models.CharField(max_length=100, verbose_name=_("Descripción"))
    estado = models.CharField(max_length=10, choices=EstadoActivo.choices, default=EstadoActivo.ACTIVO)

    def __str__(self):
        return f"{self.marca.descripcion} - {self.descripcion}"

# 4. Tipos de Combustibles
class TipoCombustible(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name=_("Descripción"))
    estado = models.CharField(max_length=10, choices=EstadoActivo.choices, default=EstadoActivo.ACTIVO)

    def __str__(self):
        return self.descripcion

# 5. Vehículos
class Vehiculo(models.Model):
    class EstadoVehiculo(models.TextChoices):
        DISPONIBLE = 'Disponible', _('Disponible')
        RENTADO = 'Rentado', _('Rentado')
        MANTENIMIENTO = 'Mantenimiento', _('Mantenimiento')

    descripcion = models.CharField(max_length=200, verbose_name=_("Descripción/Nombre"))
    no_chasis = models.CharField(max_length=50, unique=True, verbose_name=_("No. Chasis"))
    no_motor = models.CharField(max_length=50, unique=True, verbose_name=_("No. Motor"))
    no_placa = models.CharField(max_length=20, unique=True, verbose_name=_("No. Placa"))
    tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.PROTECT, verbose_name=_("Tipo de Vehículo"))
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, verbose_name=_("Marca"))
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT, verbose_name=_("Modelo"))
    tipo_combustible = models.ForeignKey(TipoCombustible, on_delete=models.PROTECT, verbose_name=_("Tipo de Combustible"))
    precio_por_dia = models.DecimalField(max_digits=10, decimal_places=2, default=1500.00, verbose_name=_("Precio por Día"))
    estado = models.CharField(max_length=20, choices=EstadoVehiculo.choices, default=EstadoVehiculo.DISPONIBLE)

    def __str__(self):
        return f"{self.descripcion} [{self.no_placa}]"

# 6. Clientes
class Cliente(models.Model):
    class TipoPersona(models.TextChoices):
        FISICA = 'Fisica', _('Física')
        JURIDICA = 'Juridica', _('Jurídica')

    nombre = models.CharField(max_length=150, verbose_name=_("Nombre Completo"))
    cedula_rnc = models.CharField(max_length=20, unique=True, verbose_name=_("Cédula / RNC"))
    no_tarjeta_cr = models.CharField(max_length=19, verbose_name=_("No. Tarjeta de Crédito"))
    limite_credito = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Límite de Crédito"))
    tipo_persona = models.CharField(max_length=15, choices=TipoPersona.choices, default=TipoPersona.FISICA)
    estado = models.CharField(max_length=10, choices=EstadoActivo.choices, default=EstadoActivo.ACTIVO)

    def __str__(self):
        return f"{self.nombre} ({self.cedula_rnc})"

# 7. Empleados
class Empleado(models.Model):
    class TandaLaboral(models.TextChoices):
        MATUTINA = 'Matutina', _('Matutina')
        VESPERTINA = 'Vespertina', _('Vespertina')
        NOCTURNA = 'Nocturna', _('Nocturna')

    nombre = models.CharField(max_length=150, verbose_name=_("Nombre"))
    cedula = models.CharField(max_length=20, unique=True, verbose_name=_("Cédula"))
    tanda_labor = models.CharField(max_length=15, choices=TandaLaboral.choices, default=TandaLaboral.MATUTINA)
    porc_comision = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Porcentaje Comisión (%)"))
    fecha_ingreso = models.DateField(default=timezone.now, verbose_name=_("Fecha de Ingreso"))
    estado = models.CharField(max_length=10, choices=EstadoActivo.choices, default=EstadoActivo.ACTIVO)

    def __str__(self):
        return f"{self.nombre} - {self.tanda_labor}"

# 8. Inspección de Vehículos
class Inspeccion(models.Model):
    class NivelCombustible(models.TextChoices):
        UN_CUARTO = '1/4', '1/4'
        MEDIO = '1/2', '1/2'
        TRES_CUARTOS = '3/4', '3/4'
        LLENO = 'Lleno', _('Lleno')

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, verbose_name=_("Vehículo"))
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name=_("Cliente"))
    tiene_ralladuras = models.BooleanField(default=False, verbose_name=_("Tiene Ralladuras"))
    cantidad_combustible = models.CharField(max_length=10, choices=NivelCombustible.choices, default=NivelCombustible.MEDIO, verbose_name=_("Cantidad de Combustible"))
    tiene_goma_repuesto = models.BooleanField(default=True, verbose_name=_("Tiene Goma de Repuesto"))
    tiene_gato = models.BooleanField(default=True, verbose_name=_("Tiene Gato Hidráulico"))
    tiene_roturas_cristal = models.BooleanField(default=False, verbose_name=_("Tiene Roturas de Cristal"))
    estado_gomas_delanteras_ok = models.BooleanField(default=True, verbose_name=_("Gomas Delanteras en Buen Estado"))
    estado_gomas_traseras_ok = models.BooleanField(default=True, verbose_name=_("Gomas Traseras en Buen Estado"))
    fecha_inspeccion = models.DateTimeField(default=timezone.now, verbose_name=_("Fecha de Inspección"))
    empleado_inspector = models.ForeignKey(Empleado, on_delete=models.PROTECT, verbose_name=_("Inspector"))
    estado = models.CharField(max_length=10, choices=EstadoActivo.choices, default=EstadoActivo.ACTIVO)

    def __str__(self):
        return f"Inspección {self.id} - Vehículo: {self.vehiculo.descripcion}"

# 9. Renta y Devolución (Reglas de Negocio Robustas)
class RentaDevolucion(models.Model):
    class EstadoTransaccion(models.TextChoices):
        ACTIVO = 'Activo', _('Activo / Rentado')
        DEVUELTO = 'Devuelto', _('Devuelto con Éxito')

    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, verbose_name=_("Empleado Ejecutor"))
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, verbose_name=_("Vehículo"))
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name=_("Cliente"))
    fecha_renta = models.DateField(default=timezone.now, verbose_name=_("Fecha de Renta"))
    fecha_devolucion = models.DateField(verbose_name=_("Fecha de Devolución Estimada"))
    monto_x_dia = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Monto por Día"))
    cantidad_dias = models.IntegerField(verbose_name=_("Cantidad de Días"))
    comentario = models.TextField(blank=True, null=True, verbose_name=_("Comentario"))
    comision_calculada = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True, verbose_name=_("Comisión Calculada"))
    estado = models.CharField(max_length=15, choices=EstadoTransaccion.choices, default=EstadoTransaccion.ACTIVO)

    def clean(self):
        # 1. Validar que el vehículo esté disponible para renta si es un registro nuevo
        if not self.pk and self.vehiculo.estado != Vehiculo.EstadoVehiculo.DISPONIBLE:
            raise ValidationError(_("El vehículo seleccionado no se encuentra disponible para renta en este momento."))

        # 2. Validar que la fecha de devolución sea posterior o igual a la de renta
        if self.fecha_devolucion and self.fecha_renta and self.fecha_devolucion < self.fecha_renta:
            raise ValidationError(_("La fecha de devolución no puede ser anterior a la fecha de inicio de la renta."))

        # 3. Validar el Límite de Crédito del cliente en tiempo real
        costo_total = self.monto_x_dia * self.cantidad_dias
        if costo_total > self.cliente.limite_credito:
            raise ValidationError(_(
                f"Límite de crédito insuficiente. El costo total de la renta (${costo_total:,.2f}) "
                f"supera el límite de crédito disponible del cliente (${self.cliente.limite_credito:,.2f})."
            ))

    def save(self, *args, **kwargs):
        self.clean()
        
        # Calcular Comisión sobre el Monto Total al momento de creación
        monto_total = self.monto_x_dia * self.cantidad_dias
        porcentaje = self.empleado.porc_comision / 100
        self.comision_calculada = monto_total * porcentaje

        # Cambiar estado del vehículo de forma automática
        if not self.pk: # Creación
            self.vehiculo.estado = Vehiculo.EstadoVehiculo.RENTADO
            self.vehiculo.save()
        elif self.estado == self.EstadoTransaccion.DEVUELTO: # Devolución exitosa
            self.vehiculo.estado = Vehiculo.EstadoVehiculo.DISPONIBLE
            self.vehiculo.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Renta {self.id} - Cliente: {self.cliente.nombre}"
