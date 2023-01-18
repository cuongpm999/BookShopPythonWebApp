from django import forms

from books.models import Book
from .models import BookItem
from django.utils.crypto import get_random_string

class BookItemForm(forms.ModelForm):
    class Meta:
        model = BookItem
        fields = ['barCode', 'book', 'price', 'discount', 'img']
        widgets = {
            'barCode': forms.TextInput(attrs={'class': 'form-control','readOnly': True}),
            'book': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.fields['book'].empty_label = None
        self.fields['book'].queryset = Book.objects.filter(status=True)
        self.fields['barCode'].initial = get_random_string(length=14)


class BookItemUpdateForm(forms.ModelForm):
    class Meta:
        model = BookItem
        fields = ['barCode', 'price', 'discount', 'img']
        widgets = {
            'barCode': forms.TextInput(attrs={'class': 'form-control', 'readOnly': True}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
