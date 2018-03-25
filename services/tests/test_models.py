# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.test import TestCase

from accounts.models import User
from services.models import (Consultancy, ConsultancyPurchase, Training,
                             TrainingPurchase)


# Create your tests here.
class TestTrainingModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        training = Training(
            name = 'Test Training',
            description = 'Test description',
            course_length = 5.5,
            min_attendees = 2,
            max_attendees = 10,
            cqc_requirement = True,
            price = 550
        )
        training.save()

    def test_training_model_saves_with_valid_data(self):
        training = Training.objects.get(id=1)

        self.assertEqual(training.name, 'Test Training')
        self.assertEqual(training.description, 'Test description')
        self.assertEqual(training.course_length, 5.5)
        self.assertEqual(training.min_attendees, 2)
        self.assertEqual(training.max_attendees, 10)
        self.assertEqual(training.cqc_requirement, True)
        self.assertEqual(training.price, 550)

    def test_training_model_name_displays_correctly(self):
        training = Training.objects.get(id=1)

        self.assertEqual(str(training), 'Test Training')


class TestConsultancyModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        consultancy = Consultancy(
            name = 'Test Consultancy',
            description = 'Test description',
            price = 440
        )
        consultancy.save()

    def test_consultancy_model_saves_correctly_with_valid_data(self):
        consultancy = Consultancy.objects.get(id=1)

        self.assertEqual(consultancy.name, 'Test Consultancy')
        self.assertEqual(consultancy.description, 'Test description')
        self.assertEqual(consultancy.price, 440)

    def test_consultancy_model_name_displays_correctly(self):
        consultancy = Consultancy.objects.get(id=1)

        self.assertEqual(str(consultancy), 'Test Consultancy')


class TestTrainingPurchaseModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        training = Training(
            name = 'Test Training',
            description = 'Test description',
            course_length = 5.5,
            min_attendees = 2,
            max_attendees = 10,
            cqc_requirement = True,
            price = 550
        )
        training.save()

        User.objects.create_user(
            email='paul@smith.com',
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )

    def setUp(self):
        user = User.objects.get(id=1)
        training = Training.objects.get(id=1)

        training_purchase = TrainingPurchase(
            user = user,
            training = training,
            amount_paid = training.price,
            training_date = datetime.date.today() + datetime.timedelta(days=5)
        )
        training_purchase.save()

    def test_training_purchase_model_saves_with_valid_data(self):
        user = User.objects.get(id=1)
        training = Training.objects.get(id=1)
        training_purchase = TrainingPurchase.objects.get(id=1)

        self.assertEqual(training_purchase.user, user)
        self.assertEqual(training_purchase.training, training)
        self.assertEqual(training_purchase.amount_paid, training.price)
        self.assertEqual(str(training_purchase.training_date),
                         str(datetime.date.today() + datetime.timedelta(days=5)))

    def test_training_purchase_model_saves_default_purchase_date(self):
        training_purchase = TrainingPurchase.objects.get(id=1)

        self.assertEqual(training_purchase.purchase_date, datetime.date.today())

    def test_training_purchase_model_has_passed_property_works_for_future_date(self):
        training_purchase = TrainingPurchase.objects.get(id=1)

        self.assertFalse(training_purchase.has_passed)

    def test_training_purchase_model_has_passed_property_works_for_past_date(self):
        training_purchase = TrainingPurchase.objects.get(id=1)
        training_purchase.training_date = datetime.date.today() + datetime.timedelta(days=-5)
        training_purchase.save()

        self.assertTrue(training_purchase.has_passed)


class TestConsultancyPurchaseModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        consultancy = Consultancy(
            name = 'Test Consultancy',
            description = 'Test description',
            price = 440
        )
        consultancy.save()

        User.objects.create_user(
            email='paul@smith.com',
            username='paul@smith.com',
            password='paulsmith',
            first_name='Paul',
            last_name='Smith'
        )

    def setUp(self):
        user = User.objects.get(id=1)
        consultancy = Consultancy.objects.get(id=1)

        consultancy_purchase = ConsultancyPurchase(
            user = user,
            consultancy = consultancy,
            amount_paid = consultancy.price,
            consultancy_date = datetime.date.today() + datetime.timedelta(days=5)
        )
        consultancy_purchase.save()

    def test_consultancy_purchase_model_saves_with_valid_data(self):
        user = User.objects.get(id=1)
        consultancy = Consultancy.objects.get(id=1)
        consultancy_purchase = ConsultancyPurchase.objects.get(id=1)

        self.assertEqual(consultancy_purchase.user, user)
        self.assertEqual(consultancy_purchase.consultancy, consultancy)
        self.assertEqual(consultancy_purchase.amount_paid, consultancy.price)
        self.assertEqual(str(consultancy_purchase.consultancy_date),
                         str(datetime.date.today() + datetime.timedelta(days=5)))

    def test_consultancy_purchase_model_saves_default_purchase_date(self):
        consultancy_purchase = ConsultancyPurchase.objects.get(id=1)

        self.assertEqual(consultancy_purchase.purchase_date, datetime.date.today())

    def test_consultancy_purchase_model_has_passed_property_works_for_future_date(self):
        consultancy_purchase = ConsultancyPurchase.objects.get(id=1)

        self.assertFalse(consultancy_purchase.has_passed)

    def test_consultancy_purchase_model_has_passed_property_works_for_past_date(self):
        consultancy_purchase = ConsultancyPurchase.objects.get(id=1)
        consultancy_purchase.consultancy_date = datetime.date.today() + datetime.timedelta(days=-5)
        consultancy_purchase.save()

        self.assertTrue(consultancy_purchase.has_passed)
