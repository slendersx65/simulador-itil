from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

SEX_CHOICES = (
    ('M','Masculino'),
    ('F','Femenino'),
    ('O','Otro'),
)

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('alumno', 'Alumno'),
    )

    full_name = models.CharField("Nombre completo", max_length=200, unique=True)
    edad = models.PositiveSmallIntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=(('M','Masculino'),('F','Femenino'),('O','Otro')), null=True, blank=True)
    rol = models.CharField(max_length=10, choices=ROLES, default='alumno')   
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk:
            orig = Usuario.objects.get(pk=self.pk)
            if orig.full_name != self.full_name:
                raise ValidationError("El nombre completo no puede ser modificado.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.rol})"


class Participacion(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_evaluacion = models.DateTimeField(default=timezone.now)
    aciertos = models.PositiveSmallIntegerField(default=0)
    total = models.PositiveSmallIntegerField(default=0)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def calcular_porcentaje(self):
        if self.total:
            self.porcentaje = round((self.aciertos / self.total) * 100, 2)
        else:
            self.porcentaje = 0
        self.save()

    def __str__(self):
        return f"{self.usuario.full_name} - {self.porcentaje}%"


class MiniCurso(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    contenido_html = models.TextField("Contenido (HTML o texto)")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class PlantillaCorreo(models.Model):
    imagen = models.ImageField(upload_to='correos/', null=True, blank=True)
    es_phishing = models.BooleanField(default=False)

    def __str__(self):
        return f"Plantilla {self.id} ({'Phishing' if self.es_phishing else 'Legítimo'})"


class Evaluacion(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    aciertos = models.IntegerField()
    total = models.IntegerField()
    porcentaje = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.full_name} - {self.porcentaje}%"


class PreguntaImagen(models.Model):
    imagen = models.ImageField(upload_to='preguntas/')
    es_phishing = models.BooleanField(default=False)
    consejo = models.CharField(max_length=255, blank=True)

    def __str__(self):
        tipo = "Phishing" if self.es_phishing else "Legítimo"
        return f"Pregunta {self.id} ({tipo})"
