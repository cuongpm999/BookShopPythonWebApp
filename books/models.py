from unicodedata import name
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher, on_delete=models.RESTRICT)
    authors = models.ManyToManyField(Author)
    pages = models.IntegerField(default=0)
    language = models.CharField(max_length=255)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("books:manage_book")

    # def save(self, *args, **kwargs):
    #     barCode = get_random_string(length=32)
    #     return super(BookItem, self).save(*args, **kwargs)
