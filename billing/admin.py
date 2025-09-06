from django.contrib import admin
from .models import Lease, LeaseDocument, Invoice, Payment

class LeaseDocumentInline(admin.TabularInline):
    """
    Permite editar documentos de un contrato de forma inline en el admin de Lease.
    """
    model = LeaseDocument
    extra = 1  # Número de formularios extra para mostrar

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'tenant', 'start_date', 'end_date', 'rent_amount', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('apartment__number', 'tenant__username', 'owner__username')
    inlines = [LeaseDocumentInline]

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'lease', 'amount', 'due_date', 'status')
    list_filter = ('status', 'due_date')
    search_fields = ('lease__apartment__number', 'lease__tenant__username')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount', 'payment_date', 'payment_method')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('invoice__id',)
