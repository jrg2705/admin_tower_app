from rest_framework import serializers
from .models import MaintenanceRequest

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    # Show readable user info on read, but expect an ID on write.
    requester = serializers.StringRelatedField(read_only=True)
    apartment = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MaintenanceRequest
        fields = [
            'id', 'title', 'description', 'requester',
            'apartment', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at']
