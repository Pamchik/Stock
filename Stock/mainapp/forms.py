from .models import Stock
from django.forms import ModelForm, TextInput, Select, Textarea, ImageField


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'location', 'place', 'name', 'description', 'image']
        widgets = {
            'category': Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'location': Select(attrs={
                'class': 'form-control form-control-sm'
            }),
            'place': TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Введите короб'
            }),
            'name': TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Введите название'
            }),
            'description': Textarea(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Введите описание'
            })
        }


class AddQtyForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'description']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
            }),
        }