"""
Definition of urls for ImageResizer.
"""

from datetime import datetime
from django.conf.urls import url, include
import django.contrib.auth.views
import django.views.static

import app.forms
import app.views
import settings

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    url(r'^media/(?P<path>.*)$', django.views.static.serve, {
        'document_root': settings.MEDIA_ROOT}),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/tasks/$', app.views.ResizeTaskList.as_view(), name="tasks-list"),
    url(r'^api/task/(?P<id>\d+)$', app.views.ResizeTaskDetail.as_view(), name="task-detail"),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
