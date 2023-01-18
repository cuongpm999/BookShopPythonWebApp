from django.db import models

# Create your models here.
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    totalAmount =  models.FloatField(default=0)
    customerId = models.IntegerField(default=0)

    def __str__(self):
        return str(self.created_at)+" | "+str(self.totalAmount)
        
class LineBookItem(models.Model):
    quanity = models.IntegerField(default=0)
    cart = models.ForeignKey(Cart, on_delete=models.RESTRICT)
    bookItemBarCode = models.CharField(max_length=255)

    def __str__(self):
        return self.bookItemBarCode+" | "+str(self.quanity)