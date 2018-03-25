# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.test import TestCase

from .forms import ContactUs


# Create your tests here.
class TestContactUsView(TestCase):
    def setUp(self):
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def tearDown(self):
        os.environ['RECAPTCHA_TESTING'] = 'False'

    def test_contact_us_view_loads_correctly(self):
        response = self.client.get('/contact-us/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_us/contact_us.html')

    def test_contact_us_post_method_excluding_company(self):
        response = self.client.post('/contact-us/', {
            'name': 'Ashley Shenton',
            'contact_number': '07123456789',
            'email_address': 'test@email.com',
            'message': 'This is a test',
            'g-recaptcha-response': 'PASSED'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/contact-us/')

    def test_contact_us_post_method_including_company(self):
        response = self.client.post('/contact-us/', {
            'name': 'Ashley Shenton',
            'company': 'BCM Training',
            'contact_number': '07123456789',
            'email_address': 'test@email.com',
            'message': 'This is a test',
            'g-recaptcha-response': 'PASSED'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/contact-us/')


class TestContactUsForm(TestCase):
    def setUp(self):
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def tearDown(self):
        os.environ['RECAPTCHA_TESTING'] = 'False'

    def test_contact_us_form_with_valid_data(self):
        form = ContactUs({
            'name': 'Ash',
            'company': 'BCM Training',
            'contact_number': '07123456789',
            'email_address': 'test@email.com',
            'message': 'This is a test',
            'g-recaptcha-response': 'PASSED'
        })

        self.assertTrue(form.is_valid())

    def test_contact_us_form_with_valid_data_excluding_company(self):
        form = ContactUs({
            'name': 'Ash',
            'contact_number': '07123456789',
            'email_address': 'test@email.com',
            'message': 'This is a test',
            'g-recaptcha-response': 'PASSED'
        })

        self.assertTrue(form.is_valid())

    def test_contact_us_form_with_missing_name(self):
        form = ContactUs({
            'contact_number': '07123456789',
            'email_address': 'test@email.com',
            'message': 'This is a test',
            'g-recaptcha-response': 'PASSED'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [u'This field is required.'])

    def test_contact_us_form_with_missing_contact_number(self):
        form = ContactUs({
            'name': 'Ash',
            'email_address': 'test@email.com',
            'message': 'This is a test',
            'g-recaptcha-response': 'PASSED'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['contact_number'], [u'This field is required.'])

    def test_contact_us_form_with_missing_email(self):
        form = ContactUs({
            'name': 'Ash',
            'contact_number': '07123456789',
            'message': 'This is a test',
            'g-recaptcha-response': 'PASSED'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email_address'], [u'This field is required.'])

    def test_contact_us_form_with_missing_message(self):
        form = ContactUs({
            'name': 'Ash',
            'contact_number': '07123456789',
            'email_address': 'test@email.com',
            'g-recaptcha-response': 'PASSED'
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['message'], [u'This field is required.'])

    def test_contact_us_form_with_invalid_recaptcha(self):
        form = ContactUs({
            'name': 'Ash',
            'contact_number': '07123456789',
            'email_address': 'test@email.com',
            'message': 'This is a test',
        })

        self.assertFalse(form.is_valid())
