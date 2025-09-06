from rest_framework import viewsets, permissions
from .models import MaintenanceRequest
from .serializers import MaintenanceRequestSerializer

from accounts.permissions import IsOwnerOrSupervisor

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint for maintenance requests.
    Users can only see their own requests. Admins/Supervisors see all for their estate.
    """
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSupervisor]

    def get_queryset(self):
        """
        Dynamically filter the queryset based on the user's role.
        """
        user = self.request.user
        if user.is_staff or user.role in ['ADMIN', 'SUPERVISOR']:
            if user.estate:
                return MaintenanceRequest.objects.filter(apartment__estate=user.estate)
            return MaintenanceRequest.objects.all() # Global admin
        return MaintenanceRequest.objects.filter(requester=user)

    def perform_create(self, serializer):
        """
        Assign the current user as the requester.
        """
        serializer.save(requester=self.request.user)
