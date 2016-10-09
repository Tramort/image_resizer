"""
Definition of models.
"""

from django.utils import timezone
import json
from django.db import models
from channels.channel import Group
from django.contrib.contenttypes.fields import GenericRelation


class AbstractImage(models.Model):
    """Table of tasks to resize images"""
    image = models.ImageField(blank=False)
    time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.time:
            self.time = timezone.now()
        super(AbstractImage, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class ImageToResize(AbstractImage):
    """Table of tasks to resize images"""
    run_task = True

    def save(self, run_task=True, *args, **kwargs):
        if self._state.adding:
            super(ImageToResize, self).save(*args, **kwargs)

            from app import serializers
            Group('clients').send({
                "text": json.dumps(
                    {
                        "event": "img_added",
                        "img": serializers.ImageToResizeSerializer(self).data
                    })
                })

            if run_task and self.run_task:
                from app import tasks
                self.task_result = tasks.resize.delay(self.id)

        else:
            super(ImageToResize, self).save(*args, **kwargs)


class ResizedImage(AbstractImage):
    image_to_resize = models.OneToOneField(ImageToResize, on_delete=models.CASCADE,
                                           primary_key=True, related_name='resized_image')

    def save(self, *args, **kwargs):
        if self._state.adding:
            super(ResizedImage, self).save(*args, **kwargs)

            from app import serializers
            Group('clients').send({
                "text": json.dumps(
                    {
                        "event": "img_resized",
                        "img": serializers.ResizedImageSerializer(self).data
                    })
                })
        else:
            super(ResizedImage, self).save(*args, **kwargs)
