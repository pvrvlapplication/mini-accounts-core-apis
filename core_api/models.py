from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import datetime
from django.db.models import Sum

GST_REGEX = "\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}"
MOBILE_REGEX = "\+?\d[\d -]{8,12}\d"
PAN_REGEX = "[A-Z]{5}\d{4}[A-Z]{1}"
GST_CHOICES = (("I", "INTER"), ("O", "OUTER"), ("NO", "NOGST"))
TRANSACTION_TYPE_CHOICES = (("BK", "BANK"), ("CQ", "CHEQUE"), ("CA", "CASH"), ("UPI", "UPI"))


class Company(models.Model):
    """This model is to store Company Details of an user."""

    COMPANY_TYPE_CHOICES = (
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
    )
    name = models.CharField(max_length=100, unique=True)  # Company Name
    # type = models.CharField(choices=COMPANY_TYPE_CHOICES, max_length=15)
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
        unique=True,
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
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True
    )  # Company
    mobile = models.CharField(max_length=12)  # Mobile number
    # role = models.CharField(choices=USER_ROLES, max_length=15)  # role of the user

    def __str__(self):
        return self.username


# -------Product Models


class Product(models.Model):
    """This model is used to store products"""

    GST_SLABS = ((0, 0), (5, 5), (12, 12), (18, 18), (28, 28))
    name = models.CharField(max_length=20)  # Name of the product
    gst_slab = models.CharField(choices=GST_SLABS, max_length=5)  # GST Slab Percentage.
    hsn = models.CharField(max_length=35)  # Hsn code
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user

    class Meta:
        unique_together = ('name', 'user',)

    def __str__(self):
        return self.name


# -------Service Models


class Service(models.Model):
    """This model is used to store services"""

    GST_SLABS = ((0, 0), (5, 5), (12, 12), (18, 18), (28, 28))
    name = models.CharField(max_length=20)  # Name of the product
    gst_slab = models.CharField(choices=GST_SLABS, max_length=5)  # GST Slab Percentage.
    hsn = models.CharField(max_length=35)  # Hsn code
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user

    class Meta:
        unique_together = ('name', 'user',)

    def __str__(self):
        return self.name



# -------Customer & Vendor Models


class Party(models.Model):
    """This model is used to store customer and vendor information"""

    PARTY_TYPE = (("C", "CUSTOMER"), ("V", "VENDOR"))
    name = models.CharField(max_length=50)  # Name of the party
    gst = models.CharField(
        max_length=20,
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

    class Meta:
        unique_together = (('name', 'user',), ('gst', 'user'), ('pan', 'user'))

    def __str__(self):
        return self.name


class Address(models.Model):
    """This model is used to store address(es) of the customers and vendors"""

    ADDRESS_OPTIONS = (("HM", "HOME"), ("BU", "BUSINESS"), ("BI", "BILLING"), ("SH", "SHIPPING"))

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
    address_type = models.CharField(choices=ADDRESS_OPTIONS, max_length=3) # Type of Address

    def __str__(self):
        return self.party.name


# -------Purchase Models


class Purchase(models.Model):
    
    vendor = models.ForeignKey(Party, on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="po_address"
    )
    shipping_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="po_shipping"
    )
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    gst_type = models.CharField(choices=GST_CHOICES, max_length=10)
    invoice_no = models.CharField(max_length=35)

    def __str__(self):
        return str(self.invoice_no)
    
    def taxble_value(self):
        return PurchaseItem.objects.filter(purchase__id=self.id).aggregate(Sum('taxble_value'))
    
    def invoice_value(self):
        return PurchaseItem.objects.filter(purchase__id=self.id).aggregate(Sum('invoice_value'))


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
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
        return str(self.id)

    def save(self, *args, **kwargs):
        self.taxble_value = self.price * self.quantity
        if self.purchase.gst_type == "I":
            self.sgst = (
                ((float(self.taxble_value) * float(self.product.gst_slab)) / 2) / (100)
                if self.product.gst_slab != 0
                else 0.0
            )
            self.cgst = (
                ((float(self.taxble_value) * float(self.product.gst_slab)) / 2) / (100)
                if self.product.gst_slab != 0
                else 0.0
            )
            self.igst = 0.0
        elif self.purchase.gst_type == "E":
            self.sgst = 0.0
            self.cgst = 0.0
            self.igst = (
                (float(self.taxble_value) * float(self.product.gst_slab)) / (100)
                if self.product.gst_slab != 0
                else 0.0
            )
        elif self.purchase.gst_type == "NO":
            self.sgst = 0.0
            self.cgst = 0.0
            self.igst = 0.0
        self.invoice_value = float(self.taxble_value) +  float(self.igst) + float(self.sgst) + float(self.cgst)
        super(PurchaseItem, self).save(*args, **kwargs)


