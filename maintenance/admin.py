from django.contrib import admin
from .models import MaintenanceRequest

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'apartment', 'requester', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'apartment__estate')
    search_fields = ('title', 'description', 'requester__username', 'apartment__number')
    date_hierarchy = 'created_at'
