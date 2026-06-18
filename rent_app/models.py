from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

def validar_cedula_rnc(valor):
    valor = valor.replace("-", "").strip()
    if not valor.isdigit():
        raise ValidationError(_("La cédula o RNC debe contener solo números."))
    
    if len(valor) == 11:
        # Validar Cédula
        suma = 0
        multiplicadores = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
        for i in range(10):
            digito = int(valor[i]) * multiplicadores[i]
            if digito >= 10:
                digito = (digito // 10) + (digito % 10)
            suma += digito
        digito_verificador = (10 - (suma % 10)) % 10
        if digito_verificador != int(valor[10]):
            raise ValidationError(_("La cédula ingresada no es válida."))
            
    elif len(valor) == 9:
        # Validar RNC
        pesos = [7, 9, 8, 6, 5, 4, 3, 2]
        suma = sum(int(valor[i]) * pesos[i] for i in range(8))
        resto = suma % 11
        if resto == 0:
            dv = 2
        elif resto == 1:
            dv = 1
        else:
            dv = 11 - resto
        if dv != int(valor[8]):
            raise ValidationError(_("El RNC ingresado no es válido."))
    else:
        raise ValidationError(_("La cédula debe tener 11 dígitos y el RNC 9 dígitos."))

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
    cedula_rnc = models.CharField(max_length=20, unique=True, verbose_name=_("Cédula / RNC"), validators=[validar_cedula_rnc])
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
    cedula = models.CharField(max_length=20, unique=True, verbose_name=_("Cédula"), validators=[validar_cedula_rnc])
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
    goma_delantera_izq = models.BooleanField(default=True, verbose_name=_("Goma Delantera Izquierda (Buen Estado)"))
    goma_delantera_der = models.BooleanField(default=True, verbose_name=_("Goma Delantera Derecha (Buen Estado)"))
    goma_trasera_izq = models.BooleanField(default=True, verbose_name=_("Goma Trasera Izquierda (Buen Estado)"))
    goma_trasera_der = models.BooleanField(default=True, verbose_name=_("Goma Trasera Derecha (Buen Estado)"))
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
        # 0. Validar que la fecha de renta no sea pasada al crear una renta
        if not self.pk and self.fecha_renta:
            if self.fecha_renta < timezone.localdate():
                raise ValidationError(_("No puedes registrar una renta en una fecha pasada."))

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

    @property
    def monto_total(self):
        return self.monto_x_dia * self.cantidad_dias

    def __str__(self):
        return f"Renta {self.id} - Cliente: {self.cliente.nombre}"
