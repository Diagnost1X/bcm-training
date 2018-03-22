# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from accounts.models import User

from testimonials.models import Testimonial


# Create your tests here.
class TestShowTestimonialView(TestCase):
    def test_get_testimonials_view(self):
        response = self.client.get('/testimonials/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'testimonials/testimonials.html')


class TestNewTestimonialView(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        User.objects.create_user(
            email='staff@email.com',
            username='staff@email.com',
            password='staffemail',
            first_name='Staff',
            last_name='Email',
            is_staff=True
        )

    def setUp(self):
        user = User.objects.get(id=1)
        Testimonial.objects.create(
            comments = 'This is a test',
            first_name = 'Paul',
            initial = 'S',
            user = user
        )

    def test_add_new_testimonial_view_with_no_user_logged_in(self):
        response = self.client.get('/testimonials/new_testimonial/')

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'testimonials/testimonial_form.html')

    def test_add_new_testimonial_view_with_logged_in_user(self):
        self.client.login(email='jack@frost.com', password='jackfrost')
        response = self.client.get('/testimonials/new_testimonial/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'testimonials/testimonial_form.html')

    def test_add_new_testimonial_view_with_user_that_already_has_a_testimonial(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        response = self.client.get('/testimonials/new_testimonial/')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/testimonials/')
        self.assertTemplateNotUsed(response, 'testimonials/testimonial_form.html')

    def test_new_testimonial_post_method_with_comment(self):
        self.client.login(email='jack@frost.com', password='jackfrost')
        response = self.client.post('/testimonials/new_testimonial/', {'comments': 'This is Jacks test'})
        testimonial = Testimonial.objects.get(id=2)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/testimonials/')
        self.assertEqual(testimonial.first_name, 'Jack')
        self.assertEqual(testimonial.initial, 'F')
        self.assertEqual(testimonial.comments, 'This is Jacks test')


class TestEditTestimonialView(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        User.objects.create_user(
            email='staff@email.com',
            username='staff@email.com',
            password='staffemail',
            first_name='Staff',
            last_name='Email',
            is_staff=True
        )

    def setUp(self):
        user = User.objects.get(id=1)
        Testimonial.objects.create(
            comments = 'This is a test',
            first_name = 'Paul',
            initial = 'S',
            user = user
        )

    def test_edit_testimonial_view_with_no_user_logged_in(self):
        testimonial = Testimonial.objects.get(id=1)
        response = self.client.get('/testimonials/edit/{0}/'.format(testimonial.id))

        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'testimonials/testimonial_form.html')

    def test_edit_testimonial_view_with_logged_in_user(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        testimonial = Testimonial.objects.get(id=1)
        response = self.client.get('/testimonials/edit/{0}/'.format(testimonial.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'testimonials/testimonial_form.html')

    def test_edit_testimonial_view_with_user_trying_to_edit_another_users_testimonial(self):
        self.client.login(email='jack@frost.com', password='jackfrost')
        testimonial = Testimonial.objects.get(id=1)
        response = self.client.get('/testimonials/edit/{0}/'.format(testimonial.id))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/testimonials/')
        self.assertTemplateNotUsed(response, 'testimonials/testimonial_form.html')

    def test_edit_testimonial_view_with_staff_user(self):
        self.client.login(email='staff@email.com', password='staffemail')
        testimonial = Testimonial.objects.get(id=1)
        response = self.client.get('/testimonials/edit/{0}/'.format(testimonial.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'testimonials/testimonial_form.html')

    def test_edit_testimonial_post_method_with_comment_changed(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        testimonial = Testimonial.objects.get(id=1)
        response = self.client.post('/testimonials/edit/{0}/'.format(testimonial.id), {'comments': 'This is a new test'})
        testimonial = Testimonial.objects.get(id=1)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/testimonials/')
        self.assertEqual(testimonial.comments, 'This is a new test')

    def test_edit_testimonial_with_id_that_does_not_exist(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        response = self.client.get('/testimonials/edit/5/')

        self.assertEqual(response.status_code, 404)

    
class TestDeleteTestimonialView(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        User.objects.create_user(
            email='staff@email.com',
            username='staff@email.com',
            password='staffemail',
            first_name='Staff',
            last_name='Email',
            is_staff=True
        )

    def setUp(self):
        user = User.objects.get(id=1)
        Testimonial.objects.create(
            comments = 'This is a test',
            first_name = 'Paul',
            initial = 'S',
            user = user
        )

    def test_delete_testimonial_view_with_correct_user_logged_in(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        testimonial = Testimonial.objects.get(id=1)
        response = self.client.get('/testimonials/delete/{0}/'.format(testimonial.id))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/testimonials/')
        self.assertFalse(Testimonial.objects.filter(id=1))

    def test_delete_testimonial_view_with_no_user_logged_in(self):
        testimonial = Testimonial.objects.get(id=1)
        response = self.client.get('/testimonials/delete/{0}/'.format(testimonial.id))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Testimonial.objects.filter(id=1))
    
    def test_delete_testimonial_view_with_wrong_user_logged_in(self):
        self.client.login(email='jack@frost.com', password='jackfrost')
        testimonial = Testimonial.objects.get(id=1)
        response = self.client.get('/testimonials/delete/{0}/'.format(testimonial.id))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/testimonials/')
        self.assertTrue(Testimonial.objects.filter(id=1))

    def test_delete_testimonial_view_with_staff_user(self):
        self.client.login(email='staff@email.com', password='staffemail')
        testimonial = Testimonial.objects.get(id=1)
        response = self.client.get('/testimonials/delete/{0}/'.format(testimonial.id))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/testimonials/')
        self.assertFalse(Testimonial.objects.filter(id=1))

    def test_delete_testimonial_with_id_that_does_not_exist(self):
        self.client.login(email='paul@smith.com', password='paulsmith')
        response = self.client.get('/testimonials/delete/5/')

        self.assertEqual(response.status_code, 404)
