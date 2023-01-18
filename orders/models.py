from django.db import models

from carts.models import Cart

# Create your models here.
class Payment(models.Model):
    totalMoney = models.FloatField(default=0)
    def __str__(self):
        return str(self.totalMoney)

class Cash(Payment):
    cashTendered = models.FloatField(default=0)
    def __str__(self):
        return str(self.cashTendered)

class DigitalWallet(Payment):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Credit(Payment):
    number = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    def __str__(self):
        return self.number+" | "+self.type+" | "+self.date

class Shipment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    address = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name+" | "+self.address

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=255)
    cart = models.OneToOneField(Cart, on_delete=models.RESTRICT)
    payment = models.OneToOneField(Payment, on_delete=models.RESTRICT)
    shipment = models.ForeignKey(Shipment, on_delete=models.RESTRICT)
    customerId = models.IntegerField(default=0)

    def __str__(self):
        return str(self.created_at)+" | "+str(self.customerId)