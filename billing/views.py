from rest_framework import viewsets, permissions
from .models import Lease, LeaseDocument, Invoice, Payment
from .serializers import (
    LeaseSerializer,
    LeaseDocumentSerializer,
    InvoiceSerializer,
    PaymentSerializer
)
from accounts.permissions import IsOwnerOrSupervisor

class LeaseViewSet(viewsets.ModelViewSet):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSupervisor]

class LeaseDocumentViewSet(viewsets.ModelViewSet):
    queryset = LeaseDocument.objects.all()
    serializer_class = LeaseDocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSupervisor]

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSupervisor]

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSupervisor]
