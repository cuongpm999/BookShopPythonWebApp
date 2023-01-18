from django.shortcuts import redirect, render
from django.views import View
from carts.models import Cart, LineBookItem
from orders.models import Order
from django.views.generic import ListView

from persons.forms import AccountForm, AddressForm, CustomerEditForm, CustomerForm, FullNameForm
from persons.models import Customer
from django.core import serializers

# Create your views here.

class RegisterView(View):
    def get(self, request):
        context = {
            'address': AddressForm,
            'fullName': FullNameForm,
            'account': AccountForm,
            'customer': CustomerForm,
        }
        return render(request, 'register.html', context)

    def post(self, request):
        address = AddressForm(request.POST)
        fullName = FullNameForm(request.POST)
        account = AccountForm(request.POST)
        customer = CustomerForm(request.POST)

        if account.is_valid():  
            account_save = account.save()
        else:
            context = {
                'status':'faileTenBiTrung',
                'address': AddressForm,
                'fullName': FullNameForm,
                'account': AccountForm,
                'customer': CustomerForm,
            }
            return render(request, 'register.html', context)
        if customer.is_valid():
            print('Email is valid')
        else:
            context = {
                'status':'faileEmailBiTrung',
                'address': AddressForm,
                'fullName': FullNameForm,
                'account': AccountForm,
                'customer': CustomerForm,
            }
            return render(request, 'register.html', context)

        if address.is_valid():
            address_save=address.save()
        if fullName.is_valid():
            fullName_save = fullName.save()
        
        if customer.is_valid():
            customer = customer.save(commit=False)
            customer_save = Customer(address=address_save,fullName = fullName_save,account=account_save,mobile=customer.mobile,
            sex=customer.sex,dateOfBirth=customer.dateOfBirth,email=customer.email,note=customer.note)
            customer_save.save()
        return redirect('home')


class LoginView(View):
    def get(self, request):
        context = {
            
        }
        return render(request, 'login.html', context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        customer = Customer.objects.filter(status=True,account__username=username,account__password=password)
        if(customer):
            request.session['customerLogin'] = username

            customer = Customer.objects.filter(status=True,account__username=username)

            orders = Order.objects.filter(customerId = customer[0].id)
            cartIds = []
            for order in orders:
                cartIds.append(order.cart.id)
            cartCurrent = Cart.objects.filter(customerId = customer[0].id).exclude(id__in=cartIds)
            if cartCurrent.count() > 0:
                lineBookItem = LineBookItem.objects.filter(cart__id=cartCurrent[0].id)
                totalQuantity = 0
                for lineItem in lineBookItem:
                    totalQuantity += lineItem.quanity
                print(totalQuantity)
                request.session['totalQuantity'] = totalQuantity

            return redirect('home')
        else:
            context = {
                "status":"failed"
            }
            return render(request, 'login.html', context)

def logout(request):
    del request.session['customerLogin']
    if 'totalQuantity' in request.session:
        del request.session['totalQuantity']
    return redirect('home')

class ProfileView(ListView):
    context_object_name = 'customer'
    def get_queryset(self):
        if 'customerLogin' in self.request.session:
            username = self.request.session['customerLogin']
            customer = Customer.objects.filter(status=True, account__username=username)[0]
            return customer

    template_name = 'view_profile.html'

class EditProfileView(View):
    def get(self, request):
        username = self.request.session['customerLogin']
        customer = Customer.objects.filter(
                status=True, account__username=username)[0]
        context = {
            'addressForm': AddressForm(instance=customer.address),
            'fullNameForm': FullNameForm(instance=customer.fullName),
            'customerForm': CustomerEditForm(instance=customer)
        }
        return render(request, 'edit_profile.html', context)

    def post(self, request):
        username = self.request.session['customerLogin']
        customer = Customer.objects.filter(
                status=True, account__username=username)[0]
        
        address = AddressForm(request.POST,instance=customer.address)
        fullName = FullNameForm(request.POST,instance=customer.fullName)
        customer = CustomerForm(request.POST,instance=customer)

        if address.is_valid():
            address.save()
        if fullName.is_valid():
            fullName.save()
        
        if customer.is_valid():
            customer.save()
        return redirect('view_profile')