from django import forms

from captcha.fields import ReCaptchaField


class ContactUs(forms.Form):
    name = forms.CharField(max_length=100, label='Name*')
    company = forms.CharField(max_length=100, required=False)
    contact_number = forms.CharField(max_length=11, min_length=11, label='Contact Number*')
    email_address = forms.EmailField(max_length=254, label='Email Address*')
    message = forms.CharField(widget=forms.Textarea, label='Message*')
    captcha = ReCaptchaField()
