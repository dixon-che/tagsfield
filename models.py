from datetime import datetime

from django.db import models
from django.conf import settings

from tagsfield import utils

class Tag(models.Model):
    value = models.CharField(max_length=50)
    norm_value = models.CharField(max_length=50, editable=False)
    created = models.DateTimeField(editable=False, default=datetime.now)

    class Meta:
        ordering = ('norm_value', 'value')

    def __unicode__(self):
        return self.value

    def save(self, **kwargs):
        self.norm_value = utils.normalize_title(self.value)
        super(Tag, self).save(**kwargs)

    def get_absolute_url(self):
        return utils.tag_url(self.value)
