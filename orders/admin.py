from django.contrib import admin

# Register your models here.
from .models import Payment, Cash, DigitalWallet, Credit, Shipment, Order

admin.site.register(Payment)
admin.site.register(Cash)
admin.site.register(DigitalWallet)
admin.site.register(Credit)
admin.site.register(Shipment)
admin.site.register(Order)