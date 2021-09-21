from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ['username','password']

class UsuarioForm(UserCreationForm):
    nombres = forms.CharField(widget=forms.TextInput())
    apellidos = forms.CharField(widget=forms.TextInput())
    cedula = forms.CharField(widget= forms.TextInput())
    celular = forms.CharField(widget= forms.TextInput())
    correo = forms.EmailField(widget= forms.EmailInput())

class PagoForm(forms.ModelForm):
    
    class Meta:
        model = Pago
        fields = ['usuario','tesorero','mesDesde','mesHasta','costoServicio']
        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({
                'class': 'form-control'  
            })
        self.fields['mesDesde'].widget.attrs['readonly'] = True
        self.fields['mesHasta'].widget.attrs['readonly'] = True

class UsuarioForms(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ['nombres','apellidos','cedula','celular','correo']
        labels = {
            'nombres': 'Nombres:',
            'apellidos': 'Apellidos:',
            'cedula': 'N° Cedula:',
            'celular': 'Celular:',
            'correo': 'Correo:',
        }

    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
            'class': 'form-control'  
            })     

class TesoreroForm(forms.ModelForm):

    class Meta:
        model = Tesorero
        fields = ['nombres','apellidos','cedula','celular','correo']
        labels = {
            'nombres': 'Nombres:',
            'apellidos': 'Apellidos:',
            'cedula': 'N° Cedula:',
            'celular': 'Celular:',
            'correo': 'Correo:',
        }

    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
            'class': 'form-control'  
            })     

class ServicioForm(forms.ModelForm):
    class Meta:
        model = ServicioAgua
        fields = ['usuario','costoActivacion','motivoSuspension']
        labels = {
            'usuario': 'Usuario',
            'costoActivacion': 'Costo de Activación',
            'motivoSuspension': 'Motivo de Suspensión',
        }

    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        for field in iter(self.fields):  
            self.fields[field].widget.attrs.update({  
            'class': 'form-control'  
            })  
            
class HistorialForm(forms.ModelForm):
    class Meta:
        model = HistorialServicio
        fields = ['usuario','costoActivacion','motivoSuspension']
    