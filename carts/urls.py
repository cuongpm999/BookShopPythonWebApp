from django.urls import path

from . import views

urlpatterns = [
    path('addToCart/', views.AddToCart.as_view()),
    path('deleteCart/', views.DeleteCart.as_view()),
    path('editCart/', views.EditCart.as_view()),
]