from django import template
from django.template.loader import render_to_string

import datetime

from apps.feeds.models import Post, Feed

register = template.Library()

@register.tag()
def feed_box(parser, token):
    bits = token.contents.split()
    if len(bits) > 3:
        raise template.TemplateSyntaxError("%s tag only takes up to two arguments" % bits[0])
    elif len(bits) < 2:
        raise template.TemplateSyntaxError("%s tag takes at least one argument" % bits[0])
    return FeedBoxNode(bits[1:])
 
class FeedBoxNode(template.Node):

    def __init__(self, args):
        self.feed_name = str(args[0])
        if len(args) == 2:
            self.post_count = int(args[1])

    def render(self, context):
        try:
            feed = Feed.objects.get(title__icontains=self.feed_name)
            if self.post_count:
                recent_posts = Post.live.filter(feed=feed).order_by('-pub_date')[:self.post_count]
            else:
                recent_posts = Post.live.filter(feed=feed).order_by('-pub_date')[:5]
                
            return render_to_string('tag_templates/feed_box.html', { 
                                    'feed': feed,
                                    'recent_posts': recent_posts,})
        except Feed.DoesNotExist:
            return str(self.feed_name) + ' ' + str(type(self.feed_name)) + '\n' + str(self.post_count) + ' ' + str(type(self.post_count))
 