# -------Sale Models


class Sale(models.Model):
    """To store sales objects"""

    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="so_address"
    )
    shipping_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="so_shipping"
    )
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    gst_type = models.CharField(choices=GST_CHOICES, max_length=10)
    invoice_no = models.CharField(max_length=35)

    def __str__(self):
        return self.invoice_no

    def taxble_value(self):
        return SaleItem.objects.filter(sale__id=self.id).aggregate(Sum('taxble_value'))
    
    def invoice_value(self):
        return SaleItem.objects.filter(sale__id=self.id).aggregate(Sum('invoice_value'))


class SaleItem(models.Model):
    """To store sale objects product items"""

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
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
        return self.sale.invoice_no

    def save(self, *args, **kwargs):
        self.taxble_value = self.price * self.quantity
        if self.sale.gst_type == "I":
            self.sgst = (
                ((float(self.taxble_value) * float(self.product.gst_slab)) / 2) / (100)
                if self.product.gst_slab != 0
                else 0.0
            )
            self.cgst = (
                ((float(self.taxble_value) * float(self.product.gst_slab)) / 2) / (100)
                if self.product.gst_slab != 0
                else 0.0
            )
            self.igst = 0.0
        elif self.sale.gst_type == "O":
            self.sgst = 0.0
            self.cgst = 0.0
            self.igst = (
                (float(self.taxble_value) * float(self.product.gst_slab)) / (100)
                if self.product.gst_slab != 0
                else 0.0
            )
        elif self.sale.gst_type == "NO":
            self.sgst = 0.0
            self.cgst = 0.0
            self.igst = 0.0
        self.invoice_value = float(self.taxble_value) + float(self.igst) + float(self.sgst) + float(self.cgst)
        super(SaleItem, self).save(*args, **kwargs)

# -------Bank Models

class Bank(models.Model):
    """This model is used to store bank details."""
    name = models.CharField(max_length=50)
    account_no = models.CharField(max_length=25)
    ifsc = models.CharField(max_length=11)
    branch = models.CharField(max_length=25)
    address = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('name', 'account_no', 'user'), ('account_no', 'user'))

    def __str__(self):
        return self.name

class PartyBank(models.Model):
    """This model is used to store bank details."""
    name = models.CharField(max_length=50)
    account_no = models.CharField(max_length=25)
    ifsc = models.CharField(max_length=11)
    branch = models.CharField(max_length=25)
    address = models.CharField(max_length=50)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('name', 'account_no', 'party'), ('account_no', 'party'))

    def __str__(self):
        return self.name

# -------Receipt Models

class Receipt(models.Model):

    """This model is used to store receipt details."""

    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True, null=True)
    cheque_no = models.CharField(max_length=20, blank=True, null=True)
    tran_type = models.CharField(choices=TRANSACTION_TYPE_CHOICES, max_length=3)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

# -------Payment Models

class Payment(models.Model):

    """This model is used to store payment details."""

    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    our_bank = models.ForeignKey(Bank, on_delete=models.CASCADE, blank=True, null=True, related_name="our_bank")
    party_bank = models.ForeignKey(PartyBank, on_delete=models.CASCADE, blank=True, null=True, related_name="party_bank")
    cheque_no = models.CharField(max_length=20, blank=True, null=True)
    tran_type = models.CharField(choices=TRANSACTION_TYPE_CHOICES, max_length=3)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)