# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.context_processors import csrf

from forms import ChangeName, UserLoginForm, UserRegistrationForm
from models import User


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password1'))

            if user:
                messages.success(request, "You have successfully registered, you may now login.")
                return redirect(reverse('login'))
            else:
                messages.error(request, 'Something went wrong, please try again.')

    else:
        form = UserRegistrationForm()

    args = {'form': form}
    args.update(csrf(request))

    return render(request, 'accounts/register.html', args)


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect(reverse('home'))
            else:
                form.add_error(None, "Your email or password was not recognised.")

    else:
        form = UserLoginForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'accounts/login.html', args)

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')
    return render(request, 'home/home.html')

@login_required
def account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    training_purchases = user.t_purchases.all()
    consultancy_purchases = user.c_purchases.all()

    # Protecting against users maliciously accessing other users accounts and order history
    if not user == request.user:
        # To ensure error message displays correctly
        storage = messages.get_messages(request)
        storage.used = True
        messages.error(request, "You are not authorised to view this page.")
        return redirect(reverse('account', kwargs={'user_id': request.user.id}))

    args = {
        'user': user,
        'training_purchases': training_purchases,
        'consultancy_purchases': consultancy_purchases
    }

    return render(request, 'accounts/account.html', args)

@login_required
def change_name(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    # Protecting against users maliciously editing other users accounts
    if not user == request.user:
        # To ensure error message displays correctly
        storage = messages.get_messages(request)
        storage.used = True
        messages.error(request, "You are not authorised to view this page.")
        return redirect(reverse('account', kwargs={'user_id': request.user.id}))

    elif request.method == 'POST':
        change_name_form = ChangeName(request.POST)
        if change_name_form.is_valid():
            user.first_name = change_name_form.cleaned_data['first_name']
            user.last_name = change_name_form.cleaned_data['last_name']
            user.save()
            messages.success(request, "Your have successfully updated your name.")
            return redirect(reverse('account', kwargs={'user_id': request.user.id}))
    else:
        change_name_form = ChangeName()

    args = {
        'user': user,
        'change_name_form': change_name_form,
        'form_action': reverse('change_name', kwargs={'user_id': request.user.id})
    }
    args.update(csrf(request))

    return render(request, 'accounts/change_name.html', args)
