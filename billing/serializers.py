from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Lease, LeaseDocument, Invoice, Payment
from estates.models import Apartment

User = get_user_model()

class LeaseDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaseDocument
        fields = ['id', 'document', 'uploaded_at']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_date', 'payment_method']

class InvoiceSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'lease', 'amount', 'issue_date', 'due_date', 'status', 'payments']

class LeaseSerializer(serializers.ModelSerializer):
    documents = LeaseDocumentSerializer(many=True, read_only=True)
    invoices = InvoiceSerializer(many=True, read_only=True)

    # Usamos PrimaryKeyRelatedField para campos de escritura, para evitar enviar objetos anidados completos
    tenant = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='TENANT'))
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='OWNER'))
    apartment = serializers.PrimaryKeyRelatedField(queryset=Apartment.objects.all())

    class Meta:
        model = Lease
        fields = [
            'id', 'apartment', 'tenant', 'owner', 'rent_amount',
            'start_date', 'end_date', 'is_active',
            'maintenance_paid_by_owner', 'documents', 'invoices'
        ]
