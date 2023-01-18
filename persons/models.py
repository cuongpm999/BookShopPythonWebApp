from django.db import models

# Create your models here.
class FullName(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    middleName = models.CharField(max_length=255)
    
    def __str__(self):
        return self.firstName

class Address(models.Model):
    number = models.IntegerField(default=0)
    street = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    
    def __str__(self):
        return self.city

class Account(models.Model):
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.username

class Person(models.Model):
    mobile = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)
    dateOfBirth = models.DateField()
    email = models.CharField(max_length=255,unique=True)
    fullName = models.OneToOneField(FullName, on_delete=models.RESTRICT)
    address = models.OneToOneField(Address, on_delete=models.RESTRICT)
    account = models.OneToOneField(Account, on_delete=models.RESTRICT)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.fullName.firstName

class Customer(Person):
    point = models.FloatField(default=0)
    note = models.TextField(null=True,blank = True)

    def __str__(self):
        return self.fullName.firstName