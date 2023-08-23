from django.db import models
from django.core import validators
from django.contrib.auth.models import User

class Empresa(models.Model):
    nombre = models.CharField(max_length=250)
    website = models.URLField(max_length=250)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Edificacion(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name = 'edificacionlist')
    direccion = models.CharField(max_length=250)
    pais = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=500)
    imagen = models.CharField(max_length=900)   
    avg_calificacion = models.FloatField(default=0)
    number_calificacion = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.direccion
    
class Comentario(models.Model):
    comentario_user = models.ForeignKey(User, on_delete=models.CASCADE)
    edificacion = models.ForeignKey(Edificacion, on_delete=models.CASCADE, related_name='comentarios')
    calificacion = models.PositiveIntegerField(validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)])    
    texto = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.calificacion) + ' ' + self.edificacion.direccion
