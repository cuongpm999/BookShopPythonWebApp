from pyexpat import model
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BookForm
from .models import Book
from django.views.generic import ListView, CreateView, UpdateView, DetailView

# Create your views here.

class ManageView(ListView):
    context_object_name = 'books'
    queryset = Book.objects.all()
    template_name = 'books/index.html'

class AddBookView(CreateView):
    form_class = BookForm
    template_name = 'books/add_edit.html'

class EditBookView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/add_edit.html'

def deleteBook(request,pk):
    Book.objects.get(id=pk).delete()
    return redirect('books:manage')
