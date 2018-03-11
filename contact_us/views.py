# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def contact_us(request):
    return render(request, 'contact_us/contact_us.html')
