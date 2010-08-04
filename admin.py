# -*- coding:utf-8 -*-
from django.contrib import admin

from models import Tag

admin.site.register(Tag, 
    list_display = ['value', 'norm_value', 'created'],
)
