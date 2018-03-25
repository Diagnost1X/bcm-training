# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.contrib import messages
from django.test import TestCase

from accounts.models import User
from bcm_training.settings import STRIPE_SECRET
from services.models import (Consultancy, ConsultancyPurchase, Training,
                             TrainingPurchase)


# Create your tests here.
class TestOurServicesView(TestCase):
    def test_get_our_services_view(self):
        response = self.client.get('/services/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('services/our_services.html')


class TestConsultancyView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            email='paul@smith.com',
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )
        consultancy = Consultancy.objects.create(
            name = 'Test Consultancy',
            description = 'Test description',
            price = 440
        )
        training = Training.objects.create(
            name = 'Test Training',
            description = 'Test description 2',
            course_length = 6,
            min_attendees = 2,
            max_attendees = 12,
            cqc_requirement = False,
            price = 600
        )
        ConsultancyPurchase.objects.create(
            user = user,
            consultancy = consultancy,
            amount_paid = consultancy.price,
            consultancy_date = datetime.date.today() + datetime.timedelta(days=5)
        )
        TrainingPurchase.objects.create(
            user = user,
            training = training,
            amount_paid = training.price,
            training_date = datetime.date.today() + datetime.timedelta(days=6)
        )

    def test_consultancy_view_with_no_user_logged_in(self):
        consultancy = Consultancy.objects.get(id=1)
        response = self.client.get('/services/consultancy/{0}/'.format(consultancy.id))

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed('/services/consultancy.html')

    def test_consultancy_view_with_user_logged_in(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        consultancy = Consultancy.objects.get(id=1)
        response = self.client.get('/services/consultancy/{0}/'.format(consultancy.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('/services/consultancy.html')

    def test_consultancy_view_with_valid_post_data(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = User.objects.get(id=1)
        consultancy = Consultancy.objects.get(id=1)
        response = self.client.post('/services/consultancy/{0}/'.format(consultancy.id), {
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '6',
            'expiry_year': str(datetime.datetime.today().year + 1),
            'consultancy_date': str(datetime.date.today() + datetime.timedelta(days=10)),
            'stripe_id': 'tok_visa',
        })
        purchase = ConsultancyPurchase.objects.get(id=2)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/services/')
        self.assertEqual(purchase.user, user)
        self.assertEqual(purchase.amount_paid, consultancy.price)

    def test_consultancy_view_with_card_declined(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        consultancy = Consultancy.objects.get(id=1)
        response = self.client.post('/services/consultancy/{0}/'.format(consultancy.id), {
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '6',
            'expiry_year': str(datetime.datetime.today().year + 1),
            'consultancy_date': str(datetime.date.today() + datetime.timedelta(days=10)),
            'stripe_id': 'tok_chargeDeclined',
        }, follow=True)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue("Your card was declined." in message.message)


class TestTrainingView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            email='paul@smith.com',
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )
        consultancy = Consultancy.objects.create(
            name = 'Test Consultancy',
            description = 'Test description',
            price = 440
        )
        training = Training.objects.create(
            name = 'Test Training',
            description = 'Test description 2',
            course_length = 6,
            min_attendees = 2,
            max_attendees = 12,
            cqc_requirement = False,
            price = 600
        )
        ConsultancyPurchase.objects.create(
            user = user,
            consultancy = consultancy,
            amount_paid = consultancy.price,
            consultancy_date = datetime.date.today() + datetime.timedelta(days=5)
        )
        TrainingPurchase.objects.create(
            user = user,
            training = training,
            amount_paid = training.price,
            training_date = datetime.date.today() + datetime.timedelta(days=6)
        )

    def test_training_view_with_no_user_logged_in(self):
        training = Training.objects.get(id=1)
        response = self.client.get('/services/training/{0}/'.format(training.id))

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed('/services/training.html')

    def test_training_view_with_user_logged_in(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        training = Training.objects.get(id=1)
        response = self.client.get('/services/training/{0}/'.format(training.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('/services/training.html')

    def test_training_view_with_valid_post_data(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = User.objects.get(id=1)
        training = Training.objects.get(id=1)
        response = self.client.post('/services/training/{0}/'.format(training.id), {
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '6',
            'expiry_year': str(datetime.datetime.today().year + 1),
            'training_date': str(datetime.date.today() + datetime.timedelta(days=10)),
            'stripe_id': 'tok_visa',
        })
        purchase = TrainingPurchase.objects.get(id=2)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/services/')
        self.assertEqual(purchase.user, user)
        self.assertEqual(purchase.amount_paid, training.price)

    def test_training_view_with_card_declined(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        training = Training.objects.get(id=1)
        response = self.client.post('/services/training/{0}/'.format(training.id), {
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '6',
            'expiry_year': str(datetime.datetime.today().year + 1),
            'training_date': str(datetime.date.today() + datetime.timedelta(days=10)),
            'stripe_id': 'tok_chargeDeclined',
        }, follow=True)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue("Your card was declined." in message.message)
