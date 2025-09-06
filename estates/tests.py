from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Estate, Apartment
from billing.models import Lease

User = get_user_model()

class ApartmentApiTests(APITestCase):
    def setUp(self):
        # Create users with different roles
        self.owner = User.objects.create_user(username='owner', password='password', role=User.Role.OWNER)
        self.other_user = User.objects.create_user(username='other', password='password', role=User.Role.OWNER)

        # Create an estate and an apartment
        self.estate = Estate.objects.create(name='Test Tower')
        self.apartment = Apartment.objects.create(
            number='101',
            estate=self.estate,
            owner=self.owner
        )

    def test_rent_out_apartment_success(self):
        """
        Ensure an owner can successfully rent out their apartment.
        """
        self.client.login(username='owner', password='password')

        url = f'/api/apartments/{self.apartment.id}/rent-out/'
        data = {
            "tenant_email": "new.tenant@example.com",
            "tenant_first_name": "New",
            "tenant_last_name": "Tenant",
            "tenant_phone": "123456789",
            "rent_amount": "1200.00",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31"
        }

        response = self.client.post(url, data, format='json')

        # Check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'Apartment rented successfully')

        # Check database state
        self.apartment.refresh_from_db()
        self.assertTrue(User.objects.filter(email="new.tenant@example.com").exists())
        tenant = User.objects.get(email="new.tenant@example.com")
        self.assertEqual(tenant.role, User.Role.TENANT)
        self.assertEqual(self.apartment.resident, tenant)
        self.assertTrue(Lease.objects.filter(apartment=self.apartment, tenant=tenant).exists())

    def test_rent_out_permission_denied(self):
        """
        Ensure a user cannot rent out an apartment they do not own.
        """
        self.client.login(username='other', password='password')

        url = f'/api/apartments/{self.apartment.id}/rent-out/'
        data = { "tenant_email": "test@test.com" } # Data doesn't need to be complete

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
