import datetime
from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField
from markdown import markdown

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

    def live_entry_set(self):
        from sb_blog.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)

class LiveEntryManager(models.Manger):
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
    categories = models.ManyToManyField(Category)
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
