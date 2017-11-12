# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import Training, Consultancy

# Create your views here.
def our_services(request):
    training = Training.objects.all()
    consultancy = Consultancy.objects.all()
    args = {'training': training, 'consultancy': consultancy}
    return render(request, 'services/our_services.html', args)
