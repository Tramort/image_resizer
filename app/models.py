"""
Definition of models.
"""

from django.db import models
from datetime import datetime

class ResizeTask(models.Model):
    """Table of tasks to resize images"""
    image = models.ImageField()
    resized_image = models.ImageField(null=True)
    receive_time = models.DateTimeField()
    converted_time = models.DateTimeField(null=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.receive_time = datetime.now()
            super(ResizeTask, self).save(*args, **kwargs)
            from app import tasks
            tasks.resize.delay(self.id, None)
        else:
            super(ResizeTask, self).save(*args, **kwargs)

