"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import os
import tempfile
import logging as log
import json

import django

django.setup()
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import File
from django.conf import settings
# run celery task synchronous
settings.BROKER_BACKEND = 'memory'
settings.CELERY_ALWAYS_EAGER = True

from rest_framework.test import APITestCase
from rest_framework import status

from channels import Group
from channels.tests import ChannelTestCase

from app import utils


# TODO: Configure your database in settings.py and sync before running tests.



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
        from app import models

        temp_image = utils.TempImageFile()
        task = models.ResizeTask(image=File(temp_image.file))
        task.save(run_task=False)
        result = tasks.resize.delay(task.id)
        result.wait(10)
        self.assertTrue(result.successful())

class AppApiTest(APITestCase, TestCase):
    """Tests for rest api"""

    def test_api_tasks(self):
        """Tests api tasks list."""
        response = self.client.get(reverse('tasks-list'), format='json')
        self.assertEqual(response.status_code, 200)

    def test_api_task_create(self):
        """Tests api create resize task"""
        temp_image = utils.TempImageFile()
        response = self.client.post(reverse('task-create'),
                                    data={'image': temp_image.file},
                                    format='multipart')
        if response.status_code != status.HTTP_201_CREATED:
            log.error(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_get_task(self):
        """Tests api get resize task"""
        from app import models

        temp_image = utils.TempImageFile()
        task = models.ResizeTask(image=File(temp_image.file))
        task.save(run_task=False)

        response = self.client.get(reverse('task-detail', kwargs={"id":task.id}), format='json')
        self.assertEqual(response.status_code, 200)


class WebsocketTest(ChannelTestCase, TestCase):
    """Tests for websocket"""
    def test_task_complete_notification(self):
        """
        Test for notification after resize task complete
        """
        Group("clients").add(u"test-channel")
        temp_image = utils.TempImageFile()
        from app import models
        task = models.ResizeTask(image=File(temp_image.file))
        task.save()
        task.task_result.wait(10)
        result = self.get_next_message(u"test-channel", require=True)
        self.assertNotEqual(json.loads(result['text'])["resized_image"], None)
