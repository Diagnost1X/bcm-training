# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.contrib import auth
from django.test import TestCase

from accounts.models import User
from services.models import (Consultancy, ConsultancyPurchase, Training,
                             TrainingPurchase)


# Create your tests here.
class TestRegisterView(TestCase):
    def test_get_register_view(self):
        response = self.client.get('/accounts/register/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_with_valid_post_data(self):
        response = self.client.post('/accounts/register/', {
            'first_name': 'Paul',
            'last_name': 'Smith',
            'email': 'paul@smith.com',
            'password1': 'paulsmith',
            'password2': 'paulsmith'
        })
        user = User.objects.get(email='paul@smith.com')

        self.assertTrue(user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))

    def test_register_view_prevents_error_if_user_already_exists(self):
        User.objects.create_user(
            email='paul@smith.com',
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )

        response = self.client.post('/accounts/register/', {
            'first_name': 'Paul',
            'last_name': 'Smith',
            'email': 'paul@smith.com',
            'password1': 'paulsmith',
            'password2': 'paulsmith'
        })
        message = list(response.context.get('messages'))[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(message.tags, "error")
        self.assertTrue("An account with this email address already exists. Please try to reset your password from the login page." in message.message)


class TestLoginView(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            email='paul@smith.com',
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )

    def test_get_login_view(self):
        response = self.client.get('/accounts/login/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_logs_user_in_with_valid_post_data(self):
        response = self.client.post('/accounts/login/', {
            'email': 'paul@smith.com',
            'password': 'paulsmith'
        })
        user = User.objects.get(email='paul@smith.com')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))
        self.assertTrue(user.is_authenticated)

    def test_login_view_does_not_log_user_in_with_invalid_password(self):
        response = self.client.post('/accounts/login/', {
            'email': 'paul@smith.com',
            'password': 'paulsmit'
        })
        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(user.is_authenticated)

    def test_login_view_does_not_log_user_in_with_invalid_email(self):
        response = self.client.post('/accounts/login/', {
            'email': 'paul@smith.co',
            'password': 'paulsmith'
        })
        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(user.is_authenticated)

    def test_login_view_fails_with_incorrect_email_format(self):
        response = self.client.post('/accounts/login/', {
            'email': 'paulsmithcom',
            'password': 'paulsmith'
        })

        self.assertEqual(response.status_code, 200)


