from django.test import Client
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from core_api.serializers import BranchSerializer, CompanySerializer
from .models import Company, Branch, User
import json
import copy

client = Client()

# if we want to use any url which is not have any id or pk at the end of the url we can use "list",
# if any url which have ip or pk we need to use details


class CompanyTest(TestCase):
    """Test module for Company model"""

    def setUp(self):
        Company.objects.create(name="Test company1")
        Company.objects.create(name="Test company2")

    def test_company_name(self):
        test1 = Company.objects.get(name="Test company1")
        test2 = Company.objects.get(name="Test company2")
        self.assertEqual(test1.name, "Test company1")
        self.assertEqual(test2.name, "Test company2")


class BranchTest(TestCase):
    """Test module for Branch model"""

    def setUp(self):
        Company.objects.create(name="Test company")
        comp_obj = Company.objects.get(name="Test company")
        Branch.objects.create(
            name="Test branch",
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
            company=comp_obj,
        )

    def test_branch_details(self):
        test = Branch.objects.get(name="Test branch")
        self.assertEqual(test.name, "Test branch")
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
        self.assertEqual(test.company, test.company)


# ================================================================== Company API Test cases ==============================================================


class GetCompanyTest(TestCase):
    """Test module for GET Company API"""

    def setUp(self):
        self.abc = Company.objects.create(name="abc")
        self.mno = Company.objects.create(name="mno")
        self.pqr = Company.objects.create(name="pqr")
        self.xyz = Company.objects.create(name="xyz")

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
        self.valid_payload = {"name": "test company"}
        self.invalid_payload = {"name": ""}

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


class UpdateCompanyTest(TestCase):
    """Test module for updating an existing company record"""

    def setUp(self):
        self.abc = Company.objects.create(name="abc")
        self.xyz = Company.objects.create(name="xyz")
        self.valid_payload = {
            "name": "ert",
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
        self.abc = Company.objects.create(name="abc")
        self.xyz = Company.objects.create(name="xyz")

    def test_valid_delete_company(self):
        response = client.delete(
            reverse("api:company-detail", kwargs={"pk": self.abc.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_company(self):
        response = client.delete(reverse("api:company-detail", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# =================================================================== Branch API Test cases ==============================================================


class GetBranchTest(TestCase):
    """Test module for GET Branch API"""

    def setUp(self):
        self.comp_obj = Company.objects.create(name="Test company")
        self.testbranch = Branch.objects.create(
            name="Test branch",
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
            company=self.comp_obj,
        )

    def test_get_valid_branch(self):
        response = client.get(
            reverse("api:branch-detail", kwargs={"pk": self.testbranch.pk})
        )
        branch_obj = Branch.objects.get(pk=self.testbranch.pk)
        serializer = BranchSerializer(branch_obj)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_branch(self):
        response = client.get(reverse("api:branch-detail", kwargs={"pk": 40}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateBranchTest(TestCase):
    """Test module for inserting a new branch"""

    def setUp(self):
        self.comp_obj = Company.objects.create(name="Test company")
        self.valid_payload = {
            "name": "Jubleeehills",
            "company": self.comp_obj.id,
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
        self.invalid_gst_payload = copy.copy(self.valid_payload)
        self.invalid_gst_payload["gst"] = "22AAAA000A1Z5"
        self.invalid_pan_payload = copy.copy(self.valid_payload)
        self.invalid_pan_payload['pan'] = "AAAA111A"

    def test_create_valid_branch(self):
        response = client.post(
            reverse("api:branch-list"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_gst(self):
        response = client.post(
            reverse("api:branch-list"),
            data=json.dumps(self.invalid_gst_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_pan(self):
        response = client.post(
            reverse("api:branch-list"),
            data=json.dumps(self.invalid_pan_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateBranchTest(TestCase):
    """Test module for updating an existing branch record"""

    def setUp(self):
        self.comp_obj = Company.objects.create(name="Test company")
        self.testbranch = Branch.objects.create(
            name="Test branch",
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
            company=self.comp_obj,
        )
        self.valid_payload = {
            "name": "Jubleeehills",
            "company": self.comp_obj.id,
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

    def test_valid_update_branch(self):
        response = client.put(
            reverse("api:branch-detail", kwargs={"pk": self.testbranch.pk}),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_branch(self):
        response = client.put(
            reverse("api:branch-detail", kwargs={"pk": self.testbranch.pk}),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteBranchTest(TestCase):
    """Test module for deleting company record"""

    def setUp(self):
        self.comp_obj = Company.objects.create(name="Test company")
        self.testbranch = Branch.objects.create(
            name="Test branch",
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
            company=self.comp_obj,
        )

    def test_valid_delete_company(self):
        response = client.delete(
            reverse("api:company-detail", kwargs={"pk": self.testbranch.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_company(self):
        response = client.delete(reverse("api:company-detail", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
