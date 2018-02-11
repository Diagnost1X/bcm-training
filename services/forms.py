from django import forms

from .models import (Consultancy, ConsultancyPurchase, Training,
                     TrainingPurchase)


class TrainingForm(forms.ModelForm):
    credit_card_number = forms.CharField(label="Card Number", max_length=16)
    cvv = forms.CharField(label="Security Code (CVV)", max_length=3)
    expiry_month = forms.CharField(label="Month (MM)", max_length=2)
    expiry_year = forms.CharField(label="Year (YYYY)", max_length=4)
    stripe_id = forms.CharField(widget=forms.HiddenInput)
    training_date = forms.DateField(widget=forms.TextInput(attrs={
        'class':'datepicker'
    }))

    class Meta:
        model = TrainingPurchase
        fields = ['training_date']
        

class ConsultancyForm(forms.ModelForm):
    credit_card_number = forms.CharField(label="Card Number", max_length=16)
    cvv = forms.CharField(label="Security Code (CVV)", max_length=3)
    expiry_month = forms.CharField(label="Month (MM)", max_length=2)
    expiry_year = forms.CharField(label="Year (YYYY)", max_length=4)
    stripe_id = forms.CharField(widget=forms.HiddenInput)
    consultancy_date = forms.DateField(widget=forms.TextInput(attrs={
        'class':'datepicker'
    }))

    class Meta:
        model = ConsultancyPurchase
        fields = ['consultancy_date']
