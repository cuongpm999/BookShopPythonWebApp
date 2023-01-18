from django.contrib import admin

from carts.models import Cart, LineBookItem

# Register your models here.
admin.site.register(Cart)
admin.site.register(LineBookItem)