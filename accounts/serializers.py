from rest_framework import serializers
from .models import User, Empresa, Persona

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'rol']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class EmpresaSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Empresa
        fields = ['user', 'nombre_empresa', 'tipo_empresa', 'nit', 'direccion', 'pais']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data, rol='empresa')
        empresa = Empresa.objects.create(user=user, **validated_data)
        return empresa
