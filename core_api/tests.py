from django.test import Client
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from core_api.serializers import CompanySerializer, UserSerializer
from .models import Company, User
import json
import copy

client = Client()  # Created object to client class to call api requests.

# if we want to use any url which is not have any id or pk at the end of the url we can use "list",
# if any url which have ip or pk we need to use details


# ================================================================== Models Test cases ==================================================================


class UserTest(TestCase):
    """Test module for Company model"""

    def setUp(self):
        self.comp_obj = Company.objects.create(
            name="Test company",
            dno="123",
            area="test area",
            city="test city",
            district="test district",
            state="test state",
            country="test country",
            gst="22AAAAA0000A1Z5",
            mobile="9988776655",
            phone="1234567890",
            pan="AAAAA1111A",
        )
        self.user = User.objects.create(
            username="Test user", email="test@gmail.com", company=self.comp_obj
        )

    def test_company_name(self):
        test_user = User.objects.get(username="Test user")
        self.assertEqual(test_user.username, self.user.username)
        self.assertEqual(test_user.email, self.user.email)
        self.assertEqual(test_user.password, self.user.password)
        self.assertEqual(test_user.company.name, self.user.company.name)
        self.assertEqual(test_user.company.dno, self.user.company.dno)
        self.assertEqual(test_user.company.area, self.user.company.area)
        self.assertEqual(test_user.company.city, self.user.company.city)
        self.assertEqual(test_user.company.district, self.user.company.district)
        self.assertEqual(test_user.company.state, self.user.company.state)
        self.assertEqual(test_user.company.country, self.user.company.country)
        self.assertEqual(test_user.company.gst, self.user.company.gst)
        self.assertEqual(test_user.company.mobile, self.user.company.mobile)
        self.assertEqual(test_user.company.phone, self.user.company.phone)
        self.assertEqual(test_user.company.pan, self.user.company.pan)
        self.assertEqual(test_user.company, self.user.company)


class CompanyTest(TestCase):
    """Test module for Company model"""

    def setUp(self):
        Company.objects.create(
            name="Test company1",
            dno="123",
            area="test area",
            city="test city",
            district="test district",
            state="test state",
            country="test country",
            gst="22AAAAA0000A1Z5",
            mobile="9988776655",
            phone="1234567890",
            pan="AAAAA1111A"
        )

    def test_company_name(self):
        test = Company.objects.get(name="Test company1")
        self.assertEqual(test.name, "Test company1")
        self.assertEqual(test.dno, "123")
        self.assertEqual(test.area, "test area")
        self.assertEqual(test.city, "test city")
        self.assertEqual(test.district, "test district")
        self.assertEqual(test.state, "test state")
        self.assertEqual(test.country, "test country")
        self.assertEqual(test.gst, "22AAAAA0000A1Z5")
        self.assertEqual(test.mobile, "9988776655")
        self.assertEqual(test.phone, "1234567890")
        self.assertEqual(test.pan, "AAAAA1111A")


# ================================================================== Company API Test cases ==============================================================


