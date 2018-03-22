# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from accounts.models import User
from testimonials.models import Testimonial


# Create your tests here.
class TestTestimonialModel(TestCase):
    def setUp(self):
        User.objects.create_user(
            email='paul@smith.com',
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )

    def test_date_created_defaults_to_now(self):
        user = User.objects.get(id=1)
        testimonial = Testimonial(
            comments = 'This is a test',
            first_name = 'Jack',
            initial = 'F',
            user = user
        )
        testimonial.save()

        self.assertTrue(testimonial.date_created)

    def test_all_data_saves_correctly(self):
        user = User.objects.get(id=1)
        testimonial = Testimonial(
            comments = 'This is a test',
            first_name = 'Jack',
            initial = 'F',
            user = user
        )
        testimonial.save()

        self.assertEqual(testimonial.comments, "This is a test")
        self.assertEqual(testimonial.first_name, "Jack")
        self.assertEqual(testimonial.initial, "F")
        self.assertEqual(testimonial.user, user)

    def test_testimonial_name_displays_correctly(self):
        user = User.objects.get(id=1)
        testimonial = Testimonial(
            comments = 'This is a test',
            first_name = 'Jack',
            initial = 'F',
            user = user
        )
        testimonial.save()

        self.assertEqual(str(testimonial), "Jack F")
