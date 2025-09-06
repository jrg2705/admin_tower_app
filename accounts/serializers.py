from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UserProfile.
    """
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'role',
            'estate'
        ]
        read_only_fields = ['id', 'role', 'estate']
