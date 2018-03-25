# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.test import TestCase

from services.forms import ConsultancyForm, TrainingForm


# Create your tests here.
class TestTrainingForm(TestCase):
    def test_training_form_works_with_valid_data(self):
        form = TrainingForm({
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '6',
            'expiry_year': str(datetime.datetime.today().year + 1),
            'training_date': str(datetime.date.today() + datetime.timedelta(days=5)),
            'stripe_id': 'abc123'
        })

        self.assertTrue(form.is_valid())

    def test_training_form_fails_with_missing_credit_card_number(self):
        form = TrainingForm({
            'cvv': '123',
            'expiry_month': '10',
            'expiry_year': str(datetime.datetime.today().year + 1),
            'training_date': str(datetime.date.today() + datetime.timedelta(days=5)),
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['credit_card_number'], [u'This field is required.'])

    def test_training_form_fails_with_missing_cvv(self):
        form = TrainingForm({
            'credit_card_number': '4242424242424242',
            'expiry_month': '10',
            'expiry_year': str(datetime.datetime.today().year + 1),
            'training_date': str(datetime.date.today() + datetime.timedelta(days=5)),
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['cvv'], [u'This field is required.'])

    def test_training_form_fails_with_missing_expiry_month(self):
        form = TrainingForm({
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_year': str(datetime.datetime.today().year + 1),
            'training_date': str(datetime.date.today() + datetime.timedelta(days=5)),
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['expiry_month'], [u'This field is required.'])

    def test_training_form_fails_with_missing_expiry_year(self):
        form = TrainingForm({
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '10',
            'training_date': str(datetime.date.today() + datetime.timedelta(days=5)),
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['expiry_year'], [u'This field is required.'])

    def test_training_form_fails_with_missing_training_date_entry(self):
        form = TrainingForm({
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '10',
            'expiry_year': str(datetime.datetime.today().year + 1),
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['training_date'], [u'This field is required.'])

    def test_training_form_fails_with_invalid_training_date_entry(self):
        form = TrainingForm({
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '10',
            'expiry_year': str(datetime.datetime.today().year + 1),
            'training_date': '123456',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['training_date'], [u'Enter a valid date.'])


class TestConsultancyForm(TestCase):
    def test_consultancy_form_works_with_valid_data(self):
        form = ConsultancyForm({
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '6',
            'expiry_year': str(datetime.datetime.today().year + 1),
            'consultancy_date': str(datetime.date.today() + datetime.timedelta(days=5)),
            'stripe_id': 'abc123'
        })

        self.assertTrue(form.is_valid())

    def test_consultancy_form_fails_with_missing_credit_card_number(self):
        form = ConsultancyForm({
            'cvv': '123',
            'expiry_month': '10',
            'expiry_year': str(datetime.datetime.today().year + 1),
            'consultancy_date': str(datetime.date.today() + datetime.timedelta(days=5)),
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['credit_card_number'], [u'This field is required.'])

    def test_consultancy_form_fails_with_missing_cvv(self):
        form = ConsultancyForm({
            'credit_card_number': '4242424242424242',
            'expiry_month': '10',
            'expiry_year': str(datetime.datetime.today().year + 1),
            'consultancy_date': str(datetime.date.today() + datetime.timedelta(days=5)),
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['cvv'], [u'This field is required.'])

    def test_consultancy_form_fails_with_missing_expiry_month(self):
        form = ConsultancyForm({
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_year': str(datetime.datetime.today().year + 1),
            'consultancy_date': str(datetime.date.today() + datetime.timedelta(days=5)),
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['expiry_month'], [u'This field is required.'])

    def test_consultancy_form_fails_with_missing_expiry_year(self):
        form = ConsultancyForm({
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '10',
            'consultancy_date': str(datetime.date.today() + datetime.timedelta(days=5)),
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['expiry_year'], [u'This field is required.'])

    def test_consultancy_form_fails_with_missing_consultancy_date_entry(self):
        form = ConsultancyForm({
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '10',
            'expiry_year': str(datetime.datetime.today().year + 1),
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['consultancy_date'], [u'This field is required.'])

    def test_consultancy_form_fails_with_invalid_consultancy_date_entry(self):
        form = ConsultancyForm({
            'credit_card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': '10',
            'expiry_year': str(datetime.datetime.today().year + 1),
            'consultancy_date': '123456',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['consultancy_date'], [u'Enter a valid date.'])
