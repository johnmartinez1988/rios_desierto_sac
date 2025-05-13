from django import forms
from .models import TipoDocumento

class BuscarClienteForm(forms.Form):
    tipo_documento = forms.ModelChoiceField(queryset=TipoDocumento.objects.all(), empty_label="Seleccione tipo de documento")
    numero_documento = forms.CharField(max_length=20)