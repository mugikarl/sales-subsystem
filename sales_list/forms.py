from django import forms
from .models import MenuItem, OrderDetail

class MenuForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price']

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ['menu_item','quantity']