"""
serializers
"""
from rest_framework import serializers
from app import models


class ImageSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                     required=False, read_only=True)

    class Meta:
        read_only_fields = ("id", "time",)


class ResizedImageSerializer(ImageSerializer):

    class Meta:
        model = models.ResizedImage


class ResizedImageSerializer(ImageSerializer):
    class Meta:
        model = models.ResizedImage


class ImageToResizeSerializer(ResizedImageSerializer):
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                     required=False, read_only=True)

    class Meta:
        model = models.ImageToResize
        read_only_fields = ("id", "time")


class FullResizeTaskSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                     required=False, read_only=True)
    resized_image = ResizedImageSerializer(read_only=True)

    class Meta:
        model = models.ImageToResize
        fields = ("id", "time", "image", "resized_image")
        read_only_fields = ("id", "time", "resized_image")