class GetCompanyTest(TestCase):
    """Test module for GET Company API"""

    def setUp(self):
        self.abc = Company.objects.create(
            name="abc",
            dno="123",
            area="test area",
            city="test city",
            district="test district",
            state="test state",
            country="test country",
            gst="22AAAAA0000A1Z5",
            mobile="9988776655",
            phone="1234567890",
            pan="AAAAA1111A",
        )

    def test_get_valid_company(self):
        response = client.get(reverse("api:company-detail", kwargs={"pk": self.abc.pk}))
        comp_obj = Company.objects.get(pk=self.abc.pk)
        serializer = CompanySerializer(comp_obj)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_company(self):
        response = client.get(reverse("api:company-detail", kwargs={"pk": 40}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateCompanyTest(TestCase):
    """Test module for inserting a new company"""

    def setUp(self):
        self.valid_payload = {
            "name": "abc company",
            "dno": 128,
            "area": "Film nagar",
            "city": "Hyderabad",
            "district": "Hyderabad",
            "state": "Telangana",
            "country": "India",
            "gst": "22AAAAA0000A1Z5",
            "mobile": "998877655",
            "phone": "1234567890",
            "pan": "AAAAA1111A",
        }
        self.invalid_payload = {"name": ""}
        self.invalid_gst_payload = copy.copy(self.valid_payload)
        self.invalid_gst_payload["gst"] = "22AAAA000A1Z5"
        self.invalid_pan_payload = copy.copy(self.valid_payload)
        self.invalid_pan_payload["pan"] = "AAAA111A"

    def test_create_valid_company(self):
        response = client.post(
            reverse("api:company-list"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_company(self):
        response = client.post(
            reverse("api:company-list"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_gst(self):
        response = client.post(
            reverse("api:company-list"),
            data=json.dumps(self.invalid_gst_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_pan(self):
        response = client.post(
            reverse("api:company-list"),
            data=json.dumps(self.invalid_pan_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateCompanyTest(TestCase):
    """Test module for updating an existing company record"""

    def setUp(self):
        self.abc = Company.objects.create(
            name="abc",
            dno="123",
            area="test area",
            city="test city",
            district="test district",
            state="test state",
            country="test country",
            gst="22AAAAA0000A1Z5",
            mobile="9988776655",
            phone="1234567890",
            pan="AAAAA1111A",)
        
        self.valid_payload = {
            "name": "Jubleeehills",
            "dno": 128,
            "area": "Film nagar",
            "city": "Hyderabad",
            "district": "Hyderabad",
            "state": "Telangana",
            "country": "India",
            "gst": "22AAAAA0000A1Z5",
            "mobile": "998877655",
            "phone": "1234567890",
            "pan": "AAAAA1111A",
        }
        self.invalid_payload = {
            "name": "",
        }

    def test_valid_update_company(self):
        response = client.put(
            reverse("api:company-detail", kwargs={"pk": self.abc.pk}),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_company(self):
        response = client.put(
            reverse("api:company-detail", kwargs={"pk": self.abc.pk}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteCompanyTest(TestCase):
    """Test module for deleting company record"""

    def setUp(self):
        self.abc = Company.objects.create(
            name="abc",
            dno="123",
            area="test area",
            city="test city",
            district="test district",
            state="test state",
            country="test country",
            gst="22AAAAA0000A1Z5",
            mobile="9988776655",
            phone="1234567890",
            pan="AAAAA1111A")

    def test_valid_delete_company(self):
        response = client.delete(
            reverse("api:company-detail", kwargs={"pk": self.abc.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_company(self):
        response = client.delete(reverse("api:company-detail", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# =================================================================== User API Test cases ==============================================================


class GetUsersTest(TestCase):
    """Test module for GET User API"""

    def setUp(self):
        self.comp_obj = Company.objects.create(
            name="Test company",
            dno="123",
            area="test area",
            city="test city",
            district="test district",
            state="test state",
            country="test country",
            gst="22AAAAA0000A1Z5",
            mobile="9988776655",
            phone="1234567890",
            pan="AAAAA1111A")
        self.user = User.objects.create(
            username="testuser", password="testpassword", company=self.comp_obj
        )

    def test_get_valid_company(self):
        response = client.get(reverse("api:user-detail", kwargs={"pk": self.user.pk}))
        user_obj = User.objects.get(pk=self.comp_obj.pk)
        serializer = UserSerializer(user_obj)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_company(self):
        response = client.get(reverse("api:user-detail", kwargs={"pk": 40}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateUserTest(TestCase):
    """Test module for inserting a new user"""

    def setUp(self):
        self.comp_obj = Company.objects.create(
            name="Test company",
            dno="123",
            area="test area",
            city="test city",
            district="test district",
            state="test state",
            country="test country",
            gst="22AAAAA0000A1Z5",
            mobile="9988776655",
            phone="1234567890",
            pan="AAAAA1111A"
        )
        self.valid_payload = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@gmail.com",
            "company": self.comp_obj.id,
        }
        self.invalid_payload = copy.copy(self.valid_payload)
        self.invalid_payload["email"] = "ddbv"

    def test_create_valid_user(self):
        response = client.post(
            reverse("api:user-list"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = client.post(
            reverse("api:user-list"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateUserTest(TestCase):
    """Test module for updating an existing user record"""

    def setUp(self):
        self.comp_obj = Company.objects.create(
            name="Test company",
            dno="123",
            area="test area",
            city="test city",
            district="test district",
            state="test state",
            country="test country",
            gst="22AAAAA0000A1Z5",
            mobile="9988776655",
            phone="1234567890",
            pan="AAAAA1111A"
        )
        self.user = User.objects.create(
            username="testuser",
            email="test@email.com",
            password="test",
            company=self.comp_obj,
        )
        self.valid_payload = {
            "email": "testuser@email.com",
            "password": "test",
            "username": "testuser",
        }
        self.invalid_payload = {
            "name": "",
        }

    def test_valid_update_user(self):
        response = client.put(
            reverse("api:user-detail", kwargs={"pk": self.user.pk}),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        user_obj = User.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_user(self):
        response = client.put(
            reverse("api:user-detail", kwargs={"pk": self.user.pk}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteUserTest(TestCase):
    """Test module for deleting user record"""

    def setUp(self):
        self.comp_obj = Company.objects.create(
            name="Test company",
            dno="123",
            area="test area",
            city="test city",
            district="test district",
            state="test state",
            country="test country",
            gst="22AAAAA0000A1Z5",
            mobile="9988776655",
            phone="1234567890",
            pan="AAAAA1111A"
        )
        self.user = User.objects.create(
            username="test user",
            email="test@email.com",
            password="test",
            company=self.comp_obj,
        )

    def test_valid_delete_user(self):
        response = client.delete(
            reverse("api:user-detail", kwargs={"pk": self.comp_obj.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_user(self):
        response = client.delete(reverse("api:user-detail", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
