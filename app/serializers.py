"""
serializers
"""
from rest_framework import serializers
from app import models


class ResizeTaskSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializing all ResizeTasks
    """
    class Meta:
        model = models.ResizeTask
        fields = ("id", "receive_time", "image", "resized_image", "converted_time",)
        read_only_fields = ("id", "resized_image", "converted_time", "receive_time")
