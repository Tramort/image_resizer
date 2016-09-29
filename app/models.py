"""
Definition of models.
"""

from datetime import datetime
from django.db import models

class ResizeTask(models.Model):
    """Table of tasks to resize images"""
    image = models.ImageField()
    resized_image = models.ImageField(null=True)
    receive_time = models.DateTimeField()
    converted_time = models.DateTimeField(null=True)

    task_result = None # seems only for tests

    def save(self, *args, **kwargs):
        if not self.pk:
            self.receive_time = datetime.now()
            super(ResizeTask, self).save(*args, **kwargs)
            from app import tasks
            self.task_result = tasks.resize.delay(self.id)
        else:
            super(ResizeTask, self).save(*args, **kwargs)
