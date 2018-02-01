# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

import bcm_training.settings


# Create your models here.
class Testimonial(models.Model):

    comments = models.TextField()
    user = models.OneToOneField(bcm_training.settings.AUTH_USER_MODEL, related_name='testimonials')
    first_name = models.CharField(max_length=30)
    initial = models.CharField(max_length=1)
    date_created = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.first_name + " " + self.initial
