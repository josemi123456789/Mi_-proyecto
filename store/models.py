from django.db import models
from django.contrib.auth.models import User

class Escritorio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='escritorios/', null=True, blank=True)

    def __str__(self):
        return self.nombre


class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    session_key = models.CharField(max_length=40, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def subtotal(self):
        return self.cantidad * self.escritorio.precio


class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    completo = models.BooleanField(default=False)
    nombre_completo = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    direccion = models.CharField(max_length=200, null=True)
    ciudad = models.CharField(max_length=200, null=True)
    total_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    escritorio = models.ForeignKey(Escritorio, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField(default=0)
    precio_al_momento = models.DecimalField(max_digits=10, decimal_places=2)
