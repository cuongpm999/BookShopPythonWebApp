from django import forms
from .models import Address, FullName, Account, Customer

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address

        fields = ['number', 'street', 'district', 'city']
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FullNameForm(forms.ModelForm):
    class Meta:
        model = FullName

        fields = ['firstName', 'lastName', 'middleName']
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'middleName': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account

        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer

        fields = ['mobile', 'sex', 'dateOfBirth', 'email', 'note']
        widgets = {
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(choices=(("Nam", "Nam"),("Nữ", "Nữ"),), attrs={'class': 'form-control'}),
            'dateOfBirth': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control','type': 'date'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer

        fields = ['id', 'mobile', 'sex', 'dateOfBirth', 'note']
        widgets = {
            'id': forms.NumberInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(choices=(("Nam", "Nam"),("Nữ", "Nữ"),), attrs={'class': 'form-control'}),
            'dateOfBirth': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control','type': 'date'}),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
        }

