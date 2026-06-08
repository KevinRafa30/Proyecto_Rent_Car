from django import forms
from .models import RentaDevolucion, Inspeccion, Vehiculo, Cliente, Empleado

# Formulario de Renta con Estilos Premium de Tailwind
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
        # Solo mostrar vehículos disponibles si estamos creando una renta nueva
        if not self.instance.pk:
            self.fields['vehiculo'].queryset = Vehiculo.objects.filter(estado=Vehiculo.EstadoVehiculo.DISPONIBLE)
        
        # Estilizar campos con clases Tailwind globales
        tailwind_classes = "w-full bg-slate-800 text-slate-100 rounded-lg border border-slate-700 p-2.5 focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition"
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
        tailwind_classes = "w-full bg-slate-800 text-slate-100 rounded-lg border border-slate-700 p-2.5 focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition"
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = tailwind_classes
