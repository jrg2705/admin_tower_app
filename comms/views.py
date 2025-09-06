from django.db.models import Q
from rest_framework import viewsets, permissions
from .models import Announcement, Message
from .serializers import AnnouncementSerializer, MessageSerializer

from accounts.permissions import IsOwnerOrSupervisor

class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for announcements.
    Users can only see announcements for the estate they belong to.
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSupervisor]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or not user.estate:
            return Announcement.objects.all()
        return Announcement.objects.filter(estate=user.estate)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for private messages.
    Users can only see messages they sent or received.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSupervisor]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(receiver=user))

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
