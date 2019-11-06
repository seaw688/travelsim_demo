# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.core.wsgi import get_wsgi_application
from .celery import app as celery_app

__all__ = ('celery_app',)

application = get_wsgi_application()

admin.site.site_header = 'Travel-Sim Admin'
admin.site.site_title = 'Travel-Sim Admin Portal'
admin.site.index_title = 'Welcome to Travel-Sim Admin Portal'