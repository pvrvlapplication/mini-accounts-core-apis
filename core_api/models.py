from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import datetime

GST_REGEX = "\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}"
MOBILE_REGEX = "\+?\d[\d -]{8,12}\d"
PAN_REGEX = "[A-Z]{5}\d{4}[A-Z]{1}"


class Company(models.Model):
    """This model is to store Company Details of an user."""

    COMPANY_TYPE_CHOICES = (
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
    )
    name = models.CharField(max_length=100, unique=True)  # Company Name
    # type = models.CharField(choices=COMPANY_TYPE_CHOICES, max_length=15)

    def __str__(self):
        return self.name


class Branch(models.Model):
    """This models is to store branch details of a company."""

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True
    )  # Company
    name = models.CharField(max_length=50)  # Branch name
    dno = models.CharField(max_length=30)  # Door number, Building name
    area = models.CharField(max_length=30)  # Village name
    city = models.CharField(max_length=30)  # City name
    district = models.CharField(max_length=25)  # District name
    state = models.CharField(max_length=20)  # State name
    country = models.CharField(max_length=20)  # Country name
    gst = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(GST_REGEX, message="Enter a Valid Indian GST Number")
        ],
    )  # GST number  22AAAAA0000A1Z5
    mobile = models.CharField(max_length=15)  # Mobile number
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(MOBILE_REGEX, message="Enter a Valid Indian Phone Number")
        ],
    )  # Phone number
    pan = models.CharField(
        max_length=15,
        validators=[RegexValidator(PAN_REGEX, message="Enter a Valid PAN Number")],
    )  # Pan number "AAAAA1111A"

    def __str__(self):
        return self.name


class User(AbstractUser):
    """This model is extension of default user model."""

    USER_ROLES = (
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
    )
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, null=True, blank=True
    )  # Branch
    mobile = models.CharField(max_length=12)  # Mobile number
    # role = models.CharField(choices=USER_ROLES, max_length=15)  # role of the user


# -------Product Models


class Product(models.Model):
    """This model is used to store information"""

    GST_SLABS = ((0, 0), (5, 5), (12, 12), (18, 18), (28, 28))
    name = models.CharField(max_length=20)  # Name of the product
    gst_slab = models.CharField(choices=GST_SLABS, max_length=5)  # GST Slab Percentage.
    hsn = models.CharField(max_length=35)  # Hsn code
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user

    def __str__(self):
        return self.name


# -------Customer & Vendor Models


class Party(models.Model):
    """This model is used to store customer and vendor information"""

    PARTY_TYPE = (("C", "CUSTOMER"), ("V", "VENDOR"))
    name = models.CharField(max_length=50)  # Name of the party
    gst = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(GST_REGEX, message="Enter a Valid Indian GST Number")
        ],
    )  # GST number  22AAAAA0000A1Z5
    pan = models.CharField(
        max_length=15,
        validators=[RegexValidator(PAN_REGEX, message="Enter a Valid PAN Number")],
    )  # Pan number "AAAAA1111A"
    party_type = models.CharField(max_length=10, choices=PARTY_TYPE)  # Type of Party
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user

    def __str__(self):
        return self.name


class Address(models.Model):
    """This model is used to store address(es) of the customers and vendors"""

    dno = models.CharField(max_length=30)  # Door number, Building name
    area = models.CharField(max_length=30)  # Village name
    city = models.CharField(max_length=30)  # City name
    district = models.CharField(max_length=25)  # District name
    state = models.CharField(max_length=20)  # State name
    country = models.CharField(max_length=20)  # Country name
    mobile = models.CharField(max_length=15)  # Mobile number
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(MOBILE_REGEX, message="Enter a Valid Indian Phone Number")
        ],
        null=True,
        blank=True,
    )  # Phone number
    primary = models.BooleanField(
        null=True, blank=True
    )  # To make this as primary address
    shipping = models.BooleanField(
        null=True, blank=True
    )  # To mark it as shipping address
    party = models.ForeignKey(Party, on_delete=models.CASCADE)  # Address of Patry

    def __str__(self):
        return self.party.name


# -------Purchase Models


class PurchaseOrder(models.Model):
    """This model is used to store Purchase order related information"""

    GST_CHOICES = (("I", "INTER"), ("O", "OUTER"), ("NO", "NOGST"))
    po_number = models.CharField(max_length=50)
    vendor = models.ForeignKey(Party, on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="po_address"
    )
    shipping_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="po_shipping"
    )
    date = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch, models.CASCADE)
    comment = models.TextField()
    gst_type = models.CharField(choices=GST_CHOICES, max_length=10)
    taxble_value = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    invoice_value = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return self.po_number


class PurchaseOrderItem(models.Model):
    """This model is used to store purchase order items (products info of a po)"""

    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    igst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    taxble_value = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    invoice_value = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return self.po.po_number

    def save(self, *args, **kwargs):
        self.taxble_value = self.price * self.quantity
        if self.po.gst_type == "I":
            self.sgst = (
                ((float(self.taxble_value) * float(self.product.gst_slab)) / 2) / (100)
                if self.product.gst_slab != 0
                else 0
            )
            self.cgst = (
                ((float(self.taxble_value) * float(self.product.gst_slab)) / 2) / (100)
                if self.product.gst_slab != 0
                else 0
            )
            self.igst = 0
        elif self.po.gst_type == "E":
            self.sgst = 0
            self.cgst = 0
            self.igst = (
                (float(self.taxble_value) * float(self.product.gst_slab)) / (100)
                if self.product.gst_slab != 0
                else 0
            )
        elif self.po.gst_type == "NO":
            self.sgst = 0
            self.cgst = 0
            self.igst = 0
        self.invoice_value = float(self.taxble_value) + self.sgst + self.cgst + self.igst
        super(PurchaseOrderItem, self).save(*args, **kwargs)


class Purchase(models.Model):
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    invoice_no = models.CharField(max_length=35)

    def __str__(self):
        return self.invoice_no
    

class PurchaseItem(models.Model):
    purhase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cgst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    igst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    taxble_value = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    invoice_value = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return self.po.po_number

    def save(self, *args, **kwargs):
        self.taxble_value = self.price * self.quantity
        if self.po.gst_type == "I":
            self.sgst = (
                ((float(self.taxble_value) * float(self.product.gst_slab)) / 2) / (100)
                if self.product.gst_slab != 0
                else 0
            )
            self.cgst = (
                ((float(self.taxble_value) * float(self.product.gst_slab)) / 2) / (100)
                if self.product.gst_slab != 0
                else 0
            )
            self.igst = 0
        elif self.po.gst_type == "E":
            self.sgst = 0
            self.cgst = 0
            self.igst = (
                (float(self.taxble_value) * float(self.product.gst_slab)) / (100)
                if self.product.gst_slab != 0
                else 0
            )
        elif self.po.gst_type == "NO":
            self.sgst = 0
            self.cgst = 0
            self.igst = 0
        self.invoice_value = float(self.taxble_value) + self.sgst + self.cgst + self.igst
        super(PurchaseItem, self).save(*args, **kwargs)
