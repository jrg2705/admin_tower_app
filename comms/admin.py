from django.contrib import admin
from .models import Announcement, Message

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'estate', 'author', 'created_at')
    list_filter = ('estate', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'sent_at', 'read_at')
    list_filter = ('sent_at', 'read_at')
    search_fields = ('sender__username', 'receiver__username', 'content')
    date_hierarchy = 'sent_at'
