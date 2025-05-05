from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="Логин",
                               error_messages={
                                   "requared": _("Пожалуйста введите логин")
                               })
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    email = forms.EmailField(label="Эл. почта")
    password1 = forms.CharField(label="Пароль",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтвердите пароль",
                                widget=forms.PasswordInput,
                                error_messages={
                                    "requared": _("Пожалуйста подтвердите пароль")
                                })


    class Meta:
        model = User
        fields = ("username", "first_name",
                  "last_name", "email", "password1", "password2")

class NewRegistrationForm(forms.ModelForm):
    password2 = forms.CharField(label="Подтвердите пароль",
                                widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username", "first_name",
                  "last_name", "email", "password")
        help_texts = {
            "username": ""
        }
    def clean_password2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError("Пароли не совпадают!")
        return cleaned_data['password2']


class CustomPasswordChangeForm(SetPasswordForm):
    old_password = forms.CharField(
        label="Старый пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    new_password1 = forms.CharField(
        label="Новый пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password"}
        ),
    )

    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        strip=False,
        widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if old_password and new_password1:
            if old_password == new_password1:
                raise ValidationError("Новый пароль должен отличаться от старого")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError("Введенные пароли не совпадают")

        return cleaned_data

