from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# ViewSet Imports
from accounts.views import UserProfileViewSet
from estates.views import EstateViewSet, ApartmentViewSet
from billing.views import LeaseViewSet, LeaseDocumentViewSet, InvoiceViewSet, PaymentViewSet
from maintenance.views import MaintenanceRequestViewSet
from comms.views import AnnouncementViewSet, MessageViewSet
from bookings.views import AmenityViewSet, BookingViewSet

# DRF Router setup
router = routers.DefaultRouter()

# Accounts & Estates
router.register(r'users', UserProfileViewSet)
router.register(r'estates', EstateViewSet)
router.register(r'apartments', ApartmentViewSet)

# Billing
router.register(r'leases', LeaseViewSet)
router.register(r'lease-documents', LeaseDocumentViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'payments', PaymentViewSet)

# Maintenance
router.register(r'maintenance-requests', MaintenanceRequestViewSet)

# Comms
router.register(r'announcements', AnnouncementViewSet)
router.register(r'messages', MessageViewSet)

# Bookings
router.register(r'amenities', AmenityViewSet)
router.register(r'bookings', BookingViewSet)


# URL Patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]