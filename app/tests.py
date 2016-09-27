"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import os
import tempfile
import logging as log

import django
django.setup()
from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status


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
        from app import tasks
        result = tasks.resize.delay(1)
        result.get()
        self.assertTrue(result.successful())

class AppApiTest(APITestCase, TestCase):
    """Tests for api"""

    def test_api_tasks(self):
        """Tests api tasks list."""
        response = self.client.get(reverse('tasks-list'), format='json')
        self.assertEqual(response.status_code, 200)

    def test_api_task_create(self):
        """Tests api create resize task"""
        from PIL import Image
        import base64

        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image.save(tmp_file)
        tmp_file.close()
        tmp_file = open(tmp_file.name, "rb")
        response = self.client.post(reverse('tasks-list'),
                                    data={'image': tmp_file},
                                    format='multipart')
        tmp_file.close()
        os.unlink(tmp_file.name)
        if response.status_code != status.HTTP_201_CREATED:
            log.error(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)        
