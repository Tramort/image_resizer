"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime

from . import forms, models, tasks


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if "POST" == request.method:
        form = forms.AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            task = models.ResizeTask(image=request.FILES["image"], receive_time=datetime.now())
            task.save()
            tasks.resize.delay(task.id)
    else:
        form = forms.AddImageForm()
    resize_tasks = models.ResizeTask.objects.all().order_by("-id")

    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'tasks': resize_tasks,
            'form': form,
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
