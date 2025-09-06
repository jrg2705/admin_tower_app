from rest_framework import serializers
from .models import Estate, Apartment
from accounts.serializers import UserProfileSerializer

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
