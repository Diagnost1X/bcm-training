# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.context_processors import csrf

from forms import ChangeEmail, ChangeName, UserLoginForm, UserRegistrationForm
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
                messages.success(request, "You have successfully registered and been logged in.")
                auth.login(request, user)
                return redirect(reverse('account', kwargs={'user_id': user.id}))
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
                return redirect(reverse('account', kwargs={'user_id': user.id}))
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

@login_required
def change_email(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    # Protecting against users maliciously editing other users accounts
    if not user == request.user:
        # To ensure error message displays correctly
        storage = messages.get_messages(request)
        storage.used = True
        messages.error(request, "You are not authorised to view this page.")
        return redirect(reverse('account', kwargs={'user_id': request.user.id}))
    
    elif request.method == 'POST':
        change_email_form = ChangeEmail(request.POST)
        if change_email_form.is_valid():
            email1 = change_email_form.cleaned_data['email1']
            email2 = change_email_form.cleaned_data['email2']
            if email1 == email2:
                user.email = email2
                user.username = email2
                user.save()
                messages.success(request, "You have successfully updated your email.")
                return redirect(reverse('account', kwargs={'user_id': request.user.id}))
            else:
                messages.error(request, "The email addresses didn't match.")
    else:
        change_email_form = ChangeEmail()
    
    args = {
        'user': user,
        'change_email_form': change_email_form,
        'form': reverse('change_email', kwargs={'user_id': request.user.id})
    }
    args.update(csrf(request))

    return render(request, 'accounts/change_email.html', args)

@login_required
def change_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    # Protecting against users maliciously editing other users accounts
    if not user == request.user:
        # To ensure error message displays correctly
        storage = messages.get_messages(request)
        storage.used = True
        messages.error(request, "You are not authorised to view this page.")
        return redirect(reverse('account', kwargs={'user_id': request.user.id}))
    
    elif request.method == 'POST':
        change_password_form = PasswordChangeForm(request.user, request.POST)
        if change_password_form.is_valid():
                new_user = change_password_form.save()
                update_session_auth_hash(request, new_user)
                messages.success(request, "You have successfully updated your password.")
                return redirect(reverse('account', kwargs={'user_id': request.user.id}))
        else:
            messages.error(request, "An error occured, please see below.")
    else:
        change_password_form = PasswordChangeForm(request.user)
    
    args = {
        'user': user,
        'change_password_form': change_password_form,
        'form': reverse('change_password', kwargs={'user_id': request.user.id})
    }
    args.update(csrf(request))

    return render(request, 'accounts/change_password.html', args)