class TestLogoutView(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            email='paul@smith.com',
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )

    def test_logout_view_logs_out_user(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        response = self.client.get('/accounts/logout/')
        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')
        self.assertFalse(user.is_authenticated)

    def test_logout_view_redirects_if_no_user_logged_in(self):
        response = self.client.get('/accounts/logout/')

        self.assertEqual(response.status_code, 302)


class TestAccountView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            email='paul@smith.com',
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )
        User.objects.create_user(
            email='jack@frost.com',
            username='jack@frost.com',
            password='jackfrost',
            first_name='Jack',
            last_name='Frost'
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
    
    def test_get_accounts_view_with_logged_in_user(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        response = self.client.get('/accounts/{0}/'.format(user.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/account.html')

    def test_get_accounts_view_redirects_with_no_user_logged_in(self):
        response = self.client.get('/accounts/1/')

        self.assertEqual(response.status_code, 302)

    def test_get_accounts_view_redirects_if_trying_to_access_another_user_account(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        response = self.client.get('/accounts/2/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))


class TestChangeNameView(TestCase):
    def setUp(self):
        User.objects.create_user(
            email='paul@smith.com',
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )
        User.objects.create_user(
            email='jack@frost.com',
            username='jack@frost.com',
            password='jackfrost',
            first_name='Jack',
            last_name='Frost'
        )

    def test_get_change_name_view(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        response = self.client.get('/accounts/{0}/change_name/'.format(user.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/change_name.html')

    def test_post_change_name_view_succeeds_with_valid_data(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        response = self.client.post('/accounts/{0}/change_name/'.format(user.id), {
            'first_name': 'Bob',
            'last_name': 'Jones'
        })
        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))
        self.assertEqual(user.first_name, 'Bob')
        self.assertEqual(user.last_name, 'Jones')

    def test_get_change_name_view_redirects_if_trying_to_change_another_user(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        response = self.client.get('/accounts/2/change_name/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))


class TestChangeEmailView(TestCase):
    def setUp(self):
        User.objects.create_user(
            email='paul@smith.com',
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )
        User.objects.create_user(
            email='jack@frost.com',
            username='jack@frost.com',
            password='jackfrost',
            first_name='Jack',
            last_name='Frost'
        )

    def test_get_change_email_view(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        response = self.client.get('/accounts/{0}/change_email/'.format(user.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/change_email.html')

    def test_post_change_email_view_succeeds_with_valid_data(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        response = self.client.post('/accounts/{0}/change_email/'.format(user.id), {
            'email1': 'smith@paul.com',
            'email2': 'smith@paul.com'
        })
        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))
        self.assertEqual(user.email, 'smith@paul.com')

    def test_get_change_email_view_redirects_if_trying_to_change_another_user(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        response = self.client.get('/accounts/2/change_email/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))

    def test_post_change_email_view_reloads_page_if_emails_do_not_match(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        response = self.client.post('/accounts/{0}/change_email/'.format(user.id), {
            'email1': 'smith@paul.com',
            'email2': 'smith@paul.co'
        })
        message = list(response.context.get('messages'))[0]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/change_email.html')
        self.assertEqual(message.tags, "error")
        self.assertTrue("The email addresses didn't match." in message.message)


class TestChangePasswordView(TestCase):
    def setUp(self):
        User.objects.create_user(
            email='paul@smith.com',
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )
        User.objects.create_user(
            email='jack@frost.com',
            username='jack@frost.com',
            password='jackfrost',
            first_name='Jack',
            last_name='Frost'
        )

    def test_get_change_password_view(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        response = self.client.get('/accounts/{0}/change_password/'.format(user.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/change_password.html')

    def test_post_change_password_view_succeeds_with_valid_data(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        response = self.client.post('/accounts/{0}/change_password/'.format(user.id), {
            'old_password': 'paulsmith',
            'new_password1': 'smithpaul234',
            'new_password2': 'smithpaul234'
        })
        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))
        self.client.logout()
        self.assertTrue(self.client.login(email='paul@smith.com', password='smithpaul234'))

    def test_get_change_password_view_redirects_if_trying_to_change_another_user(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        response = self.client.get('/accounts/2/change_password/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))

    def test_post_change_password_view_reloads_page_if_invalid_data(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        response = self.client.post('/accounts/{0}/change_password/'.format(user.id), {
            'old_password': 'paulsmith',
            'new_password1': 'smithpaul234',
            'new_password2': ''
        })
        message = list(response.context.get('messages'))[0]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/change_password.html')
        self.assertEqual(message.tags, "error")
        self.assertTrue("An error occured, please see below." in message.message)


class TestChangeTrainingView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            email='paul@smith.com',
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )
        User.objects.create_user(
            email='jack@frost.com',
            username='jack@frost.com',
            password='jackfrost',
            first_name='Jack',
            last_name='Frost'
        )
        Training.objects.create(
            name = 'Test Training',
            description = 'Test description 2',
            course_length = 6,
            min_attendees = 2,
            max_attendees = 12,
            cqc_requirement = False,
            price = 600
        )
        consultancy = Consultancy.objects.create(
            name = 'Test Consultancy',
            description = 'Test description',
            price = 440
        )
        ConsultancyPurchase.objects.create(
            user = user,
            consultancy = consultancy,
            amount_paid = consultancy.price,
            consultancy_date = datetime.date.today() + datetime.timedelta(days=5)
        )

    def setUp(self):
        user = User.objects.get(id=1)
        training = Training.objects.get(id=1)

        TrainingPurchase.objects.create(
            user = user,
            training = training,
            amount_paid = training.price,
            training_date = datetime.date.today() + datetime.timedelta(days=6)
        )

    def test_get_change_training_view(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        order = TrainingPurchase.objects.get(id=1)
        response = self.client.get('/accounts/{0}/t/{1}/'.format(user.id, order.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/change_training.html')

    def test_post_change_training_view_with_valid_data_saves_to_database(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        order = TrainingPurchase.objects.get(id=1)
        new_date = str(datetime.date.today() + datetime.timedelta(days=15))
        response = self.client.post('/accounts/{0}/t/{1}/'.format(user.id, order.id), {
            'training_date': new_date
        })
        order = TrainingPurchase.objects.get(id=1)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))
        self.assertEqual(str(order.training_date), new_date)

    def test_get_change_training_view_redirects_if_date_has_passed(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        order = TrainingPurchase.objects.get(id=1)
        order.training_date -= datetime.timedelta(days=15)
        order.save()
        response = self.client.get('/accounts/{0}/t/{1}/'.format(user.id, order.id))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))

    def test_get_change_training_view_redirects_if_trying_change_another_users_date(self):
        self.client.login(email='jack@frost.com', password='jackfrost')
        user = auth.get_user(self.client)
        order = TrainingPurchase.objects.get(id=1)
        response = self.client.get('/accounts/{0}/t/{1}/'.format(user.id, order.id))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))


class TestChangeConsultancyView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            email='paul@smith.com',
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )
        User.objects.create_user(
            email='jack@frost.com',
            username='jack@frost.com',
            password='jackfrost',
            first_name='Jack',
            last_name='Frost'
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
        Consultancy.objects.create(
            name = 'Test Consultancy',
            description = 'Test description',
            price = 440
        )
        TrainingPurchase.objects.create(
            user = user,
            training = training,
            amount_paid = training.price,
            training_date = datetime.date.today() + datetime.timedelta(days=6)
        )

    def setUp(self):
        user = User.objects.get(id=1)
        consultancy = Consultancy.objects.get(id=1)

        ConsultancyPurchase.objects.create(
            user = user,
            consultancy = consultancy,
            amount_paid = consultancy.price,
            consultancy_date = datetime.date.today() + datetime.timedelta(days=5)
        )

    def test_get_change_consultancy_view(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        order = ConsultancyPurchase.objects.get(id=1)
        response = self.client.get('/accounts/{0}/c/{1}/'.format(user.id, order.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/change_consultancy.html')

    def test_post_change_consultancy_view_with_valid_data_saves_to_database(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        order = ConsultancyPurchase.objects.get(id=1)
        new_date = str(datetime.date.today() + datetime.timedelta(days=15))
        response = self.client.post('/accounts/{0}/c/{1}/'.format(user.id, order.id), {
            'consultancy_date': new_date
        })
        order = ConsultancyPurchase.objects.get(id=1)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))
        self.assertEqual(str(order.consultancy_date), new_date)

    def test_get_change_consultancy_view_redirects_if_date_has_passed(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        user = auth.get_user(self.client)
        order = ConsultancyPurchase.objects.get(id=1)
        order.consultancy_date -= datetime.timedelta(days=15)
        order.save()
        response = self.client.get('/accounts/{0}/c/{1}/'.format(user.id, order.id))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))

    def test_get_change_consultancy_view_redirects_if_trying_change_another_users_date(self):
        self.client.login(email='jack@frost.com', password='jackfrost')
        user = auth.get_user(self.client)
        order = ConsultancyPurchase.objects.get(id=1)
        response = self.client.get('/accounts/{0}/c/{1}/'.format(user.id, order.id))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/{0}/'.format(user.id))
