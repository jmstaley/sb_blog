import operator
from django import template
from django.db.models import get_model
from tagging.models import Tag
from sbblog.models import Entry

def do_latest_content(parser, token):
    bits = token.split_contents()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'get_latest_content' tag takes exactly four arguments")
    model_args = bits[1].split('.')
    if len(model_args) != 2:
        raise template.TemplateSyntaxError("First argument to 'get_latest_content' must be 'application name'.'model name' string")
    model = get_model(*model_args)
    if model is None:
        raise template.TemplateSyntaxError("'get_latest_content' tag got an invalid mode: %s" % bits[1])
    return LatestContentNode(model, bits[2], bits[4])

class LatestContentNode(template.Node):
    def __init__(self, model, num, varname):
        self.model = model
        self.num = int(num)
        self.varname = varname

    def render(self, context):
        context[self.varname] = self.model.live.all()[:self.num]
        return ''

def do_all_tags(parser, token):
    return BlogTags()

class BlogTags(template.Node):
    def render(self, context):
        context['all_tags_list'] = Tag.objects.all()
        tags = Tag.objects.usage_for_model(Entry, counts=True)
        tags.sort(key=operator.attrgetter('count'), reverse=True)
        context['top_tags_list'] = tags[:10]
        return ''

register = template.Library()
register.tag('get_latest_content', do_latest_content)
register.tag('get_all_tags', do_all_tags)
