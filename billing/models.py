from django.db import models
from django.conf import settings

class Lease(models.Model):
    """
    Representa un contrato de arrendamiento de un apartamento.
    """
    apartment = models.OneToOneField(
        'estates.Apartment',
        on_delete=models.CASCADE,
        related_name='lease',
        verbose_name='Apartamento'
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='leases_as_tenant',
        limit_choices_to={'role': 'TENANT'},
        verbose_name='Inquilino'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='leases_as_owner',
        limit_choices_to={'role': 'OWNER'},
        verbose_name='Propietario'
    )
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto del Alquiler')
    start_date = models.DateField(verbose_name='Fecha de Inicio')
    end_date = models.DateField(verbose_name='Fecha de Fin')
    is_active = models.BooleanField(default=True, verbose_name='Contrato Activo')
    maintenance_paid_by_owner = models.BooleanField(default=True, verbose_name='Mantenimiento pagado por propietario')

    def __str__(self):
        return f"Contrato para {self.apartment} (Inquilino: {self.tenant})"

class LeaseDocument(models.Model):
    """
    Almacena los documentos PDF asociados a un contrato de arrendamiento.
    """
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='documents', verbose_name='Contrato')
    document = models.FileField(upload_to='leases/contracts/', verbose_name='Documento PDF')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documento para contrato {self.lease.id}"

class Invoice(models.Model):
    """
    Representa una factura, generalmente de alquiler o mantenimiento.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        PAID = 'PAID', 'Pagada'
        OVERDUE = 'OVERDUE', 'Vencida'

    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='invoices', verbose_name='Contrato')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto')
    issue_date = models.DateField(auto_now_add=True, verbose_name='Fecha de Emisión')
    due_date = models.DateField(verbose_name='Fecha de Vencimiento')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, verbose_name='Estado')

    def __str__(self):
        return f"Factura {self.id} para {self.lease.apartment} - {self.status}"

class Payment(models.Model):
    """
    Representa un pago realizado para una factura.
    """
    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'CC', 'Tarjeta de Crédito'
        BANK_TRANSFER = 'TRANSFER', 'Transferencia Bancaria'
        CASH = 'CASH', 'Efectivo'
        OTHER = 'OTHER', 'Otro'

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments', verbose_name='Factura')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Pagado')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Pago')
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, verbose_name='Método de Pago')

    def __str__(self):
        return f"Pago de {self.amount} para Factura {self.invoice.id}"
