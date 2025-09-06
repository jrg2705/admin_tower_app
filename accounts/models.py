from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    """
    Modelo de usuario personalizado que extiende el de Django.
    """
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador Global'
        SUPERVISOR = 'SUPERVISOR', 'Supervisor de Torre'
        OWNER = 'OWNER', 'Propietario'
        TENANT = 'TENANT', 'Inquilino'
        RESIDENT = 'RESIDENT', 'Residente'

    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RESIDENT, verbose_name='Rol')

    # Relación con una propiedad/torre. Nulable porque un admin global no pertenece a ninguna.
    estate = models.ForeignKey(
        'estates.Estate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff',
        verbose_name='Torre Asignada'
    )

    @property
    def is_manager(self):
        "Identifica si el usuario es un administrador de torre."
        return self.role == self.Role.SUPERVISOR

    def __str__(self):
        return self.username
