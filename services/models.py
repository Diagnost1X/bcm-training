# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

import bcm_training.settings


# Create your models here.
class Training(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    course_length = models.DecimalField(max_digits=2, decimal_places=1)
    min_attendees = models.IntegerField(default='0')
    max_attendees = models.IntegerField()
    cqc_requirement = models.BooleanField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return self.name

class Consultancy(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default='300')

    def __unicode__(self):
        return self.name

class TrainingPurchase(models.Model):

    user = models.ForeignKey(bcm_training.settings.AUTH_USER_MODEL, related_name='purchases')
    training = models.ForeignKey(Training, related_name='purchases')
    purchase_date = models.DateField(default=timezone.now)
    amount_paid = models.DecimalField(max_digits=6, decimal_places=2)
    training_date = models.DateField(default=timezone.now)
