from django.contrib import admin
from .models import Amenity, Booking

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'estate')
    list_filter = ('estate',)
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('amenity', 'user', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'amenity__estate', 'amenity')
    search_fields = ('user__username', 'amenity__name')
    date_hierarchy = 'start_time'
