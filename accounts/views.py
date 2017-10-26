# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.template.context_processors import csrf

from forms import UserRegistrationForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password1'))

            if user:
                return redirect(reverse('home'))

    else:
        form = UserRegistrationForm()

    args = {'form': form}
    args.update(csrf(request))

    return render(request, 'accounts/register.html', args)
