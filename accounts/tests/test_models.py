# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from accounts.models import User

# Create your tests here.
class TestUserModel(TestCase):
    def test_user_can_login_using_email(self):
        User.objects.create_user(
            username='paul@smith.com',
            email='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )

        self.assertTrue(self.client.login(email='paul@smith.com',
                                          password='paulsmith'))

    def test_correct_error_when_no_email_supplied(self):
        with self.assertRaises(ValueError) as cm:
            User.objects.create_user(
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )

        the_exception = cm.exception
        self.assertEqual(str(the_exception), 'The given username must be set')
