# arriendos/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Maquina, Arriendo

# --- NUEVA VISTA: Catálogo ---
def catalogo(request):
    # Le pedimos a la base de datos todas las máquinas que estén disponibles
    maquinas = Maquina.objects.filter(disponible=True)
    # Se las enviamos a tu archivo HTML
    return render(request, 'catalogo.html', {'maquinas': maquinas})


# --- VISTA QUE YA TENÍAS: Solicitar Arriendo ---

from django.core.mail import send_mail
from django.conf import settings

def solicitar_arriendo(request, maquina_id):
    maquina = get_object_or_404(Maquina, id=maquina_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email_usuario = request.POST.get('email')
        telefono = request.POST.get('telefono')
        f_inicio = request.POST.get('fecha_inicio')
        f_fin = request.POST.get('fecha_fin')

        # 1. Guardar en la base de datos
        Arriendo.objects.create(
            maquina=maquina,
            nombre_cliente=nombre,
            email_cliente=email_usuario,
            telefono_cliente=telefono,
            fecha_inicio=f_inicio,
            fecha_fin=f_fin
        )

        # 2. CORREO PARA EL CLIENTE (Confirmación)
        asunto_cliente = f"Confirmación de solicitud: {maquina.nombre} - Ingeniería Díazza SpA"
        mensaje_cliente = f"""
        Hola {nombre},
        Hemos recibido tu solicitud de cotización para la maquinaria: {maquina.nombre}.
        
        Detalles:
        - Desde: {f_inicio}
        - Hasta: {f_fin}
        
        Un ejecutivo de Ingeniería Díazza SpA se pondrá en contacto contigo al teléfono {telefono} a la brevedad.
        ¡Gracias por preferirnos!
        """

        # 3. CORREO PARA TI (Aviso de nueva venta)
        asunto_admin = f"🚨 NUEVA COTIZACIÓN: {maquina.nombre} de {nombre}"
        mensaje_admin = f"""
        Has recibido una nueva solicitud en la web:
        
        Cliente: {nombre}
        Correo: {email_usuario}
        Teléfono: {telefono}
        Máquina: {maquina.nombre}
        Fechas: {f_inicio} al {f_fin}
        """

        # Enviar ambos (Asegúrate de que recipient_list sea una lista [])
        try:
            # Enviar al cliente
            send_mail(asunto_cliente, mensaje_cliente, settings.DEFAULT_FROM_EMAIL, [email_usuario])
            # Enviar a tu correo personal (pon tu correo real aquí abajo)
            send_mail(asunto_admin, mensaje_admin, settings.EMAIL_HOST_USER, ['gajardo.arturo@gmail.com'])
        except Exception as e:
            print(f"Error enviando correos: {e}")

        return redirect('catalogo')

    return render(request, 'solicitar_arriendo.html', {'maquina': maquina})
