# accounts/urls.py
from django.urls import path
from .views import register_user, donate_food

urlpatterns = [
    path('register/', register_user, name='register_user'),  # Ruta: /api/register/
    path('donate-food/', donate_food, name='donate_food'),  # Ruta: /api/donate-food/
]
