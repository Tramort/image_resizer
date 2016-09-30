"""
serializers
"""
from rest_framework import serializers
from app import models


class ResizeTaskSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializing all ResizeTasks
    """
    receive_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                             required=False, read_only=True)
    converted_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                               required=False, read_only=True)

    class Meta:
        model = models.ResizeTask
        fields = ("id", "receive_time", "image", "resized_image", "converted_time",)
        read_only_fields = ("id", "resized_image", "converted_time", "receive_time")
