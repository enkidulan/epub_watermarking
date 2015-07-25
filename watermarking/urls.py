"""
List of URL mapping
"""
from django.conf.urls import patterns, url
from django.conf import settings
from django.http import HttpResponseRedirect

from . import views


# pylint: disable=invalid-name
urlpatterns = patterns(
    '',
    url(r'^add_to_watermark_queue?', views.add_to_watermark_queue),
    url(r'^$', lambda r: HttpResponseRedirect('index.html')),
    url(r'^(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.FRONTEND_APP_PATH}),
)
