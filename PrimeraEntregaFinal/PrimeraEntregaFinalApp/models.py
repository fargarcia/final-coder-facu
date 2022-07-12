from configparser import MissingSectionHeaderError
from django.db import models
from django.forms import CharField, EmailField, URLField
from django.contrib.auth.models import User

# Create your models here.
class Avatar(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatar/', blank=True, null=True)
    
class Inicio(models.Model):
    bievenida = models.CharField(max_length=100)

class Socio(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=30)
    edad = models.IntegerField()
    deportes = models.CharField(max_length=200)
    email = models.EmailField()
    def __str__(self):
        return f"Nombre: {self.nombre} - Apellido: {self.apellido} - Edad: {self.edad} - Deportes: {self.deportes} - Email: {self.email}"
    
class Deporte(models.Model):
    deporte = models.CharField(max_length=30)
    profesor = models.CharField(max_length=70)
    horario = models.CharField(max_length=60, default="Sin horario")

class Profesor(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=30)
    deporte = models.CharField(max_length=30)
    email = models.EmailField()

class Administrador(models.Model):
    puesto = models.CharField(max_length=100)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()


class Post(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField()
    
    def __str__(self):
        return self.title
    

class Comment(models.Model): 
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80) 
    email = models.EmailField() 
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 

    class Meta: 
        ordering = ('created',) 

    def __str__(self): 
        return 'Comment by {} on {}'.format(self.name, self.post)
