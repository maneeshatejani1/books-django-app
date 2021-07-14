import re

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model

from accounts.utils import split_full_name


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(required=True)
    # phone_number = forms.RegexField(regex='^((\+92)|(0092))-{0,1}\d{3}-{0,1}\d{7}$|^\d{11}$|^\d{4}-\d{7}$')
    full_name = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('phone_number', 'email', 'full_name', 'profile_pic_url', 'country',)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r"^((\+92)|(0092))-{0,1}\d{3}-{0,1}\d{7}$|^\d{11}$|^\d{4}-\d{7}$", phone_number):
            raise forms.ValidationError(
                "phone number must start with '0' or '0092' or '+92' " +
                "and the remaining digits cannot be more than 9 digits"
            )
        return phone_number

    def save(self, commit=True):
        instance = super().save(commit=False)
        full_name = self.cleaned_data['full_name']
        first_name, last_name = split_full_name(full_name)
        if first_name is not None and last_name is None:
            instance.first_name = first_name
        elif first_name is not None and last_name is not None:
            instance.first_name = first_name
            instance.last_name = last_name
        if commit:
            instance.save()
        return instance


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = UserChangeForm.Meta.fields
