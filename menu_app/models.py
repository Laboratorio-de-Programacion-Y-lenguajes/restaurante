from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def _str_(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categorias = models.ManyToManyField(Categoria, related_name="productos")
    disponible = models.BooleanField(default=True)
    precio = models.IntegerField()

    def _str_(self):
        return self.nombre

class Calificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('usuario', 'producto')

class FranjaHoraria(models.Model):
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def _str_(self):
        return f"{self.hora_inicio} - {self.hora_fin}"

class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidad = models.IntegerField()
    franjas_disponibles = models.ManyToManyField(FranjaHoraria, related_name="mesas")

    def _str_(self):
        return f"Mesa {self.numero}"

class Reserva(models.Model):
    ESTADOS_RESERVA = [
        ('Pendiente', 'Pendiente'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mesas = models.ManyToManyField(Mesa, related_name="reservas")
    franja_horaria = models.ForeignKey(FranjaHoraria, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADOS_RESERVA, default='Pendiente')
    creada_el = models.DateTimeField(auto_now_add=True)

class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ('Pendiente', 'Pendiente'),
        ('En progreso', 'En progreso'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, related_name="pedidos")
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='Pendiente')
    creado_el = models.DateTimeField(auto_now_add=True)

class Notificacion(models.Model):
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    creada_el = models.DateTimeField(auto_now_add=True)
    usuarios = models.ManyToManyField(User, through='NotificacionUsuario', related_name="notificaciones")

    def _str_(self):
        return self.titulo

class NotificacionUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    notificacion = models.ForeignKey(Notificacion, on_delete=models.CASCADE)
    leida = models.BooleanField(default=False)

    class Meta:
        unique_together = ('usuario', 'notificacion')
    def __str__(self):
        return self.name

    @classmethod
    def validate(cls, name, description, price):
        errors = {}

        if name == "":
            errors["name"] = "Por favor ingrese un nombre"

        if description == "":
            errors["description"] = "Por favor ingrese una descripcion"

        if price <= 0:
            errors["price"] = "Por favor ingrese un precio mayor a 0"

        return errors

    @classmethod
    def new(cls, name, description, price, quantity, image):
        errors = Product.validate(name, description, price)

        if len(errors.keys()) > 0:
            return False, errors

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            image=image,
        )

        return True, None

    def update(self, name, description, price, quantity):
        self.name = name or self.name
        self.description = description or self.description
        self.price = price or self.price
        self.quantity = quantity or self.quantity

        self.save()
