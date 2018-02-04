from django import forms

from .models import Testimonial

class TestimonialForm(forms.ModelForm):
    comments = forms.Textarea()

    class Meta:
        model = Testimonial
        fields = ['comments']
