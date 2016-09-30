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

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
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
    model = models.ResizeTask
    queryset = models.ResizeTask.objects.all()
    serializer_class = serializers.ResizeTaskSerializer
    lookup_field = 'id'
