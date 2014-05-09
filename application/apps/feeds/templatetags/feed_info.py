from django import template
from django.db.models import Count, Q
from django.template.loader import render_to_string

import datetime

#from apps.blogs.models import Post, Feed
#from apps.feeds.models import Episode

from apps.feeds.models import Feed, Post

register = template.Library()

@register.tag
def blog_header(parser, token):
    bits = token.contents.split()
    if len(bits) != 1:
        raise template.TemplateSyntaxError("%s tag takes no arguments" % bits[0])
    return FeedHeaderNode()

class FeedHeaderNode(template.Node):

    def render(self, context):
        featured_posts = Post.live.filter(featured=True).order_by('-pub_date')
        feeds = Feed.objects.filter(public=True).annotate(Count('post'))
        return render_to_string('feeds/feed_header.html', { 'posts': featured_posts, 'feeds': feeds })

@register.tag
def show_recent(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("%s tag takes 1 argument." % bits[0])
    return RecentPostsNode(bits[1])

class RecentPostsNode(template.Node):
    
    def __init__(self, recent_type):
        self.recent_type = recent_type

    def render(self, context):
        recent = []
        if self.recent_type == 'blogs':
            recent = Post.live.filter(Q(feed__is_audio_podcast=False)|Q(feed__is_video_podcast=False)).order_by('-pub_date')[:10]
        elif self.recent_type == 'podcasts':
            recent = Post.live.filter(Q(feed__is_audio_podcast=True)|Q(feed__is_video_podcast=True)).order_by('-pub_date')[:10]
        return render_to_string('recent_list.html', { 'list': recent })


