"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import logging as log
import json

import django
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import File
from django.conf import settings
from django.test.utils import override_settings

from rest_framework.test import APITestCase
from rest_framework import status

from channels import Group
from channels.tests import ChannelTestCase

from app import utils


django.setup()
# run celery task synchronous
settings.BROKER_BACKEND = 'memory'
settings.CELERY_ALWAYS_EAGER = True


# TODO: Configure your database in settings.py and sync before running tests.


class ViewTest(TestCase):
    """Tests for the application views."""

    def test_home(self):
        """Tests the home page."""
        response = self.client.get('/')
        self.assertContains(response, 'Home Page', 1, 200)

    def test_resize_task(self):
        """Tests resize task"""
        from app import tasks
        from app import models

        temp_image = utils.TempImageFile()
        image_to_resize = models.ImageToResize(image=File(temp_image.file))
        image_to_resize.save(run_task=False)
        with self.assertNumQueries(2):
            result = tasks.resize.delay(image_to_resize.id)
            result.wait(10)
        self.assertTrue(result.successful())
        resized_image = models.ResizedImage.objects.get(image_to_resize=image_to_resize)
        self.assertTrue(resized_image.image)

    def test_resize_task_inline(self):
        """Tests resize task"""
        from app import tasks, models

        temp_image = utils.TempImageFile()
        image_to_resize = models.ImageToResize(image=File(temp_image.file))
        image_to_resize.save(run_task=False)
        with self.assertNumQueries(2):
            tasks.resize(image_to_resize.id)
        resized_image = models.ResizedImage.objects.get(image_to_resize=image_to_resize)
        self.assertTrue(resized_image.image)


class AppApiTest(APITestCase, TestCase):
    """Tests for rest api"""

    def test_api_tasks(self):
        """Tests api tasks list."""
        from app import models
        temp_image = utils.TempImageFile()
        image_to_resize = models.ImageToResize(image=File(temp_image.file))
        image_to_resize.save(run_task=False)

        image_to_resize.pk = None
        image_to_resize.save(run_task=False)

        with self.assertNumQueries(1):
            response = self.client.get(reverse('tasks-list'), format='json')
        self.assertEqual(response.status_code, 200)

    def test_api_task_create(self):
        """Tests api create resize task"""
        temp_image = utils.TempImageFile()
        from app import models
        models.ImageToResize.run_task = False
        with self.assertNumQueries(1):
            response = self.client.post(reverse('task-create'),
                                        data={'image': temp_image.file},
                                        format='multipart')
        if response.status_code != status.HTTP_201_CREATED:
            log.error(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_get_task(self):
        """Tests api get resize task"""
        from app import models, tasks

        temp_image = utils.TempImageFile()
        image_to_resize = models.ImageToResize(image=File(temp_image.file))
        image_to_resize.save(run_task=False)

        # get before task ends
        with self.assertNumQueries(1):
            response = self.client.get(reverse('task-detail',
                                               kwargs={"id": image_to_resize.id}),
                                       format='json')
        data = json.loads(response.content.decode(encoding=response.charset))
        self.assertNotEqual(data["time"], None)
        self.assertEqual(response.status_code, 200)

        from app import tasks
        result = tasks.resize.delay(image_to_resize.id)
        result.wait(10)

        # get after task ends
        with self.assertNumQueries(1):
            response = self.client.get(reverse('task-detail',
                                               kwargs={"id": image_to_resize.id}),
                                       format='json')
        data = json.loads(response.content.decode(encoding=response.charset))
        print(data)
        self.assertNotEqual(data["time"], None)
        self.assertNotEqual(data["resized_image"]["image"], None)
        self.assertEqual(response.status_code, 200)


class WebsocketTest(ChannelTestCase, TestCase):
    """Tests for websocket"""
    def test_task_complete_notification(self):
        """
        Test for notification after resize task complete
        """
        Group("clients").add(u"test-channel")
        temp_image = utils.TempImageFile()
        from app import models, tasks
        image_to_resize = models.ImageToResize(image=File(temp_image.file))
        image_to_resize.save(run_task=False)

        result = self.get_next_message(u"test-channel", require=True)
        self.assertEqual(json.loads(result['text'])["event"], "img_added")
        self.assertNotEqual(json.loads(result['text'])["img"]["time"], None)
        self.assertNotEqual(json.loads(result['text'])["img"]["image"], None)

        tasks.resize.delay(image_to_resize.id).wait(10)

        result = self.get_next_message(u"test-channel", require=True)
        self.assertEqual(json.loads(result['text'])["event"], "img_resized")
        self.assertNotEqual(json.loads(result['text'])["img"]["time"], None)
        self.assertNotEqual(json.loads(result['text'])["img"]["image"], None)
