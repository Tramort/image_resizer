"""
serializers
"""
from datetime import datetime
from rest_framework import serializers
from app import models, tasks

class ResizeTaskSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializing all ResizeTasks
    """
    class Meta:
        model = models.ResizeTask
        fields = ("receive_time", "image", "resized_image", "converted_time",)
        read_only_fields = ("resized_image", "converted_time", "receive_time")

    def create(self, validated_data):
        """create new resize task"""
        task = models.ResizeTask(image=validated_data["image"], receive_time=datetime.now())
        task.save()
        tasks.resize.delay(task.id)
        return task
