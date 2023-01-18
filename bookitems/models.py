from django.db import models
from django.urls import reverse
from books.models import Book

# Create your models here.
class BookItem(models.Model):
    barCode = models.CharField(max_length=255, primary_key=True)
    book = models.OneToOneField(Book, on_delete=models.RESTRICT)
    price = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    img = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.book.title+" | "+str(self.price)+" | "+str(self.discount)

    def get_absolute_url(self):
        return reverse("manage_bookitem")