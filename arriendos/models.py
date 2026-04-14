from django.db import models
from django.contrib.auth.models import User

class Maquina(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la Máquina")
    descripcion = models.TextField(verbose_name="Descripción detallada")
    precio_por_dia = models.IntegerField(verbose_name="Precio por Día") 
    disponible = models.BooleanField(default=True, verbose_name="¿Está disponible?")
    
    # Campo para subir la foto de la máquina
    imagen = models.ImageField(upload_to='maquinas/', null=True, blank=True)

    @property
    def precio_formateado(self):
        # Esta función hace el trabajo sucio de poner los puntos
        return "{:,.0f}".format(self.precio_por_dia).replace(",", ".")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Máquina"
        verbose_name_plural = "Máquinas"


class Arriendo(models.Model):
    ESTADOS_ARRIENDO = [
        ('pendiente', 'Pendiente de Confirmación'),
        ('aprobado', 'Aprobado y Pagado'),
        ('en_curso', 'En Curso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]

    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='arriendos')
    
    

    nombre_cliente = models.CharField(max_length=150, verbose_name="Nombre Completo", default="Cliente Antiguo")
    email_cliente = models.EmailField(verbose_name="Correo Electrónico", default="sin@correo.com")
    telefono_cliente = models.CharField(max_length=20, verbose_name="Teléfono", default="+56900000000")
    

    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Término")
    estado = models.CharField(max_length=20, choices=ESTADOS_ARRIENDO, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.maquina.nombre} - Solicitado por {self.nombre_cliente}"

    class Meta:
        verbose_name = "Arriendo"
        verbose_name_plural = "Arriendos"


