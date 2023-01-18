"""book_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from persons.views import RegisterView, LoginView, logout, ProfileView, EditProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manage/book/', include('books.urls')),
    path('manage/book-item/', include('bookitems.urls')),
    path('rest/api/cart/', include('carts.urls')),
    path('rest/api/order/', include('orders.urls')),
    path('', views.HomeView.as_view(), name='home'),
    path('book-detail/<pk>', views.DetailBookView.as_view(), name='detail'),
    path('collections/', views.CategoryBookView.as_view(), name='collection'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/post', views.checkout, name='checkout_post'),
    path('my-order/', views.MyOrderView.as_view(), name='myorder'),
    path('view-profile/', ProfileView.as_view(), name='view_profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('paypal/', include('paypal.standard.ipn.urls')),

    path('order/paypal/process-payment/', views.process_payment, name='process_payment'),
    path('order/paypal/payment-done/', views.payment_done, name='payment_done'),
    path('order/paypal/payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
