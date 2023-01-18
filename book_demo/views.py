import json
from pyexpat import model
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.urls import reverse
from bookitems.models import BookItem
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.db.models import Func, F
from django.core.paginator import Paginator
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.conf import settings

from books.models import Author, Book, Publisher
from carts.models import Cart, LineBookItem
from orders.models import Cash, Credit, DigitalWallet, Order, Payment, Shipment
from persons.models import Customer
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import serializers

# Create your views here.


class HomeView(ListView):
    context_object_name = 'bookItems1'
    queryset = BookItem.objects.filter(status=True).filter(
        book__category='Lịch sử truyền thống')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookItems2'] = BookItem.objects.filter(
            status=True).filter(book__category='Kiến thức khoa học')
        context['bookItems3'] = BookItem.objects.filter(
            status=True).filter(book__category='Văn học Việt Nam')
        context['bookItems4'] = BookItem.objects.filter(
            status=True).filter(book__category='Văn học nước ngoài')
        context['bookItems5'] = BookItem.objects.filter(
            status=True).filter(book__category='Truyện tranh')
        return context

    template_name = 'home.html'


class DetailBookView(DetailView):
    model = BookItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookItem = get_object_or_404(BookItem, pk=self.kwargs['pk'])
        print(bookItem.book.title)
        context['bookItemSames'] = BookItem.objects.filter(
            status=True, book__category=bookItem.book.category).exclude(pk=bookItem.barCode).order_by('?')
        return context

    template_name = 'detail.html'


class CategoryBookView(ListView):
    context_object_name = 'bookItems'

    def get_queryset(self):
        bookItems = BookItem.objects.filter(status=True)

        category_ = self.request.GET.get('category')
        if category_:
            bookItems = bookItems.filter(
                status=True, book__category=category_)

        author_ = self.request.GET.get('author_')
        if author_:
            bookItems = bookItems.filter(
                status=True, book__authors__id=author_)

        publisher_ = self.request.GET.get('publisher_')
        if publisher_:
            bookItems = bookItems.filter(
                status=True, book__publisher__id=publisher_)

        price_ = self.request.GET.get('price')
        if price_:
            if price_ == 'duoi50':
                bookItems = bookItems.filter(status=True).annotate(priceBought=F(
                    'price')*((100-F('discount'))/100)).filter(priceBought__lt=50000)
            if price_ == '50den100':
                bookItems = bookItems.filter(status=True).annotate(priceBought=F(
                    'price')*((100-F('discount'))/100)).filter(priceBought__gte=50000, priceBought__lt=100000)
            if price_ == '100den200':
                bookItems = bookItems.filter(status=True).annotate(priceBought=F(
                    'price')*((100-F('discount'))/100)).filter(priceBought__gte=100000, priceBought__lt=200000)
            if price_ == '200den300':
                bookItems = bookItems.filter(status=True).annotate(priceBought=F(
                    'price')*((100-F('discount'))/100)).filter(priceBought__gte=200000, priceBought__lt=300000)
            if price_ == 'tren300':
                bookItems = bookItems.filter(status=True).annotate(priceBought=F(
                    'price')*((100-F('discount'))/100)).filter(priceBought__lte=300000)

        sort_ = self.request.GET.get('sort')
        if sort_:
            if sort_ == 'low-to-high':
                bookItems = bookItems.filter(
                    status=True).annotate(priceBought=F(
                    'price')*((100-F('discount'))/100)).order_by("price")
            if sort_ == 'high-to-low':
                bookItems = bookItems.filter(
                    status=True).annotate(priceBought=F(
                    'price')*((100-F('discount'))/100)).order_by("-price")
            if sort_ == 'moi-nhat':
                bookItems = bookItems.filter(
                    status=True).order_by("-created_at")

        state_ = self.request.GET.get('state')
        if state_:
            if state_ == 'khuyen-mai':
                bookItems = bookItems.filter(
                    status=True, discount__gt=0)

        key_ = self.request.GET.get('key')
        if key_:
            bookItems = bookItems.filter(
                status=True, book__title__icontains=key_)

        p = Paginator(bookItems, 12)
        page_number = self.request.GET.get('page')
        bookItems_ = p.get_page(page_number)

        return bookItems_

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.filter(
            status=True).order_by('?')[:6]
        context['authorsAll'] = Author.objects.filter(status=True)
        context['publishers'] = Publisher.objects.filter(
            status=True).order_by('?')[:6]
        context['publishersAll'] = Publisher.objects.filter(status=True)
        key_ = self.request.GET.get('key')
        if key_:
            context['key'] = key_
        return context

    template_name = 'category.html'


