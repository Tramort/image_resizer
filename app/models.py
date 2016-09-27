"""
Definition of models.
"""

from django.db import models

class ResizeTask(models.Model):
    """Table of tasks to resize images"""
    image = models.ImageField()
    resized_image = models.ImageField(null=True)
    receive_time = models.DateTimeField()
    converted_time = models.DateTimeField(null=True)
