from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    """
    Configuración del admin para el modelo UserProfile.
    """
    # Agrega los campos personalizados a la vista de edición del usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('role', 'phone', 'estate'),
        }),
    )

    # Agrega los campos personalizados a la lista de visualización
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role', 'estate')
    list_filter = UserAdmin.list_filter + ('role', 'estate')
