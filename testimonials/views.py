# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from models import Testimonial


# Create your views here.
def show_testimonials(request):
    testimonials = Testimonial.objects.all()
    args = {'testimonials': testimonials}
    return render(request, 'testimonials/testimonials.html', args)
