# -*- coding:utf-8 -*-
import re

from django.utils.http import urlquote
from django.conf import settings

def normalize_title(title):
    '''
    Casts strings to a representation suitable for searching
    stripping out details insignificant for comparision.

    This function has a sibling in js/tags.js, don't forget to
    update it whenever this function is changed.
    '''
    STROKES = {
        u'Ø': u'O', u'ø': u'o',
        u'Đ': u'D', u'đ': u'd',
        u'Ħ': u'H', u'ħ': u'h',
        u'Ł': u'L', u'ł': u'l',
        u'Ŧ': u'T', u'ŧ': u't',
    }
    title=title.decode(settings.DEFAULT_CHARSET)
    title=title.lower()
    import unicodedata
    title = unicodedata.normalize('NFD', title)
    title = u''.join(c for c in title if not unicodedata.combining(c))
    title = u''.join(STROKES.get(l, l) for l in title)
    safe_title = title # safe_title can't be empty since nothing has been removed yet
    title=re.sub(re.compile(r'\bthe\b',re.I),'',title)
    title=re.sub(re.compile(r'[\,\.\(\)\-\!\'\"\`\?\_\:\;\$\]\[\#\/]'),'',title)
    title=re.sub(re.compile(r'\s+'),'',title)
    return (title or safe_title).encode(settings.DEFAULT_CHARSET)

def tag_url(value):
    if not getattr(settings, 'TAGS_URL', ''):
        return ''
    try:
        return settings.TAGS_URL % urlquote(value)
    except TypeError:
        return settings.TAGS_URL + urlquote(value)
