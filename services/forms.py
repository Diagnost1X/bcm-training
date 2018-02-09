from django import forms

from .models import Consultancy, Training, TrainingPurchase


class TrainingForm(forms.ModelForm):
    credit_card_number = forms.CharField(label="Card Number", max_length=16)
    cvv = forms.CharField(label="Security Code (CVV)", max_length=3)
    expiry_month = forms.CharField(label="Month (MM)", max_length=2)
    expiry_year = forms.CharField(label="Year (YYYY)", max_length=4)
    stripe_id = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = TrainingPurchase
        fields = ['stripe_id']
        