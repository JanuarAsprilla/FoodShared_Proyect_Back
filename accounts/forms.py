# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Persona, Empresa

class PersonaRegisterForm(UserCreationForm):
    nombre_completo = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'rol', 'nombre_completo', 'telefono', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 'persona'
        if commit:
            user.save()
            # Crear el perfil de persona
            Persona.objects.create(
                user=user,
                nombre_completo=self.cleaned_data['nombre_completo'],
                telefono=self.cleaned_data['telefono']
            )
        return user

class EmpresaRegisterForm(UserCreationForm):
    nombre_empresa = forms.CharField(max_length=50)
    tipo_empresa = forms.CharField(max_length=20)
    nit = forms.CharField(max_length=20)
    direccion = forms.CharField(max_length=50)
    pais = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'rol', 'nombre_empresa', 'tipo_empresa', 'nit', 'direccion', 'pais', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 'empresa'
        if commit:
            user.save()
            Empresa.objects.create(
                user=user,
                nombre_empresa=self.cleaned_data['nombre_empresa'],
                tipo_empresa=self.cleaned_data['tipo_empresa'],
                nit=self.cleaned_data['nit'],
                direccion=self.cleaned_data['direccion'],
                pais=self.cleaned_data['pais']
            )
        return user
