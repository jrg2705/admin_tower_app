from django.db import models
from django.conf import settings

class Announcement(models.Model):
    """
    Representa un anuncio o aviso para un edificio completo.
    """
    estate = models.ForeignKey(
        'estates.Estate',
        on_delete=models.CASCADE,
        related_name='announcements',
        verbose_name='Edificio'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='announcements',
        verbose_name='Autor'
    )
    title = models.CharField(max_length=255, verbose_name='Título')
    content = models.TextField(verbose_name='Contenido')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')

    def __str__(self):
        return self.title

class Message(models.Model):
    """
    Representa un mensaje privado entre dos usuarios.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Remitente'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name='Destinatario'
    )
    content = models.TextField(verbose_name='Contenido')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Envío')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Lectura')

    def __str__(self):
        return f"De: {self.sender} a {self.receiver} ({self.sent_at:%Y-%m-%d %H:%M})"
