from rest_framework import serializers
from .models import Announcement, Message

class AnnouncementSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'estate', 'author', 'created_at']
        read_only_fields = ['author', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'sent_at', 'read_at']
        read_only_fields = ['sender', 'sent_at', 'read_at']
