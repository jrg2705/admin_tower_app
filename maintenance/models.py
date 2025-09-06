from django.db import models
from django.conf import settings

class MaintenanceRequest(models.Model):
    """
    Representa una solicitud de mantenimiento hecha por un residente.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        IN_PROGRESS = 'IN_PROGRESS', 'En Proceso'
        RESOLVED = 'RESOLVED', 'Resuelto'
        CLOSED = 'CLOSED', 'Cerrado'

    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='maintenance_requests',
        verbose_name='Solicitante'
    )

    apartment = models.ForeignKey(
        'estates.Apartment',
        on_delete=models.CASCADE,
        related_name='maintenance_requests',
        verbose_name='Apartamento'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Estado'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    def __str__(self):
        return f'"{self.title}" para {self.apartment} (Estado: {self.get_status_display()})'
