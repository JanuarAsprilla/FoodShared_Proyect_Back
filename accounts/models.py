# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROL_CHOICES = (
        ('persona', 'Persona'),
        ('empresa', 'Empresa'),
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='persona')

class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='persona_profile')
    nombre_completo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empresa_profile')
    nombre_empresa = models.CharField(max_length=50)
    tipo_empresa = models.CharField(max_length=100)  
    nit = models.CharField(max_length=20)
    direccion = models.CharField(max_length=50)
    pais = models.CharField(max_length=15)
    



class Donacion(models.Model):
    nombre_donante = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    tipo_alimento = models.CharField(max_length=50)
    fecha_donacion = models.DateField()
    cantidad = models.PositiveIntegerField()
    metodo_entrega = models.CharField(max_length=50)
    fecha_vencimiento = models.DateField()
    detalles = models.TextField(blank=True, null=True)



