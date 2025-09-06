from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los administradores editar.
    Otros usuarios tienen permiso de solo lectura.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOwnerOrSupervisor(permissions.BasePermission):
    """
    Permiso para permitir la edición solo al propietario del objeto o a un supervisor/admin.
    """
    def has_object_permission(self, request, view, obj):
        # Permisos de lectura para todos
        if request.method in permissions.SAFE_METHODS:
            return True

        # El propietario del objeto puede editarlo
        if hasattr(obj, 'owner') and obj.owner == request.user:
            return True

        # El usuario asociado al objeto puede editarlo (inquilino, solicitante, autor, remitente)
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        if hasattr(obj, 'requester') and obj.requester == request.user:
            return True
        if hasattr(obj, 'author') and obj.author == request.user:
            return True
        if hasattr(obj, 'sender') and obj.sender == request.user:
            return True

        # El supervisor del edificio puede editar
        user = request.user
        if user.is_staff or user.role == 'SUPERVISOR':
            # Determinar el edificio del objeto
            estate = None
            if hasattr(obj, 'estate'):
                estate = obj.estate
            elif hasattr(obj, 'apartment') and hasattr(obj.apartment, 'estate'):
                estate = obj.apartment.estate
            elif hasattr(obj, 'amenity') and hasattr(obj.amenity, 'estate'):
                estate = obj.amenity.estate

            if estate and user.estate == estate:
                return True

        return False
