import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bookitems.models import BookItem

from carts.forms import ApiSerializer
from carts.models import Cart, LineBookItem
from orders.models import Order
from persons.models import Customer

# Create your views here.
class AddToCart(APIView):
    def post(self, request, format=None):
        serializer = ApiSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            if 'customerLogin' in request.session:
                username = request.session['customerLogin']
                customer = Customer.objects.filter(status=True,account__username=username)

                orders = Order.objects.filter(customerId = customer[0].id)
                cartIds = []
                for order in orders:
                    cartIds.append(order.cart.id)
                cartCurrent = Cart.objects.filter(customerId = customer[0].id).exclude(id__in=cartIds)
                if cartCurrent.count() == 0:
                    cart = Cart(customerId = customer[0].id)
                    cart.save()

                cartCurrent = Cart.objects.filter(customerId = customer[0].id).exclude(id__in=cartIds)
                cartCurrent_ = cartCurrent[0]

                barCode_ = json.loads(json.dumps(serializer.data))['barCode']
                lineBookItem = LineBookItem.objects.filter(cart__id=cartCurrent_.id,bookItemBarCode=barCode_)
                print(lineBookItem.count())
                if lineBookItem.count() == 0:
                    lineBookItemNew = LineBookItem(quanity=1,cart=cartCurrent_,bookItemBarCode=barCode_)
                    lineBookItemNew.save()
                else:
                    quanity=lineBookItem[0].quanity+1
                    lineBookItemNew=lineBookItem[0]
                    lineBookItemNew.quanity=quanity
                    lineBookItemNew.save()

                bookItem = BookItem.objects.filter(status=True,barCode=barCode_)[0]
                
                cartCurrent_.totalAmount=cartCurrent_.totalAmount+bookItem.price*(100-bookItem.discount)/100
                cartCurrent_.save()
                
                lineBookItem = LineBookItem.objects.filter(cart__id=cartCurrent[0].id)
                totalQuantity = 0
                for lineItem in lineBookItem:
                    totalQuantity += lineItem.quanity
                print(totalQuantity)
                request.session['totalQuantity'] = totalQuantity

                serializer = ApiSerializer({'barCode': barCode_,'totalQuantity':totalQuantity})
            else:
                serializer = ApiSerializer({'barCode': 'login'})
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteCart(APIView):
    def post(self, request, format=None):
        serializer = ApiSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            if 'customerLogin' in request.session:
                username = request.session['customerLogin']
                customer = Customer.objects.filter(status=True,account__username=username)

                orders = Order.objects.filter(customerId = customer[0].id)
                cartIds = []
                for order in orders:
                    cartIds.append(order.cart.id)
                cartCurrent = Cart.objects.filter(customerId = customer[0].id).exclude(id__in=cartIds)

                barCode_ = json.loads(json.dumps(serializer.data))['barCode']
                lIBDelete = LineBookItem.objects.filter(cart__id=cartCurrent[0].id,bookItemBarCode=barCode_)[0]
                lIBDelete.delete()

                lineBookItem = LineBookItem.objects.filter(cart__id=cartCurrent[0].id)
                
                totalQuantity = 0
                totalAmount = 0
                for lineItem in lineBookItem:
                    totalQuantity += lineItem.quanity
                    bookItem = BookItem.objects.get(barCode=lineItem.bookItemBarCode)
                    totalAmount = totalAmount + lineItem.quanity*bookItem.price*(100-bookItem.discount)/100
                cartCurrent_ = cartCurrent[0]
                cartCurrent_.totalAmount=totalAmount
                cartCurrent_.save()
                
                if(LineBookItem.objects.filter(cart__id=cartCurrent[0].id).count() == 0):
                    cartCurrent_.delete()

                request.session['totalQuantity'] = totalQuantity

                serializer = ApiSerializer({'barCode': barCode_})
            else:
                serializer = ApiSerializer({'barCode': 'login'})
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditCart(APIView):
    def post(self, request, format=None):
        serializer = ApiSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            if 'customerLogin' in request.session:
                username = request.session['customerLogin']
                customer = Customer.objects.filter(status=True,account__username=username)

                orders = Order.objects.filter(customerId = customer[0].id)
                cartIds = []
                for order in orders:
                    cartIds.append(order.cart.id)
                cartCurrent = Cart.objects.filter(customerId = customer[0].id).exclude(id__in=cartIds)

                barCode_ = json.loads(json.dumps(serializer.data))['barCode']
                quantity_ = json.loads(json.dumps(serializer.data))['quantity']
                lIBUpdate = LineBookItem.objects.filter(cart__id=cartCurrent[0].id,bookItemBarCode=barCode_)[0]
                lIBUpdate.quanity = quantity_
                lIBUpdate.save()

                lineBookItem = LineBookItem.objects.filter(cart__id=cartCurrent[0].id)
                
                totalQuantity = 0
                totalAmount = 0
                for lineItem in lineBookItem:
                    totalQuantity += lineItem.quanity
                    bookItem = BookItem.objects.get(barCode=lineItem.bookItemBarCode)
                    totalAmount = totalAmount + lineItem.quanity*bookItem.price*(100-bookItem.discount)/100
                cartCurrent_ = cartCurrent[0]
                cartCurrent_.totalAmount=totalAmount
                cartCurrent_.save()

                lineItem = LineBookItem.objects.filter(cart__id=cartCurrent[0].id,bookItemBarCode=barCode_)[0]
                price = lineItem.quanity*bookItem.price*(100-bookItem.discount)/100
                
                request.session['totalQuantity'] = totalQuantity

                serializer = ApiSerializer({'barCode': barCode_,'totalQuantity':totalQuantity,'price':price,'totalAmount':totalAmount})
            else:
                serializer = ApiSerializer({'barCode': 'login'})
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)