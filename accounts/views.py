# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import User, Persona, Empresa
from .models import User, Empresa
from .models import Donacion
from django.templatetags.static import static
from urllib.parse import urljoin




@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)

        rol = data.get('rol')  # 'persona' o 'empresa'
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')

        # Validaciones básicas
        if not email or not password or not password2:
            return JsonResponse({'error': 'Faltan campos obligatorios'}, status=400)
        
        if password != password2:
            return JsonResponse({'error': 'Las contraseñas no coinciden'}, status=400)

        if rol == 'persona':
            nombre_completo = data.get('nombre_completo')
            telefono = data.get('telefono')

            if not nombre_completo or not telefono:
                return JsonResponse({'error': 'Faltan datos para persona'}, status=400)

            # Crear usuario
            user = User.objects.create(
                username=email,  
                email=email,
                password=make_password(password),
                rol='persona'
            )

            # Crear perfil persona
            Persona.objects.create(
                user=user,
                nombre_completo=nombre_completo,
                telefono=telefono
            )

            return JsonResponse({'message': 'Usuario persona creado con éxito'}, status=201)

        elif rol == 'empresa':
            nombre_empresa = data.get('nombre_empresa')
            tipo_empresa = data.get('tipo_empresa')
            nit = data.get('nit')
            direccion = data.get('direccion')
            pais = data.get('pais')

            # Validar campos de empresa
            if not (nombre_empresa and tipo_empresa and nit and direccion and pais):
                return JsonResponse({'error': 'Faltan datos para empresa'}, status=400)

            # Crear usuario
            user = User.objects.create(
                username=email,  
                email=email,
                password=make_password(password),
                rol='empresa'
            )

            # Crear perfil empresa
            Empresa.objects.create(
                user=user,
                nombre_empresa=nombre_empresa,
                tipo_empresa=tipo_empresa,
                nit=nit,
                direccion=direccion,
                pais=pais
            )

            return JsonResponse({'message': 'Usuario empresa creado con éxito'}, status=201)

        else:
            return JsonResponse({'error': 'Rol inválido'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def register_company(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extraer datos del formulario
            nombre_empresa = data.get('nombre_empresa')
            tipo_empresa = data.get('tipo_empresa')
            nit = data.get('nit')
            direccion = data.get('direccion')
            pais = data.get('pais')

            # Validar campos requeridos
            if not nombre_empresa or not tipo_empresa or not nit or not direccion or not pais:
                return JsonResponse({"error": "Faltan campos requeridos"}, status=400)

            # Crear el usuario
            user = User.objects.create_user(
                username=nombre_empresa, 
                email=f"{nombre_empresa.lower().replace(' ', '')}@example.com",  # Correo generado dinámicamente
                password=nit,  # Esto debería ser una contraseña segura en producción
                rol='empresa'
            )

            # Crear la empresa
            Empresa.objects.create(
                user=user,
                nombre_empresa=nombre_empresa,
                tipo_empresa=tipo_empresa,
                nit=nit,
                direccion=direccion,
                pais=pais
            )

            return JsonResponse({"message": "Empresa registrada correctamente"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)




from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Donacion

from urllib.parse import urljoin
from django.templatetags.static import static
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Donacion

@csrf_exempt
def donate_food(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Validar campos requeridos
            required_fields = [
                'username', 'mail', 'number', 'address',
                'foodType', 'date', 'foodAmount', 'method', 'expirationDate'
            ]
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({"error": f"El campo {field} es obligatorio"}, status=400)

            # Guardar la donación en la base de datos
            donacion = Donacion.objects.create(
                nombre_donante=data['username'],
                email=data['mail'],
                telefono=data['number'],
                direccion=data['address'],
                tipo_alimento=data['foodType'],
                fecha_donacion=data['date'],
                cantidad=data['foodAmount'],
                metodo_entrega=data['method'],
                fecha_vencimiento=data['expirationDate'],
                detalles=data.get('details', '')
            )

            # Calcular la URL absoluta para el logo
            logo_url = urljoin(request.build_absolute_uri('/'), static('/accounts/img/logoSinNombre.ico'))

            # Enviar correo de agradecimiento
            subject = 'Gracias por tu donación - FoodShared'
            message = f"""
            ¡Hola {data['username']}!

            Queremos agradecerte por tu generosa donación a FoodShared.

            Detalles de tu donación:
            - Tipo de alimento: {data['foodType']}
            - Cantidad: {data['foodAmount']} unidades
            - Método de entrega: {data['method']}

            ¡Tu apoyo hace una gran diferencia!

            Saludos,
            El equipo de FoodShared
            """
            send_mail(
                subject=subject,
                message=message,
                from_email='noreply@foodshared.com',
                recipient_list=[data['mail']],
                html_message=f"""
                <html>
                <body>
                    <div style="text-align: center; font-family: Arial, sans-serif;">
                        <img src="{logo_url}" alt="Logo FoodShared" style="width: 100px; height: auto;"/>
                        <h1 style="color: #4CAF50;">¡Gracias por tu donación, {data['username']}!</h1>
                        <p>Queremos agradecerte por tu generosidad y apoyo.</p>
                        <h3>Detalles de tu donación:</h3>
                        <ul style="list-style: none; padding: 0;">
                            <li><strong>Tipo de alimento:</strong> {data['foodType']}</li>
                            <li><strong>Cantidad:</strong> {data['foodAmount']} unidades</li>
                            <li><strong>Método de entrega:</strong> {data['method']}</li>
                        </ul>
                        <p>¡Tu donación ayuda a cambiar vidas!</p>
                        <p style="font-size: 12px; color: #555;">&copy; 2024 FoodShared - Todos los derechos reservados.</p>
                    </div>
                </body>
                </html>
                """
            )

            return JsonResponse({"message": "¡Muchas gracias por la donación!"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Datos JSON inválidos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)




