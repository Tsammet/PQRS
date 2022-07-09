from django.db import models

# Create your models here.

class usuario(models.Model):
    TIPO_CLIENTE_CHOICES = [
        ('A','A'),
        ('B','B'),
        ('C','C'),
    ]

    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    cc = models.IntegerField(unique=True)
    correo = models.EmailField(max_length=30,)
    tipo_cliente = models.CharField(max_length=1, choices=TIPO_CLIENTE_CHOICES, )
   

    def __str__(self):
        return self.cc




class pqrs(models.Model):
    TIPO_CLIENTE_CHOICES = [
        ('A','A'),
        ('B','B'),
        ('C','C'),
    ]

    TIPO_SOLICITUD_CHOICES = [
        ('PREGUNTA', 'P'),
        ('QUEJA', 'Q'),
        ('RECLAMO', 'R'),
        ('SUGERENCIAS', 'S'),
    ]

    ESTADO_PQRS_CHOICES = [
        ('ABIERTO', 'ABIERTO'),
        ('PROGRESO', 'PROGRESO'),
        ('CERRADO', 'CERRADO'),
        
    ]


    
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE, to_field='cc')
    tipo_solicitud = models.CharField(max_length=11, choices=TIPO_SOLICITUD_CHOICES, null=True)
    asunto = models.CharField(max_length=20, null=True)
    comentario = models.CharField(max_length=100, null=True)
    estado_pqrs = models.CharField(max_length=8, default="ABIERTO", choices=ESTADO_PQRS_CHOICES)
    tratamiento = models.CharField(max_length=10, null=True)
    fecha_solicitud = models.DateField(null=True, auto_now=False)

    def __str__(self):
        return self.usuario.cc


class piano(models.Model):
    referencia_piano = models.CharField(max_length=20, null=False)
    precio=models.IntegerField(null=False)
    image=models.ImageField(upload_to='pianos')
    contenido= models.CharField(max_length=500, null=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.referencia_piano


class agendar_cita(models.Model):
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE, to_field="cc")
    asunto_cita = models.CharField(max_length=20, null=False)
    fecha_inicio = models.DateTimeField(auto_now=False, null=False)
    fecha_salida = models.DateTimeField(null=False)

