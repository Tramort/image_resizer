"""
tasks for ImageResizer app
"""
import os
from datetime import datetime
import json

from ImageResizer.celery import app
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
try:
    # python 2
    from StringIO import StringIO as BuffIO

    def buffio_len(buffio):
        return buffio.len
except ImportError:
    # python 3
    from io import BytesIO as BuffIO

    def buffio_len(buffio):
        return buffio.getbuffer().nbytes

from app import models, serializers
from channels.channel import Group


@app.task(bind=True)
def resize(self, task_id):
    """
    resizing image
    """
    image_to_resize = models.ImageToResize.objects.get(id=task_id)
    image_path = image_to_resize.image.path
    img = Image.open(image_path)
    ratio = 0.5
    new_size = [int(i * ratio) for i in img.size]
    img.thumbnail(new_size, Image.ANTIALIAS)

    image_name = os.path.basename(image_path)
    splited_name = image_name.rsplit('.', 1)
    splited_name.insert(1, ".thumbnail.")
    image_name = "".join(splited_name)

    temp_io = BuffIO()
    img.save(temp_io, format="JPEG")

    image_file = InMemoryUploadedFile(temp_io, None, image_name, 'image/jpeg',
                                      buffio_len(temp_io), None)

    resized_image = models.ResizedImage(image_to_resize=image_to_resize,
                                        image=image_file)
    resized_image.save(force_insert=True)
