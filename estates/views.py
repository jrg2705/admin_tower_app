from rest_framework import viewsets, permissions
from .models import Estate, Apartment
from .serializers import EstateSerializer, ApartmentSerializer

class EstateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows estates to be viewed or edited.
    """
    queryset = Estate.objects.all().prefetch_related('apartments', 'supervisor')
    serializer_class = EstateSerializer
    permission_classes = [permissions.IsAuthenticated]

class ApartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows apartments to be viewed or edited.
    """
    queryset = Apartment.objects.all().select_related('estate', 'owner', 'resident')
    serializer_class = ApartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
