from rest_framework import serializers
from .models import Estate, Apartment
from accounts.serializers import UserProfileSerializer


class RentApartmentSerializer(serializers.Serializer):
    """
    Serializer for the 'rent_out' action. Validates input for creating
    a new tenant and lease.
    """
    tenant_email = serializers.EmailField()
    tenant_first_name = serializers.CharField(max_length=150)
    tenant_last_name = serializers.CharField(max_length=150)
    tenant_phone = serializers.CharField(max_length=20)

    rent_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    contract_pdf = serializers.FileField(required=False)

    def validate_tenant_email(self, value):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class ApartmentSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Apartment.
    """
    # Usamos un serializer de solo lectura para mostrar info del propietario y residente
    owner = UserProfileSerializer(read_only=True)
    resident = UserProfileSerializer(read_only=True)

    class Meta:
        model = Apartment
        fields = ['id', 'number', 'estate', 'owner', 'resident']

class EstateSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Estate, incluye sus apartamentos.
    """
    apartments = ApartmentSerializer(many=True, read_only=True)
    supervisor = UserProfileSerializer(read_only=True)

    class Meta:
        model = Estate
        fields = [
            'id',
            'name',
            'address',
            'supervisor',
            'rules_pdf',
            'apartments'
        ]
