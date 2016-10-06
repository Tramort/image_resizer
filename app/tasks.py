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
    task = models.ResizeTask.objects.get(id=task_id)
    print(task.id, task.receive_time, task.image.path)

    img = Image.open(task.image.path)
    ratio = 0.5
    new_size = [int(i * ratio) for i in img.size]
    img.thumbnail(new_size, Image.ANTIALIAS)

    image_name = os.path.basename(task.image.path)
    splited_name = image_name.rsplit('.', 1)
    splited_name.insert(1, ".thumbnail.")
    image_name = "".join(splited_name)

    temp_io = BuffIO()
    img.save(temp_io, format="JPEG")

    image_file = InMemoryUploadedFile(temp_io, None, image_name, 'image/jpeg',
                                      buffio_len(temp_io), None)

    task.resized_image.save(image_name, image_file)
    task.converted_time = datetime.now()
    task.save()

    Group('clients').send({
        "text": json.dumps(serializers.ResizeTaskSerializer(task).data)
        })
