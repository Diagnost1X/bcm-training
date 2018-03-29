# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.test import TestCase

from accounts.forms import (ChangeConsultancy, ChangeEmail, ChangeName,
                            ChangeTraining, UserLoginForm,
                            UserRegistrationForm)


# Create your tests here.
class TestUserRegistrationForm(TestCase):
    def test_user_reg_form_with_valid_data(self):
        form = UserRegistrationForm({
            'first_name': 'Paul',
            'last_name': 'Smith',
            'email': 'paul@smith.com',
            'password1': 'paulsmith',
            'password2': 'paulsmith'
        })

        self.assertTrue(form.is_valid())

    def test_user_reg_form_fails_with_mismatched_passwords(self):
        form = UserRegistrationForm({
            'first_name': 'Paul',
            'last_name': 'Smith',
            'email': 'paul@smith.com',
            'password1': 'paulsmith',
            'password2': 'paulsmit'
        })

        self.assertFalse(form.is_valid())

    def test_user_reg_form_fails_with_missing_first_name(self):
        form = UserRegistrationForm({
            'last_name': 'Smith',
            'email': 'paul@smith.com',
            'password1': 'paulsmith',
            'password2': 'paulsmith'
        })

        self.assertFalse(form.is_valid())

    def test_user_reg_form_fails_with_missing_last_name(self):
        form = UserRegistrationForm({
            'first_name': 'Paul',
            'email': 'paul@smith.com',
            'password1': 'paulsmith',
            'password2': 'paulsmith'
        })

        self.assertFalse(form.is_valid())

    def test_user_reg_form_fails_with_missing_email(self):
        form = UserRegistrationForm({
            'first_name': 'Paul',
            'last_name': 'Smith',
            'password1': 'paulsmith',
            'password2': 'paulsmith'
        })

        self.assertFalse(form.is_valid())

    def test_user_reg_form_fails_with_incorrectly_formatted_email(self):
        form = UserRegistrationForm({
            'first_name': 'Paul',
            'last_name': 'Smith',
            'email': 'paulsmithcom',
            'password1': 'paulsmith',
            'password2': 'paulsmith'
        })

        self.assertFalse(form.is_valid())


class TestUserLoginForm(TestCase):
    def test_login_form_submits_with_valid_data(self):
        form = UserLoginForm({
            'email': 'paul@smith.com',
            'password': 'paulsmith'
        })

        self.assertTrue(form.is_valid())

    def test_login_form_fails_with_incorrectly_formatted_email(self):
        form = UserLoginForm({
            'email': 'paulsmithcom',
            'password': 'paulsmith'
        })

        self.assertFalse(form.is_valid())

    def test_login_form_fails_with_missing_email(self):
        form = UserLoginForm({
            'password': 'paulsmith'
        })

        self.assertFalse(form.is_valid())

    def test_login_form_fails_with_missing_password(self):
        form = UserLoginForm({
            'email': 'paulsmithcom'
        })

        self.assertFalse(form.is_valid())


class TestChangeNameForm(TestCase):
    def test_change_name_form_submits_with_valid_data(self):
        form = ChangeName({
            'first_name': 'Paul',
            'last_name': 'Smith'
        })

        self.assertTrue(form.is_valid())

    def test_change_name_form_fails_with_missing_first_name(self):
        form = ChangeName({
            'last_name': 'Smith'
        })

        self.assertFalse(form.is_valid())

    def test_change_name_form_fails_with_missing_last_name(self):
        form = ChangeName({
            'first_name': 'Paul'
        })

        self.assertFalse(form.is_valid())


class TestChangeEmailForm(TestCase):
    def test_change_email_form_submits_with_valid_data(self):
        form = ChangeEmail({
            'email1': 'paul@smith.com',
            'email2': 'paul@smith.com'
        })

        self.assertTrue(form.is_valid())

    def test_change_email_form_fails_with_missing_email1(self):
        form = ChangeEmail({
            'email2': 'paul@smith.com'
        })

        self.assertFalse(form.is_valid())

    def test_change_email_form_fails_with_missing_email2(self):
        form = ChangeEmail({
            'email1': 'paul@smith.com'
        })

        self.assertFalse(form.is_valid())


class TestChangeTrainingForm(TestCase):
    def test_change_training_form_submits_with_valid_data(self):
        form = ChangeTraining({
            'training_date': str(datetime.date.today() + datetime.timedelta(days=5))
        })

        self.assertTrue(form.is_valid())

    def test_change_training_form_fails_with_empty_field(self):
        form = ChangeTraining({
            'training_date': ''
        })

        self.assertFalse(form.is_valid())

    def test_change_training_form_fails_without_date(self):
        form = ChangeTraining({
            'training_date': 'paul'
        })

        self.assertFalse(form.is_valid())

    def test_change_training_form_fails_with_incorrectly_formatted_date(self):
        form = ChangeTraining({
            'training_date': '13/13/2020'
        })

        self.assertFalse(form.is_valid())


class TestChangeConsultancyForm(TestCase):
    def test_change_consultancy_form_submits_with_valid_data(self):
        form = ChangeConsultancy({
            'consultancy_date': str(datetime.date.today() + datetime.timedelta(days=5))
        })

        self.assertTrue(form.is_valid())

    def test_change_consultancy_form_fails_with_empty_field(self):
        form = ChangeConsultancy({
            'consultancy_date': ''
        })

        self.assertFalse(form.is_valid())

    def test_change_consultancy_form_fails_without_date(self):
        form = ChangeConsultancy({
            'consultancy_date': 'paul'
        })

        self.assertFalse(form.is_valid())

    def test_change_consultancy_form_fails_with_incorrectly_formatted_date(self):
        form = ChangeConsultancy({
            'consultancy_date': '13/13/2020'
        })

        self.assertFalse(form.is_valid())
