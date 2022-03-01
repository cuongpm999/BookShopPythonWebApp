from django.urls import path

from . import views

app_name = 'books'

urlpatterns = [
    path('', views.ManageView.as_view(), name='manage'),
    path('add/', views.AddBookView.as_view(), name='add'),
    path('edit/<int:pk>', views.EditBookView.as_view(), name='edit'),
    path('delete/<int:pk>', views.deleteBook, name='delete'),
]