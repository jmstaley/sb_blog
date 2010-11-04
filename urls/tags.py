from django.conf.urls.defaults import *
from sb_blog.models import Entry
from tagging.models import Tag

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list',
     {'queryset': Tag.objects.all()}),
    (r'^(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list',
     {'queryset_or_model': Entry.live.all(),
      'template_name': 'sb_blog/entries_by_tag.html'}),
)