class CartView(ListView):
    context_object_name = 'lineBookItems'

    def get_queryset(self):
        if 'customerLogin' in self.request.session:
            username = self.request.session['customerLogin']
            customer = Customer.objects.filter(
                status=True, account__username=username)

            orders = Order.objects.filter(customerId=customer[0].id)
            cartIds = []
            Dict = {}
            for order in orders:
                cartIds.append(order.cart.id)
            cartCurrent = Cart.objects.filter(
                customerId=customer[0].id).exclude(id__in=cartIds)
            lineBookItem = []
            if cartCurrent.count() > 0:
                lineBookItem = LineBookItem.objects.filter(
                    cart__id=cartCurrent[0].id)
                for lineItem in lineBookItem:
                    bookItem = BookItem.objects.get(
                        barCode=lineItem.bookItemBarCode)
                    Dict[lineItem] = bookItem
            print(Dict)
            return Dict

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'customerLogin' in self.request.session:
            username = self.request.session['customerLogin']
            customer = Customer.objects.filter(
                status=True, account__username=username)

            orders = Order.objects.filter(customerId=customer[0].id)
            cartIds = []
            for order in orders:
                cartIds.append(order.cart.id)
            cartCurrent = Cart.objects.filter(
                customerId=customer[0].id).exclude(id__in=cartIds)
            if cartCurrent.count() > 0:
                context['cart'] = cartCurrent[0]
            return context
    template_name = 'cart.html'


class CheckoutView(ListView):
    context_object_name = 'lineBookItems'

    def get_queryset(self):
        if 'customerLogin' in self.request.session:
            username = self.request.session['customerLogin']
            customer = Customer.objects.filter(
                status=True, account__username=username)

            orders = Order.objects.filter(customerId=customer[0].id)
            cartIds = []
            Dict = {}
            for order in orders:
                cartIds.append(order.cart.id)
            cartCurrent = Cart.objects.filter(
                customerId=customer[0].id).exclude(id__in=cartIds)
            lineBookItem = []
            if cartCurrent.count() > 0:
                lineBookItem = LineBookItem.objects.filter(
                    cart__id=cartCurrent[0].id)
                for lineItem in lineBookItem:
                    bookItem = BookItem.objects.get(
                        barCode=lineItem.bookItemBarCode)
                    Dict[lineItem] = bookItem
            print(Dict)
            return Dict

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'customerLogin' in self.request.session:
            username = self.request.session['customerLogin']
            customer = Customer.objects.filter(
                status=True, account__username=username)
            context['customer'] = customer[0]

            shipments = Shipment.objects.filter(status__in=[True])
            context['shipments'] = shipments
            context['defaultPriceShipment'] = shipments[0].price

            orders = Order.objects.filter(customerId=customer[0].id)
            cartIds = []
            for order in orders:
                cartIds.append(order.cart.id)
            cartCurrent = Cart.objects.filter(
                customerId=customer[0].id).exclude(id__in=cartIds)
            if cartCurrent.count() > 0:
                context['cart'] = cartCurrent[0]
            return context

    template_name = 'checkout.html'


