# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from accounts.models import User

from testimonials.forms import TestimonialForm


# Create your tests here.
class TestTestimonialForm(TestCase):
    def test_form_works_by_only_entering_comments(self):
        form = TestimonialForm({
            'comments': 'This is a test'
        })

        self.assertTrue(form.is_valid())

    def test_correct_message_for_missing_comments(self):
        form = TestimonialForm({
            'comments': ''
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['comments'], [u'This field is required.'])
