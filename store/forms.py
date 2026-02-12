from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Escritorio, MensajeContacto, Pedido # Importación limpia de los modelos

# Formulario para crear/editar Escritorios (Panel Admin)
class EscritorioForm(forms.ModelForm):
    class Meta:
        model = Escritorio
        fields = ['nombre', 'descripcion', 'precio', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# Formulario para Registro de Usuarios (Con Email)
class RegistroForm(UserCreationForm):
    # Agregamos el campo email y lo hacemos obligatorio
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = User
        # Definimos qué campos mostrar del modelo (las contraseñas se agregan solas)
        fields = ['username', 'email'] 
        labels = {
            'username': 'Nombre de Usuario',
        }

# Formulario para Contacto (Página Contacto)
class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tucorreo@ejemplo.com'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe tu mensaje aquí...'}),
        }


# --- EN store/forms.py ---

# Importa el nuevo modelo:
# from .models import Escritorio, MensajeContacto, Pedido 
# Asegúrate de importar Pedido en la línea de imports de .models

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre_completo', 'email', 'direccion', 'ciudad']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
        }        