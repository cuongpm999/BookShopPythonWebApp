from django.urls import path

from . import views

urlpatterns = [
    path('shipment/select/', views.SelectShipment.as_view()),
]