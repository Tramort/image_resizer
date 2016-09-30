"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from rest_framework import generics

from . import forms, models, tasks, serializers


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )

class ResizeTaskList(generics.ListAPIView):
    """
    API endpoint that represents a list of resize tasks.
    """
    queryset = models.ResizeTask.objects.all()
    serializer_class = serializers.ResizeTaskSerializer

class ResizeTaskCreate(generics.CreateAPIView):
    """
    API endpoint create resize task.
    """
    serializer_class = serializers.ResizeTaskSerializer

class ResizeTaskDetail(generics.RetrieveAPIView):
    """
    API endpoint to represent one resize task.
    """
    model = models.ResizeTask
    queryset = models.ResizeTask.objects.all()
    serializer_class = serializers.ResizeTaskSerializer
    lookup_field = 'id'
