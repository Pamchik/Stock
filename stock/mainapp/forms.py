from django.contrib.auth.forms import UsernameField, UserModel
from .models import Product, Transaction, Status, Direction
from django.forms import ModelForm, TextInput, Select, Textarea, ClearableFileInput, CharField
from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _


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
        fields = ['number', 'status', 'direction', 'location', 'quality', 'quantity', 'reason', 'author']

        widgets = {
            'number': Select(attrs={
                'style': 'display:none'
            }),
            'author': Select(attrs={
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
        fields = ['number', 'status', 'direction', 'location', 'quality', 'quantity', 'reason', 'author']


        widgets = {
            'number': Select(attrs={
                'style': 'display:none'
            }),
            'author': Select(attrs={
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
        fields = ['number', 'status', 'direction', 'location', 'quality', 'quantity', 'reason', 'author']

        widgets = {
            'number': Select(attrs={
                'style': 'display:none'
            }),
            'author': Select(attrs={
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
        fields = ['number', 'status', 'direction', 'location', 'quality', 'quantity', 'reason', 'author']

        widgets = {
            'number': Select(attrs={
                'style': 'display:none'
            }),
            'author': Select(attrs={
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

class AuthenticationCustomForm(forms.Form):

    username = UsernameField(
        label=False,
        widget=forms.TextInput(attrs={
            # 'class': 'text',
            # "autofocus": True
        }),
    )


    password = forms.CharField(
        label=False,
        # strip=False,
        widget=forms.PasswordInput(attrs={
            # 'class': 'password',
            # "autocomplete": "current-password"
        }),
    )

    error_messages = {
        "invalid_login": _("Пожалуйста, введите правильный Логин и/или Пароль."
                           "Обратите внимание, что поля могут быть чувствительны к регистру."),
        "inactive": _("Данный аккаунт не активен."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length
        if self.fields["username"].label is None:
            self.fields["username"].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"username": self.username_field.verbose_name},
        )


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """

    error_messages = {
        "password_mismatch": _("Введенные пароли не совпадают."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class PasswordChangeCustomForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """

    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": _(
            "Ваш старый пароль был введен неверно."
        ),
    }
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    field_order = ["old_password", "new_password1", "new_password2"]

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages["password_incorrect"],
                code="password_incorrect",
            )
        return old_password
