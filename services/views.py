# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.context_processors import csrf

import stripe
from models import Consultancy, ConsultancyPurchase, Training, TrainingPurchase

from .forms import ConsultancyForm, TrainingForm

stripe.api_key = settings.STRIPE_SECRET

# Create your views here.
def our_services(request):
    training = Training.objects.all()
    consultancy = Consultancy.objects.all()
    args = {'training': training, 'consultancy': consultancy}
    return render(request, 'services/our_services.html', args)

@login_required
def consultancy(request, consultancy_id):
    consultancy = get_object_or_404(Consultancy, pk=consultancy_id)

    if request.method == 'POST':
        form = ConsultancyForm(request.POST)
        if form.is_valid():
            try:
                purchase = stripe.Charge.create(
                    amount = int((consultancy.price * 100)),
                    currency = "GBP",
                    description = "Consultancy: " + str(consultancy) + " for " + str(request.user),
                    card = form.cleaned_data['stripe_id']
                )
                if purchase.paid:
                    confirmed = form.save(False)
                    confirmed.user = request.user
                    confirmed.consultancy = consultancy
                    confirmed.amount_paid = consultancy.price
                    confirmed.save()

                    messages.success(request, "Purchase Successful!")
                    return redirect(reverse('our_services'))
                else:
                    messages.error(request, "Unfortunately, we were unable to take a payment with that card.")
            except stripe.error.CardError, e:
                messages.error(request, "Your card was declined.")
    else:
        form = ConsultancyForm()

    # Passes an array that Javascript can interpret for disabling dates in datepicker
    dates_taken = []
    for date in TrainingPurchase.objects.values_list('training_date'):
        date = str(date)
        date = date[15:]
        date = date[:-3]
        dates_taken.append(date)

    for date in ConsultancyPurchase.objects.values_list('consultancy_date'):
        date = str(date)
        date = date[15:]
        date = date[:-3]
        dates_taken.append(date)

    args = {
        'form': form,
        'form_action': reverse('consultancy', kwargs={'consultancy_id': consultancy.id}),
        'consultancy': consultancy,
        'publishable': settings.STRIPE_PUBLISHABLE,
        'dates_taken': dates_taken,
    }
    args.update(csrf(request))

    return render(request, 'services/consultancy.html', args)


@login_required
def training(request, training_id):
    training = get_object_or_404(Training, pk=training_id)

    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            try:
                purchase = stripe.Charge.create(
                    amount = int((training.price * 100)),
                    currency = "GBP",
                    description = "Training: " + str(training) + " for " + str(request.user),
                    card = form.cleaned_data['stripe_id']
                )
                if purchase.paid:
                    confirmed = form.save(False)
                    confirmed.user = request.user
                    confirmed.training = training
                    confirmed.amount_paid = training.price
                    confirmed.save()

                    messages.success(request, "Purchase Successful!")
                    return redirect(reverse('our_services'))
                else:
                    messages.error(request, "Unfortunately, we were unable to take a payment with that card.")
            except stripe.error.CardError, e:
                messages.error(request, "Your card was declined.")
    else:
        form = TrainingForm()
    
    # Passes an array that Javascript can interpret for disabling dates in datepicker
    dates_taken = []
    for date in TrainingPurchase.objects.values_list('training_date'):
        date = str(date)
        date = date[15:]
        date = date[:-3]
        dates_taken.append(date)

    for date in ConsultancyPurchase.objects.values_list('consultancy_date'):
        date = str(date)
        date = date[15:]
        date = date[:-3]
        dates_taken.append(date)

    args = {
        'form': form,
        'form_action': reverse('training', kwargs={'training_id': training.id}),
        'training': training,
        'publishable': settings.STRIPE_PUBLISHABLE,
        'dates_taken': dates_taken,
    }
    args.update(csrf(request))

    return render(request, 'services/training.html', args)
