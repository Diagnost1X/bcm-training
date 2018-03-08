from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from accounts.models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", max_length=30)
    last_name = forms.CharField(label="Last Name", max_length=30)
    # Show user their email in lowercase so they know how it will be submitted
    email = forms.CharField(label="Email Address", max_length=254, widget=forms.TextInput(attrs={
        'style':'text-transform: lowercase;'
    }), help_text="Email Addresses must be lowercase.")
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html()
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        exclude = ['username']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            message = "Passwords do not match"
            raise ValidationError(message)
        # Added to improve password security and mirror change password form validation
        password_validation.validate_password(password2)
        return password2

    def save(self, commit=True):
        instance = super(UserRegistrationForm, self).save(commit=False)
        instance.email = instance.email.lower()
        instance.username = instance.email

        if commit:
            instance.save()

        return instance


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'style':'text-transform: lowercase;'
        }))
    password = forms.CharField(widget=forms.PasswordInput)


class ChangeName(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=30)
    last_name = forms.CharField(label="Last Name", max_length=30)


class ChangeEmail(forms.Form):
    # Show user their email in lowercase so they know how it will be submitted
    email1 = forms.EmailField(label='New Email Address', max_length=254, widget=forms.TextInput(attrs={
        'style':'text-transform: lowercase;'
        }), help_text="Email Addresses must be lowercase.")
    email2 = forms.EmailField(label='Confirm New Email', max_length=254, widget=forms.TextInput(attrs={
        'style':'text-transform: lowercase;'
        }))


class ChangeTraining(forms.Form):
    training_date = forms.DateField(widget=forms.TextInput(attrs={
        'class':'datepicker'
    }))


class ChangeConsultancy(forms.Form):
    consultancy_date = forms.DateField(widget=forms.TextInput(attrs={
        'class':'datepicker'
    }))
