from django.urls import path

from . import views

urlpatterns = [
    path('add', views.AddBookItemView.as_view(), name='add_bookitem'),
    path('', views.ManageBookItemView.as_view(), name='manage_bookitem'),
    path('edit/<pk>', views.EditBookItemView.as_view(), name='edit_bookitem'),
    path('delete/<pk>', views.deleteBookItem, name='delete_bookitem'),
]