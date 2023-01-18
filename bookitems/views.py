from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .forms import BookItemForm,BookItemUpdateForm
from .models import BookItem

# Create your views here.
class AddBookItemView(CreateView):
    form_class = BookItemForm
    template_name = 'manage/bookitems/add_edit.html'

class ManageBookItemView(ListView):
    context_object_name = 'bookitems'
    queryset = BookItem.objects.filter(status=True)
    template_name = 'manage/bookitems/index.html'

class EditBookItemView(UpdateView):
    model = BookItem
    form_class = BookItemUpdateForm
    template_name = 'manage/bookitems/add_edit.html'

def deleteBookItem(request,pk):
    bookitem = BookItem.objects.get(barCode=pk)
    bookitem.status = False
    bookitem.save()
    return redirect('manage_bookitem')