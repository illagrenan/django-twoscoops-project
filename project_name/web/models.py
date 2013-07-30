# -*- encoding: utf-8 -*-

from django.db import models


class FooModel(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100, verbose_name='Name')
    description = models.TextField(blank=True, verbose_name='Description')

    class Meta:
        verbose_name = verbose_name_plural = 'foo_model'