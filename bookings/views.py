from rest_framework import viewsets, permissions
from .models import Amenity, Booking
from .serializers import AmenitySerializer, BookingSerializer
from accounts.permissions import IsAdminOrReadOnly, IsOwnerOrSupervisor

class AmenityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for amenities.
    """
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        """
        Filter amenities based on the user's estate.
        """
        user = self.request.user
        if user.is_staff or not user.estate:
            return Amenity.objects.all()
        return Amenity.objects.filter(estate=user.estate)

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for bookings.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSupervisor]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role in ['ADMIN', 'SUPERVISOR']:
            if user.estate:
                return Booking.objects.filter(amenity__estate=user.estate)
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