def checkout(request):
    shipmentId = request.POST.get('shipmentId')
    paymentType = request.POST.get('paymentType')
    ccname = request.POST.get('cc-name')
    ccnumber = request.POST.get('cc-number')
    ccexpiration = request.POST.get('cc-expiration')
    paymentWith = request.POST.get('paymentWith')

    username = request.session['customerLogin']
    customer = Customer.objects.filter(status=True, account__username=username)[0]

    orders = Order.objects.filter(customerId=customer.id)
    cartIds = []
    for order in orders:
        cartIds.append(order.cart.id)
    cartCurrent = Cart.objects.filter(
            customerId=customer.id).exclude(id__in=cartIds)[0]
    shipment = Shipment.objects.get(id=int(shipmentId))
    order = Order(cart = cartCurrent,status='Đã giao hàng',shipment=shipment,customerId=customer.id)
    
    if(paymentWith=='Cash'):
        total = cartCurrent.totalAmount+shipment.price
        cash = Cash(totalMoney= total,cashTendered=total)
        cash.save()
        order.payment = cash

    if(paymentWith=='Credit'):
        total = cartCurrent.totalAmount+shipment.price
        credit = Credit(totalMoney= total,number=ccnumber,type=ccname,date=ccexpiration)
        credit.save()
        order.payment = credit

    if(paymentWith=='DigitalWallet'):
        total = cartCurrent.totalAmount+shipment.price
        digitalWallet = DigitalWallet(totalMoney= total,name=paymentType)
        digitalWallet.save()
        order.payment = digitalWallet

        request.session['orderNow'] = serializers.serialize('json', [order])

        return redirect('process_payment')

    customer.point = customer.point + order.payment.totalMoney* 0.009
    order.save()
    customer.save()
    del request.session['totalQuantity']

    sendingMail(request, order)

    context = {
        'status': 'success',
    }

    return render(request, 'cart.html', context)

class MyOrderView(ListView):
    context_object_name = 'myorders'

    def get_queryset(self):
        if 'customerLogin' in self.request.session:
            username = self.request.session['customerLogin']
            customer = Customer.objects.filter(
                status=True, account__username=username)

            orders = Order.objects.filter(customerId=customer[0].id)
            Dict = {}
            for order in orders:
                Dict1 = {}
                lineBookItem = []
                lineBookItem = LineBookItem.objects.filter(cart__id=order.cart.id)
                for lineItem in lineBookItem:
                    bookItem = BookItem.objects.get(barCode=lineItem.bookItemBarCode)
                    Dict1[lineItem] = bookItem
                Dict[order]=Dict1
            print(Dict)
            return Dict

    template_name = 'myorder.html'

def sendingMail(request,order):
    if 'customerLogin' in request.session:
        username = request.session['customerLogin']
        customer = Customer.objects.filter(status=True, account__username=username)[0]

        mapLineItem = {}
        lineBookItem = LineBookItem.objects.filter(cart__id=order.cart.id)
        for lineItem in lineBookItem:
            bookItem = BookItem.objects.get(barCode=lineItem.bookItemBarCode)
            mapLineItem[lineItem] = bookItem

        subject, from_email, to = 'HÓA ĐƠN BOOK '+ str(order.created_at), 'computercuongpham999@gmail.com', customer.email
        html_content = render_to_string("email_template.html",{
            'order':order,
            'customer':customer,
            'mapLineItem':mapLineItem
        })
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def process_payment(request):
    host = request.get_host()
    orderNow = request.session['orderNow']
    orders = json.loads(orderNow)
    payment = Payment.objects.get(id=orders[0]['fields']['payment'])
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': payment.totalMoney/21000,
        'item_name': 'Order {}'.format(get_random_string(length=14)),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'form': form})


@csrf_exempt
def payment_done(request):
    orderNow = request.session['orderNow']
    orders = json.loads(orderNow)
    cart = Cart.objects.get(id=orders[0]['fields']['cart'])
    payment = Payment.objects.get(id=orders[0]['fields']['payment'])
    shipment = Shipment.objects.get(id=orders[0]['fields']['shipment'])
    order = Order(status = orders[0]['fields']['status'],cart = cart, payment = payment, shipment = shipment, customerId = orders[0]['fields']['customerId'])

    order.save()

    username = request.session['customerLogin']
    customer = Customer.objects.filter(status=True, account__username=username)[0]
    customer.point = customer.point + order.payment.totalMoney* 0.009
    customer.save()
    del request.session['totalQuantity']

    sendingMail(request, order)

    context = {
        'status': 'success',
    }

    return render(request, 'cart.html', context)


@csrf_exempt
def payment_canceled(request):
    return redirect('checkout')
