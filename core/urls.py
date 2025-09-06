from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from accounts.views import UserProfileViewSet
from estates.views import EstateViewSet, ApartmentViewSet

# DRF Router setup
router = routers.DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'estates', EstateViewSet)
router.register(r'apartments', ApartmentViewSet)

# URL Patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
