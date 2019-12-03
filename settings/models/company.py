from django.db import models
from helpers.models import Model

STATUS_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive')
)


class Country(Model):
    code = models.CharField(max_length=11, blank=True, null=True)
    name = models.CharField(max_length=255, null=True)
    dial_code = models.CharField(max_length=255, null=True)
    currency = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class State(Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class City(Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Company(Model):
    OWNERSHIP_TYPE_CHOICE = (
        ('public-limited', 'Public Limited'),
        ('public-limited', 'Joint Venture'),
        ('public-limited', 'Proprietor'),
        ('public-limited', 'Private Limited'),
        ('public-limited', 'Partnership'),
        ('public-limited', 'Others'),
    )
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=100)
    ownership_type = models.CharField(max_length=20, choices=OWNERSHIP_TYPE_CHOICE)
    establishment_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    company_start_date = models.DateField(blank=True, null=True)
    company_end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'


class CompanyPhysicalAddress(Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    address_start_date = models.DateField(blank=True, null=True)
    address_end_date = models.DateField(blank=True, null=True)
