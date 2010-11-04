import datetime
from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag
from markdown import markdown

class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(\
            status=self.model.LIVE_STATUS)

class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft')
    )

    author = models.ForeignKey(User)
    title = models.CharField(max_length=250)
    excerpt = models.TextField(blank=True)
    excerpt_html = models.TextField(editable=False, blank=True)
    body = models.TextField()
    body_html = models.TextField(editable=False, blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    slug = models.SlugField(unique_for_date='pub_date')
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
    tags = TagField()

    live = LiveEntryManager()
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ('-pub_date',)

    def save(self, force_insert=False, force_update=False):
        self.body_html = markdown(self.body)
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        super(Entry, self).save(force_insert, force_update)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog_entry_detail', (), {'year': self.pub_date.strftime('%Y'),
                                          'month': self.pub_date.strftime('%m'),
                                          'day': self.pub_date.strftime('%d'),
                                          'slug': self.slug})

    def get_tags(self):
        return Tag.objects.get_for_object(self)
