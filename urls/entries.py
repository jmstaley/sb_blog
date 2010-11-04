from django.conf.urls.defaults import *

from sb_blog.models import Entry

entry_info_dict = {'queryset': Entry.live.all(),
                   'date_field': 'pub_date'}

date_info_dict = {'queryset': Entry.live.all(),
                  'date_field': 'pub_date',
                  'month_format': 'm'}

urlpatterns = patterns('django.views.generic.date_based',
    (r'^$', 'archive_index', entry_info_dict, 'blog_entry_archive_index'),
    (r'^(?P<year>\d{4})/$', 'archive_year', entry_info_dict,
     'blog_entry_archive_year'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', date_info_dict,
     'blog_entry_archive_month'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'archive_day',
     date_info_dict, 'blog_entry_archive_day'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
     'object_detail', date_info_dict, 'blog_entry_detail'),
)
