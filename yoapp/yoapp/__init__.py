# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .celery import app as celery_app
from django.contrib import admin
from django.core.wsgi import get_wsgi_application
from yoapp.utils import AESCipher
__all__ = ('celery_app',)

application = get_wsgi_application()

admin.site.site_header = 'Halap-YO Admin'
admin.site.site_title = 'Halap-YO Admin Portal'
admin.site.index_title = 'Welcome to Halap-YO Admin Portal'

aes_key = '5aQaH74fEezKjR94'
cipher = AESCipher(aes_key)