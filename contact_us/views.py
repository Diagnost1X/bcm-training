# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse
from django.template.context_processors import csrf

from forms import ContactUs


# Create your views here.
def contact_us(request):
    if request.method == 'POST':
        form = ContactUs(request.POST)
        if form.is_valid():
            messages.success(request, 'Thank you, I will respond to you within 24 hours.')
            return redirect(reverse('contact_us'))
    else:
        form = ContactUs()

    args = {
        'form': form,
    }
    args.update(csrf(request))

    return render(request, 'contact_us/contact_us.html', args)
