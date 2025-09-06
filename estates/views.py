from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.crypto import get_random_string
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.permissions import IsAdminOrReadOnly, IsOwnerOrSupervisor
from billing.models import Lease, LeaseDocument
from .models import Estate, Apartment
from .serializers import EstateSerializer, ApartmentSerializer, RentApartmentSerializer


class EstateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows estates to be viewed or edited.
    Only Admins can edit.
    """
    queryset = Estate.objects.all().prefetch_related('apartments', 'supervisor')
    serializer_class = EstateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]


class ApartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows apartments to be viewed or edited.
    Only the owner or a supervisor/admin can edit.
    """
    queryset = Apartment.objects.all().select_related('estate', 'owner', 'resident')
    serializer_class = ApartmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSupervisor]

    @action(detail=True, methods=['post'], url_path='rent-out', serializer_class=RentApartmentSerializer)
    @transaction.atomic
    def rent_out(self, request, pk=None):
        """
        Marks an apartment as rented, creating a new tenant user and a lease.
        """
        apartment = self.get_object()
        if hasattr(apartment, 'lease') and apartment.lease.is_active:
            return Response({'error': 'This apartment is already rented.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # 1. Create Tenant User
        User = get_user_model()
        password = get_random_string(12)
        tenant = User.objects.create_user(
            username=data['tenant_email'],
            email=data['tenant_email'],
            first_name=data['tenant_first_name'],
            last_name=data['tenant_last_name'],
            password=password,
            phone=data['tenant_phone'],
            role=User.Role.TENANT,
            estate=apartment.estate
        )
        # In a real app, you'd email this password to the user.
        print(f"Generated password for {tenant.email}: {password}")

        # 2. Create Lease
        lease = Lease.objects.create(
            apartment=apartment,
            tenant=tenant,
            owner=apartment.owner,
            rent_amount=data['rent_amount'],
            start_date=data['start_date'],
            end_date=data['end_date'],
        )

        # 3. Create Lease Document if provided
        if 'contract_pdf' in data:
            LeaseDocument.objects.create(lease=lease, document=data['contract_pdf'])

        # 4. Update Apartment Resident
        apartment.resident = tenant
        apartment.save()

        return Response(
            {'status': 'Apartment rented successfully', 'tenant_id': tenant.id, 'lease_id': lease.id},
            status=status.HTTP_201_CREATED
        )
