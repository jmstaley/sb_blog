from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from sb_blog.models import Entry

current_site = Site.objects.get_current()

class EntriesFeed(Feed):
    author_name = current_site.domain
    description = '%s blog entries feed' % current_site.domain
    link = '/feeds/blog/'
    title = '%s : blog entries' % current_site.domain

    def items(self):
        return Entry.live.all()

    def item_pubdate(self, item):
        return item.pub_date
