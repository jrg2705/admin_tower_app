from django.db import models
from django.conf import settings

class Amenity(models.Model):
    """
    Representa un espacio o área común que se puede reservar.
    """
    estate = models.ForeignKey(
        'estates.Estate',
        on_delete=models.CASCADE,
        related_name='amenities',
        verbose_name='Edificio'
    )
    name = models.CharField(max_length=100, verbose_name='Nombre de la Amenidad')
    description = models.TextField(blank=True, verbose_name='Descripción')
    rules = models.TextField(blank=True, verbose_name='Reglas de Uso')

    def __str__(self):
        return f"{self.name} - {self.estate.name}"

class Booking(models.Model):
    """
    Representa la reserva de una amenidad por un usuario.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente de Aprobación'
        CONFIRMED = 'CONFIRMED', 'Confirmada'
        CANCELLED = 'CANCELLED', 'Cancelada'

    amenity = models.ForeignKey(
        Amenity,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Amenidad'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Usuario'
    )
    start_time = models.DateTimeField(verbose_name='Inicio de la Reserva')
    end_time = models.DateTimeField(verbose_name='Fin de la Reserva')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Estado'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.amenity.name} por {self.user} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"
