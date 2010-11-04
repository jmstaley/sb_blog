from django.conf.urls.defaults import *

from sb_blog.models import Category

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list',
     {'queryset': Category.objects.all()}),
    (r'^(?P<slug>[-\w]+)/$', 'sb_blog.views.category_detail'),
)
