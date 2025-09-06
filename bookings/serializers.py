from rest_framework import serializers
from .models import Amenity, Booking

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'description', 'rules', 'estate']

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    amenity = AmenitySerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'amenity', 'start_time', 'end_time', 'status', 'created_at']
        read_only_fields = ['user', 'status', 'created_at']
