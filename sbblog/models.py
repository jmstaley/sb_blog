import datetime
from akismet import Akismet

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator
from django.contrib.sites.models import Site
from django.utils.encoding import smart_str

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
    APPROVE_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (APPROVE_STATUS, 'To Approve'),
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

    objects = models.Manager()
    live = LiveEntryManager()

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ('-pub_date',)
        permissions = (
            ('can_publish', 'Can set the entry live'),
        )

    def save(self, force_insert=False, force_update=False):
        if getattr(settings, 'HTML_ENTRY', None):
            self.body_html = self.body
            self.excerpt_html = self.excerpt
        else:
            self.body_html = markdown(self.body)
            if self.excerpt:
                self.excerpt_html = markdown(self.excerpt)
        if self.tags:
            tags = []
            for tag in self.tags.split(','):
                tag = tag.strip()
                tags.append(tag.replace(' ', '-'))
            self.tags = ','.join(tags)
        super(Entry, self).save(force_insert, force_update)

    def clean(self):
        from django.core.exceptions import ValidationError
        can_publish = self.author.has_perm('sbblog.can_publish')
        if not can_publish and self.status == Entry.LIVE_STATUS:
            raise ValidationError('You don\'t have permissons to set entries live, please to "To Approve"')

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

class EntryModerator(CommentModerator):
    auto_moderate_field = 'pub_date'
    moderate_after = 30
    email_notification = True
    enable_field = 'enable_comments'

    def moderate(self, comment, content_object, request):
        already_moderated = super(EntryModerator, self).moderate(comment, content_object, request)
        if already_moderated:
            return True
        akismet_api = Akismet(key=settings.AKISMET_API_KEY,
                              blog_url="http://%s/" % Site.objects.get_current().domain)
        if akismet_api.verify_key():
            akismet_data = {'comment_type': 'comment',
                           'referrer': request.META['HTTP_REFERER'],
                           'user_ip': comment.ip_address,
                           'user_agent': request.META['HTTP_USER_AGENT']}
            return akismet_api.comment_check(smart_str(comment.comment),
                                             akismet_data,
                                             build_data=True)
        return False

moderator.register(Entry, EntryModerator)
