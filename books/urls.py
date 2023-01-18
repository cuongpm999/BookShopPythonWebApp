from django.urls import path

from . import views

app_name = 'books'

urlpatterns = [
    path('', views.ManageBookView.as_view(), name='manage_book'),
    path('add/', views.AddBookView.as_view(), name='add_book'),
    path('edit/<int:pk>', views.EditBookView.as_view(), name='edit_book'),
    path('delete/<int:pk>', views.deleteBook, name='delete_book'),
]