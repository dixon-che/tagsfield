# -*- coding:utf-8 -*-
from django.db import models
from django import forms
from django.template import loader, Context
from django.utils.safestring import mark_safe
from django.conf import settings

from tagsfield.models import Tag
from tagsfield.utils import normalize_title

class TagsWidget(forms.Widget):
    choices = [] # contrib.admin can't live without it

    class Media:
        js = ['tagsfield/js/tags.js']
        css = {
            'all': ['tagsfield/css/tags.css']
        }

    def __init__(self, tag_choices, *args, **kwargs):
        super(TagsWidget, self).__init__(*args, **kwargs)
        if hasattr(tag_choices, '__call__'):
            self.tag_choices = tag_choices
        else:
            self.tag_choices = lambda: tag_choices

    def value_from_datadict(self, data, files, name):
        return [v for v in data.getlist(name) if v]

    def render(self, name, value, attrs=None):
        if value is None:
            value = []
        tags_dict = dict(self.tag_choices())
        value_tags = [tags_dict.get(v, v) for v in value]
        tags = tags_dict.values()
        template = loader.get_template('tags/tag_widget.html')
        context = Context({
            'id': attrs['id'],
            'name': name,
            'tags': tags,
            'value_tags': value_tags,
            'media_url': settings.MEDIA_URL,
            'show_as_url': bool(getattr(settings, 'TAGS_URL', '')),
            'max_length': attrs.get('max_length'),
        })
        return mark_safe(template.render(context))


class TagsFormField(forms.Field):
    hidden_widget = forms.MultipleHiddenInput


class TagsField(models.ManyToManyField):
    def formfield(self, **kwargs):
        model = self.rel.to
        tag_choices = lambda: ((t.id, t.value) for t in model.objects.all())
        attrs = {'max_length': model._meta.get_field('value').max_length}
        defaults = {
            'widget': TagsWidget(tag_choices, attrs=attrs),
        }
        defaults.update(kwargs)
        return TagsFormField(**defaults)

    def _get_tag(self, value):
        norm_value = normalize_title(value)
        tag, created = self.rel.to._default_manager.get_or_create(
            norm_value=norm_value,
            defaults={'value': value}
        )
        return tag

    def save_form_data(self, instance, data):
        tags = [self._get_tag(value) for value in data]
        setattr(instance, self.attname, tags)
