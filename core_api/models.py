from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Company(models.Model):
    '''This model is to store Company Details of an user.'''
    COMPANY_TYPE_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )
    name = models.CharField(max_length=100, unique=True) # Company Name
    #type = models.CharField(choices=COMPANY_TYPE_CHOICES, max_length=15)

    def __str__(self):
        return self.name
    

class Branch(models.Model):
    '''This models is to store branch details of a company.'''
    GST_REGEX = '\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}'
    MOBILE_REGEX = '\+?\d[\d -]{8,12}\d'
    PAN_REGEX = '[A-Z]{5}\d{4}[A-Z]{1}'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True) # Company
    name = models.CharField(max_length=50) # Branch name
    dno = models.CharField(max_length=30) # Door number, Building name
    area = models.CharField(max_length=30) # Village name
    city = models.CharField(max_length=30) # City name
    district = models.CharField(max_length=25) # District name
    state = models.CharField(max_length=20) # State name
    country = models.CharField(max_length=20) # Country name
    gst = models.CharField(max_length=20, unique=True, validators=[RegexValidator(GST_REGEX, message="Enter a Valid Indian GST Number")]) # GST number  22AAAAA0000A1Z5
    mobile = models.CharField(max_length=15) # Mobile number
    phone = models.CharField(max_length=15, validators=[RegexValidator(MOBILE_REGEX, message="Enter a Valid Indian Phone Number")]) # Phone number
    pan = models.CharField(max_length=15, validators=[RegexValidator(PAN_REGEX, message="Enter a Valid PAN Number")]) # Pan number "AAAAA1111A"

    def __str__(self):
        return self.name


class User(AbstractUser):
    '''This model is extension of default user model.'''
    USER_ROLES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True) # Branch
    mobile = models.CharField(max_length=12) # Mobile number
    role = models.CharField(choices=USER_ROLES, max_length=15) # role of the user
