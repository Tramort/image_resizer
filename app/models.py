"""
Definition of models.
"""

from datetime import datetime
import json
from django.db import models
from channels.channel import Group


class ResizeTask(models.Model):
    """Table of tasks to resize images"""
    image = models.ImageField()
    resized_image = models.ImageField(null=True)
    receive_time = models.DateTimeField()
    converted_time = models.DateTimeField(null=True)

    task_result = None # seems only for tests

    def save(self, run_task=True, *args, **kwargs):
        if not self.pk:
            self.receive_time = datetime.now()
            super(ResizeTask, self).save(*args, **kwargs)
            from app import serializers
            Group('clients').send({"text": json.dumps(serializers.ResizeTaskSerializer(self).data)})
            if run_task:
                from app import tasks
                self.task_result = tasks.resize.delay(self.id)
        else:
            super(ResizeTask, self).save(*args, **kwargs)
