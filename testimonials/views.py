# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.context_processors import csrf

from .forms import TestimonialForm
from .models import Testimonial


# Create your views here.
def show_testimonials(request):
    testimonials = Testimonial.objects.all()
    args = {'testimonials': testimonials}
    return render(request, 'testimonials/testimonials.html', args)

@login_required
def new_testimonial(request):
    has_testimonial = Testimonial.objects.filter(user_id=request.user).exists()

    # Protecting against users trying to enter more than one testimonial
    if has_testimonial == True:
        # To ensure error message displays correctly
        storage = messages.get_messages(request)
        storage.used = True
        messages.error(request, 'You have already shared a testimonial, please edit or delete your current one.')
        return redirect(reverse('testimonials'))

    elif request.method == 'POST':
        testimonial_form = TestimonialForm(request.POST)
        if testimonial_form.is_valid():
            testimonial = testimonial_form.save(False)
            testimonial.user = request.user
            testimonial.first_name = request.user.first_name
            testimonial.initial = request.user.last_name
            testimonial.initial = testimonial.initial[0]
            testimonial.save()

            messages.success(request, "Thank you for your feedback!")
            return redirect(reverse('testimonials'))

    else:
        testimonial_form = TestimonialForm()

    args = {
        'testimonial_form': testimonial_form,
        'form_action': reverse('new_testimonial'),
        'button_text': 'Share Testimonial',
        'header_text': 'Write Your Testimonial'
    }
    args.update(csrf(request))

    return render(request, 'testimonials/testimonial_form.html', args)

@login_required
def edit_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, pk=testimonial_id)

    # Protecting against users maliciously editing other users testimonials
    if not testimonial.user == request.user and not request.user.is_staff:
        # To ensure error message displays correctly
        storage = messages.get_messages(request)
        storage.used = True
        messages.error(request, 'You can only edit your own testimonial.')
        return redirect(reverse('testimonials'))

    elif request.method == 'POST':
        testimonial_form = TestimonialForm(request.POST, instance=testimonial)
        if testimonial_form.is_valid():
            testimonial_form.save()
            messages.success(request, "Your testimonial has successfully been updated.")
            return redirect(reverse('testimonials'))
    else:
        testimonial_form = TestimonialForm(instance=testimonial)

    args = {
        'testimonial_form': testimonial_form,
        'form_action': reverse('edit_testimonial', kwargs={'testimonial_id': testimonial.id}),
        'button_text': 'Update Testimonial',
        'header_text': 'Edit Your Testimonial'
    }
    args.update(csrf(request))

    return render(request, 'testimonials/testimonial_form.html', args)

@login_required
def delete_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, pk=testimonial_id)

    # Protecting against users maliciously deleting other users testimonials
    if not testimonial.user == request.user and not request.user.is_staff:
        # To ensure error message displays correctly
        storage = messages.get_messages(request)
        storage.used = True
        messages.error(request, 'You can only delete your own testimonial.')
        return redirect(reverse('testimonials'))

    testimonial.delete()

    messages.success(request, "You have successfully deleted your testimonial.")
    return redirect(reverse('testimonials'))
