from django import forms
from .models import RentaDevolucion, Inspeccion, Vehiculo, Cliente, Empleado, TipoVehiculo, Marca, Modelo, TipoCombustible

# Definición del formulario de renta
class RentaForm(forms.ModelForm):
    class Meta:
        model = RentaDevolucion
        fields = ['empleado', 'vehiculo', 'cliente', 'fecha_renta', 'fecha_devolucion', 'monto_x_dia', 'cantidad_dias', 'comentario']
        widgets = {
            'fecha_renta': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'comentario': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restringe las opciones a vehículos disponibles durante operaciones de inserción
        if not self.instance.pk:
            self.fields['vehiculo'].queryset = Vehiculo.objects.filter(estado=Vehiculo.EstadoVehiculo.DISPONIBLE)
        
        # Asignación de clases de diseño a los widgets del formulario
        tailwind_classes = "w-full bg-slate-50 text-slate-800 rounded-xl border border-slate-200 p-2.5 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = tailwind_classes

# Formulario de Inspección Técnica
class InspeccionForm(forms.ModelForm):
    class Meta:
        model = Inspeccion
        fields = '__all__'
        exclude = ['fecha_inspeccion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tailwind_classes = "w-full bg-slate-50 text-slate-800 rounded-xl border border-slate-200 p-2.5 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition"
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = tailwind_classes

# Formulario Tipo de Vehículo
class TipoVehiculoForm(forms.ModelForm):
    class Meta:
        model = TipoVehiculo
        fields = ['descripcion', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tailwind_classes = "w-full bg-slate-50 text-slate-800 rounded-xl border border-slate-200 p-2.5 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = tailwind_classes

# Formulario Marca
class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['descripcion', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tailwind_classes = "w-full bg-slate-50 text-slate-800 rounded-xl border border-slate-200 p-2.5 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = tailwind_classes

# Formulario Modelo
class ModeloForm(forms.ModelForm):
    class Meta:
        model = Modelo
        fields = ['marca', 'descripcion', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tailwind_classes = "w-full bg-slate-50 text-slate-800 rounded-xl border border-slate-200 p-2.5 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = tailwind_classes

# Formulario Tipo de Combustible
class TipoCombustibleForm(forms.ModelForm):
    class Meta:
        model = TipoCombustible
        fields = ['descripcion', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tailwind_classes = "w-full bg-slate-50 text-slate-800 rounded-xl border border-slate-200 p-2.5 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = tailwind_classes

# Formulario Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'cedula_rnc', 'no_tarjeta_cr', 'limite_credito', 'tipo_persona', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tailwind_classes = "w-full bg-slate-50 text-slate-800 rounded-xl border border-slate-200 p-2.5 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = tailwind_classes

    def clean_cedula_rnc(self):
        cedula_rnc = self.cleaned_data.get('cedula_rnc')
        # Sanea la cadena eliminando espacios en blanco perimetrales
        if cedula_rnc:
            cedula_rnc = cedula_rnc.strip()
        if not cedula_rnc.isdigit():
            raise forms.ValidationError("La cédula/RNC debe contener únicamente números sin guiones o espacios.")
        if len(cedula_rnc) not in [9, 11]:
            raise forms.ValidationError("La cédula debe tener 11 dígitos y el RNC 9 dígitos.")
        return cedula_rnc

# Formulario Empleado
class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'cedula', 'tanda_labor', 'porc_comision', 'fecha_ingreso', 'estado']
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tailwind_classes = "w-full bg-slate-50 text-slate-800 rounded-xl border border-slate-200 p-2.5 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = tailwind_classes

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if cedula:
            cedula = cedula.strip()
        if not cedula.isdigit():
            raise forms.ValidationError("La cédula debe contener únicamente números sin guiones o espacios.")
        if len(cedula) != 11:
            raise forms.ValidationError("La cédula debe tener exactamente 11 dígitos.")
        return cedula

# Formulario Vehículo
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['descripcion', 'no_chasis', 'no_motor', 'no_placa', 'tipo_vehiculo', 'marca', 'modelo', 'tipo_combustible', 'precio_por_dia', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tailwind_classes = "w-full bg-slate-50 text-slate-800 rounded-xl border border-slate-200 p-2.5 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = tailwind_classes
