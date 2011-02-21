from django.conf.urls.defaults import *
from sbblog.models import Entry
from tagging.models import Tag

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list',
     {'queryset': Tag.objects.all()}),
    (r'^(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list',
     {'queryset_or_model': Entry.live.all(),
      'template_name': 'sbblog/entries_by_tag.html'},
      'entries_by_tag'),
)
