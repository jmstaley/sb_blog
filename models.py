from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255, 
                             help_text="Maximum 250 characters")
    slug = models.SlugField(unique=True,
                            help_text="Automatically generated from title")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.title
