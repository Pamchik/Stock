from .models import Product, Transaction, Status, Direction
from django import forms
from django.forms import ModelForm, TextInput, Select, Textarea, ClearableFileInput, CharField

class ProductForm(ModelForm):

    class Meta:
        model = Product
        # fields = ['category', 'name', 'description', 'comment', 'image']
        fields = ['category', 'number', 'name', 'description', 'comment', 'image']

        widgets = {
            'category': Select(attrs={
                'class': 'form-control custom-select'

            }),
            'name': TextInput(attrs={
                'class': 'form-control'
            }),
            'number': TextInput(attrs={
                'style': 'display:none'
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'rows': '3'
            }),
            'comment': Textarea(attrs={
                'class': 'form-control',
                'rows': '3'
            }),
            'image': ClearableFileInput(attrs={
                'class': 'form-control'
            })
        }


class AddQtyForm(ModelForm):

    status = forms.ModelChoiceField(queryset=Transaction.objects.all(), widget=forms.TextInput(attrs={
            'style': 'display:none'
        }), initial=1)

    direction = forms.ModelChoiceField(queryset=Transaction.objects.all(), widget=forms.TextInput(attrs={
            'style': 'display:none'
        }), initial=1)


    def __init__(self, *args, **kwargs):

        super(AddQtyForm, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        self.fields['direction'].queryset = Direction.objects.all()

    class Meta:
        model = Transaction
        # fields = ['name', 'status', 'direction', 'location', 'quality', 'quantity', 'reason']
        fields = ['number', 'status', 'direction', 'location', 'quality', 'quantity', 'reason']

        widgets = {
            'number': Select(attrs={
                'style': 'display:none'
            }),
            'location': Select(attrs={
                'class': 'form-control'
            }),
            'quality': Select(attrs={
                'class': 'form-control'
            }),
            'quantity': TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'pattern': '[0-9]+',
                'placeholder': "Введите целое число"
            }),
            'reason': Textarea(attrs={
            'class': 'form-control',
            'placeholder': "Опишите причину изменения количества (например: новая поставка)",
            'rows': '3'
            }),


        }


class WriteOffQtyForm(ModelForm):

    status = forms.ModelChoiceField(queryset=Transaction.objects.all(), widget=forms.TextInput(attrs={
            'style': 'display:none'
        }), initial=3)

    direction = forms.ModelChoiceField(queryset=Transaction.objects.all(), widget=forms.TextInput(attrs={
            'style': 'display:none'
        }), initial=2)


    def __init__(self, *args, **kwargs):

        super(WriteOffQtyForm, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        self.fields['direction'].queryset = Direction.objects.all()

    class Meta:
        model = Transaction
        # fields = ['name', 'status', 'direction', 'location', 'quality', 'quantity', 'reason']
        fields = ['number', 'status', 'direction', 'location', 'quality', 'quantity', 'reason']


        widgets = {
            'number': Select(attrs={
                'style': 'display:none'
            }),
            'location': Select(attrs={
                'class': 'form-control'
            }),
            'quality': Select(attrs={
                'class': 'form-control'
            }),
            'quantity': TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'pattern': '[0-9]+',
                'placeholder': "Введите целое число"
            }),
            'reason': Textarea(attrs={
            'class': 'form-control',
            'placeholder': "Опишите причину изменения количества (например: Продажа клиенту)",
            'rows': '3'
            }),
        }


    def clean_quantity(self):
        form_quantity = self.cleaned_data.get('quantity')
        if form_quantity > 0:
            form_quantity = int(form_quantity) * -1

        return form_quantity


class MoveQtyFromForm(ModelForm):

    status = forms.ModelChoiceField(queryset=Transaction.objects.all(), widget=forms.TextInput(attrs={
            'style': 'display:none'
        }), initial=2)

    direction = forms.ModelChoiceField(queryset=Transaction.objects.all(), widget=forms.TextInput(attrs={
            'style': 'display:none'
        }), initial=2)



    def __init__(self, *args, **kwargs):

        super(MoveQtyFromForm, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        self.fields['direction'].queryset = Direction.objects.all()

    class Meta:
        model = Transaction
        # fields = ['name', 'status', 'direction', 'location', 'quality', 'quantity', 'reason']
        fields = ['number', 'status', 'direction', 'location', 'quality', 'quantity', 'reason']

        widgets = {
            'number': Select(attrs={
                'style': 'display:none'
            }),
            # 'name': Select(attrs={
            #     'style': 'display:none'
            # }),
            'location': Select(attrs={
                'class': 'form-control'
            }),
            'quality': Select(attrs={
                'class': 'form-control'
            }),
            'quantity': TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'pattern': '[0-9]+',
                'placeholder': "Введите целое число"
            }),
            'reason': Textarea(attrs={
            'class': 'form-control',
            'placeholder': "Опишите причину изменения количества (например: Перемещение в офис)",
            'rows': '3'
            }),
        }


    def clean_quantity(self):
        form_quantity = self.cleaned_data.get('quantity')
        if form_quantity > 0:
            form_quantity = int(form_quantity) * -1

        return form_quantity

class MoveQtyToForm(ModelForm):

    # name = forms.ModelChoiceField(queryset=Transaction.objects.all(), widget=forms.TextInput(attrs={
    #     # 'style': 'display:none'
    # }), required=False)

    status = forms.ModelChoiceField(queryset=Transaction.objects.all(), widget=forms.TextInput(attrs={
        'style': 'display:none'
    }), initial=2)

    direction = forms.ModelChoiceField(queryset=Transaction.objects.all(), widget=forms.TextInput(attrs={
        'style': 'display:none'
    }), initial=1)

    quantity = forms.ModelChoiceField(queryset=Transaction.objects.all(), widget=forms.TextInput(attrs={
        'style': 'display:none'
    }), required=False)

    reason = CharField(widget = forms.Textarea(attrs={
        'style': 'display:none'
    }), required=False)



    def __init__(self, *args, **kwargs):
        super(MoveQtyToForm, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        self.fields['direction'].queryset = Direction.objects.all()

    class Meta:
        model = Transaction
        # fields = ['name', 'status', 'direction', 'location', 'quality', 'quantity', 'reason']
        fields = ['number', 'status', 'direction', 'location', 'quality', 'quantity', 'reason']

        widgets = {
            'number': Select(attrs={
                'style': 'display:none'
            }),
            # 'name': Select(attrs={
            #     'style': 'display:none'
            # }),
            'location': Select(attrs={
                'class': 'form-control'
            }),
            'quality': Select(attrs={
                'class': 'form-control'
            })
        }


FORMAT_CHOICES = (
    ('xls', 'xls'),
    ('csv', 'csv'),
    ('json', 'json'),
)
class FormatForm(forms.Form):

    format = forms.ChoiceField(choices=FORMAT_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))