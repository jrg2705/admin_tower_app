from django.db import models
from django.conf import settings

class Estate(models.Model):
    """
    Representa una propiedad principal, como una torre o un edificio.
    """
    name = models.CharField(max_length=255, verbose_name='Nombre del Edificio')
    address = models.TextField(verbose_name='Dirección')

    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_estate',
        limit_choices_to={'role': 'SUPERVISOR'},
        verbose_name='Supervisor Asignado'
    )

    rules_pdf = models.FileField(
        upload_to='estates/rules/',
        blank=True,
        null=True,
        verbose_name='Normas del Edificio (PDF)'
    )

    def __str__(self):
        return self.name

class Apartment(models.Model):
    """
    Representa un apartamento o local dentro de un Estate.
    """
    number = models.CharField(max_length=50, verbose_name='Número de Apartamento/Local')

    estate = models.ForeignKey(
        Estate,
        on_delete=models.CASCADE,
        related_name='apartments',
        verbose_name='Edificio'
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_apartments',
        limit_choices_to={'role': 'OWNER'},
        verbose_name='Propietario'
    )

    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resident_of',
        limit_choices_to={'role__in': ['TENANT', 'RESIDENT']},
        verbose_name='Inquilino/Residente Actual'
    )

    def __str__(self):
        return f'{self.estate.name} - {self.number}'
