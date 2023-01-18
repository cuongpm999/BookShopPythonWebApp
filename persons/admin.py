from django.contrib import admin

from persons.models import Account, Address, Customer, FullName, Person

# Register your models here.
admin.site.register(FullName)
admin.site.register(Address)
admin.site.register(Account)
admin.site.register(Person)
admin.site.register(Customer)