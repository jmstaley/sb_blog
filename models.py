from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.title
