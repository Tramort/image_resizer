"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
django.setup()
from django.test import TestCase
from app import tasks

# TODO: Configure your database in settings.py and sync before running tests.

# run celery task synchronous
from django.conf import settings
settings.CELERY_ALWAYS_EAGER = True

class ViewTest(TestCase):
    """Tests for the application views."""

    def test_home(self):
        """Tests the home page."""
        response = self.client.get('/')
        self.assertContains(response, 'Home Page', 1, 200)

    def test_contact(self):
        """Tests the contact page."""
        response = self.client.get('/contact')
        self.assertContains(response, 'Contact', 3, 200)

    def test_about(self):
        """Tests the about page."""
        response = self.client.get('/about')
        self.assertContains(response, 'About', 3, 200)

    def test_resize_task(self):
        """Tests resize task"""
        result = tasks.resize.delay(1)
        result.get()
        self.assertTrue(result.successful())
