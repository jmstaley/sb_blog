from django.views.generic.list_detail import object_list

from models import Entry

objs_per_page = 5

def entries_index(request, page=1):
    entries = Entry.live.order_by('-pub_date')
    return object_list(request, queryset=entries, paginate_by=5, page=page, template_name='sb_blog/entry_index.html')
