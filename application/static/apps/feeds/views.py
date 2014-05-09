from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, ArchiveIndexView
from django.db.models import Q

from endless_pagination.views import AjaxListView
from tagging.models import Tag

from apps.feeds.models import Topic, Post, Feed


class FrontPageView(AjaxListView):
    """Lists the front pages featured stories"""
    model = Post
    template_name = 'feeds/post_archive.html'
    page_template = 'feeds/post_archive_page.html'
    queryset = Post.live.filter(feed__title="Front Page").order_by('-pub_date')


class FeedListView(AjaxListView):
    """Filters out podcast feeds, to list blogs"""
    model = Feed
    template_name = 'feeds/feed_list.html'
    queryset = Feed.objects.filter(public=True)

    def get_context_data(self, **kwargs):
        context = super(FeedListView, self).get_context_data( **kwargs)
        context['item_type']= 'blog'
        return context


class PostListView(FrontPageView):
    """Lists most recent public posts on a given feed"""
    def get_queryset(self):
        return Post.live.filter(feed__slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data( **kwargs)
        context['slug']= get_object_or_404(Feed, slug=self.kwargs['slug'])
        return context


class PostDetailView(DetailView):
    """Displays a page for any given post"""
    date_filed = 'pub_date'
    template_name = 'feeds/post_detail.html'
    
    def get_queryset(self):
        return Post.live.filter(feed__slug=self.kwargs['feed'])


class ByTopicView(AjaxListView):
    """Displays all posts under a given topic"""
    model = Topic
    template_name = 'feeds/topic_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return Post.live.filter(categories__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ByTopicView, self).get_context_data( **kwargs)
        context['topic']= get_object_or_404(Topic, slug=self.kwargs['slug'])
        return context


class AllTopicView(AjaxListView):
    """Lists all topics"""
    model = Topic
    queryset = Topic.objects.all()
    template_name = 'feeds/categories.html'


class FeedTopArchiveView(AjaxListView):
    """Lists all years with posts"""
    model = Post
    template_name = 'feeds/post_archive_top.html'

    def get_queryset(self):
        return Post.live.datetimes('pub_date', 'year', order='DESC').filter(feed__slug=self.kwargs['slug'])
 

class FeedYearArchiveView(YearArchiveView):
    """Lists all months in a given year that contain posts"""
    date_field='pub_date'
    template_name = 'feeds/post_archive_year.html'

    def get_queryset(self):
        return Post.live.filter(feed__slug=self.kwargs['slug'])


class FeedMonthArchiveView(MonthArchiveView):
    """Lists all posts in a given month"""
    date_field='pub_date'
    template_name = 'feeds/post_archive_month.html'

    def get_queryset(self):
        return Post.live.filter(feed__slug=self.kwargs['slug'])

        
class TagDetailView(DetailView):
    """Lists all posts with given tag"""

    def get_queryset(self):
        return Post.live.filter(tag=Tag.objects.get(id=self.kwargs['id']))


class TagListView(AjaxListView):
    """Lists all tags"""
    queryset = Tag.objects.all()
    
    def get_context_data(self, **kwargs):
        alphabet = map(chr, range(65, 91))
        alphabet_tag_list = [[letter, Post.live.filter(name__istartswith=letter)] for letter in alphabet]
        alphabet_tag_list.append(['#', Post.live.filter(name__iregex=r'^[^[:alpha:]]')])
        context = super(ByTopicView, self).get_context_data( **kwargs)
        context['tag_list']= alphabet_tag_list
        return context

