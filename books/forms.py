from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','category','publisher','authors','pages','language','summary']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'publisher':forms.Select(attrs={'class':'form-control'}),
            'authors':forms.SelectMultiple(attrs={'class':'form-control'}),
            'pages':forms.NumberInput(attrs={'class':'form-control'}),
            'language':forms.TextInput(attrs={'class':'form-control'}),
            'summary':forms.Textarea(attrs={'class':'form-control'}),
        }
    
    def __init__(self, *args, **kargs):
            super().__init__(*args, **kargs)
            self.fields['category'].empty_label = None
            self.fields['publisher'].empty_label = None
            self.fields['authors'].empty_label = None
            # self.fields['publisher'].queryset = Publisher.objects.filter(status=True)
    
