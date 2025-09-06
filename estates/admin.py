from django.contrib import admin
from .models import Estate, Apartment

@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Estate.
    """
    list_display = ('name', 'address', 'supervisor')
    search_fields = ('name', 'address')
    list_filter = ('supervisor',)

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Apartment.
    """
    list_display = ('number', 'estate', 'owner', 'resident')
    search_fields = ('number', 'owner__username', 'resident__username', 'estate__name')
    list_filter = ('estate', 'owner')
    raw_id_fields = ('estate', 'owner', 'resident')
