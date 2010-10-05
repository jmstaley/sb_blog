import datetime
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255, 
                             help_text='Maximum 250 characters')
    slug = models.SlugField(unique=True,
                            help_text='Automatically generated from title')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/categories/%s' % self.slug

class Entry(models.Model):
    title = models.CharField(max_length=250)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    slug = models.SlugField(unique_for_date='pub_date')
