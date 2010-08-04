# -*- coding:utf-8 -*-
from django.template import Library
from django.conf import settings

from tagsfield import utils

register = Library()

@register.filter
def tag_url(value):
    return utils.tag_url(value)
