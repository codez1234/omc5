
from pyexpat import model
from django.db import models

# Create your models here.

# note To define a many-to-one relationship, use ForeignKey:


class One(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.IntegerField()
    two = models.ForeignKey("Two", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Two(models.Model):
    place = models.CharField(max_length=100)
    place_id = models.IntegerField()

    def __str__(self) -> str:
        return self.place

# To define a many-to-many relationship, use ManyToManyField.


class Three(models.Model):
    name = models.CharField(max_length=100)
    two = models.ManyToManyField(Two)

    def __str__(self) -> str:
        return self.name


class Four(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Voucher(models.Model):
    name = models.CharField(max_length=100)
    code = models.ForeignKey(
        'VoucherCustomer', related_name='voucher_code', on_delete=models.CASCADE)


class VoucherCustomer(models.Model):
    customer_id = models.IntegerField()
