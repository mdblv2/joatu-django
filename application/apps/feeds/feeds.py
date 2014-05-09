from django.contrib.syndication.views import Feed as BaseFeed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.shortcuts import get_object_or_404

from apps.feeds.models import Post, Feed
import datetime
import audioread
import re


tags = re.compile('<.*?>')


class RssFeed(BaseFeed):
    
    def get_object(self, request, slug):
        return get_object_or_404(Feed, slug=slug)

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return obj.description

    def items(self, obj):
        return Post.live.filter(feed=obj)[:50]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.descriptoin


class AtomFeed(RssFeed):
    feed_type = Atom1Feed
    subtitle = RssFeed.description


class RssPodcastFeed(BaseFeed):

    def get_object(self, request, slug):
        return get_object_or_404(Feed, slug=slug)

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        import re
        tags = re.compile('<(.|\n)*?>')
        return tags.sub('', obj.description)
    
    def copyright(self, obj):
        return obj.copyright
 
    def items(self, obj):
        return Post.objects.filter(feed=obj)
   

class AtomPodcastFeed(RssPodcastFeed):
    feed_type = Atom1Feed
    subtitle = RssPodcastFeed.description


class iTunesPodcastsFeedGenerator(Rss201rev2Feed):

    def rss_attributes(self):
        return {u"version": self._version, u"xmlns:atom": u"http://www.w3.org/2005/Atom", u'xmlns:itunes': u'http://www.itunes.com/dtds/podcast-1.0.dtd'}

    def add_root_elements(self, handler):
        super(iTunesPodcastsFeedGenerator, self).add_root_elements(handler)
        handler.addQuickElement(u"title", self.feed["title"])
        handler.addQuickElement(u"link", self.feed["link"])
        handler.startElement(u"itunes:owner", {})
        handler.addQuickElement(u'itunes:name', self.feed['iTunes_name'])
        handler.addQuickElement(u'itunes:email', self.feed['iTunes_email'])
        handler.endElement(u'itunes:owner')
        handler.addQuickElement(u'itunes:subtitle', self.feed['subtitle'])
        handler.addQuickElement(u'itunes:author', self.feed['iTunes_name'])
        handler.addQuickElement(u'itunes:summary', self.feed['description'])
        handler.addQuickElement(u'itunes:image', attrs={'href':self.feed['iTunes_image_url']})
        handler.addQuickElement(u'itunes:explicit', self.feed['explicit'])
        handler.addQuickElement(u'itunes:block', self.feed['block'])
        handler.addQuickElement(u'itunes:complete', self.feed['complete'])

    def add_item_elements(self,  handler, item):
        super(iTunesPodcastsFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u'guid', item.id)
        handler.addQuickElement(u'enclosure', attrs={'url':item.enclosure.url, 'length':item.enclosure_length, 'type':item.enclosure_mime_type,})
        handler.addQuickElement(u'pubDate', item.pubdate)
        handler.addQuickElement(u'itunes:title', item.title)
        handler.addQuickElement(u'itunes:author', item.author)
        handler.addQuickElement(u'itunes:subtitle', item.subtitle)
        handler.addQuickElement(u'itunes:summary', item.summary)
        handler.addQuickElement(u'itunes:duration', item.duration)
        handler.addQuickElement(u'itunes:block', item.block)
        handler.addQuickElement(u'itunes:explicit', item.explicit)
        

class iTunesPodcastPost():
    def __init__(self, post):
        self.id = post.id
        self.title = post.title
        self.summary = post.summary
        self.subtitle = tags.sub('', post.description)
        self.author = ' '.join([author.get_full_name() for author in post.feed.authors.all()])
        self.enclosure_url = post.file.url
        self.enclosure_length = post.file.size
        self.enclosure_mime_type = mimetypes.guess_type(post.media.name)
        self.duration = post.duration
        self.explicit = 'yes' if post.explicit else 'no'
        self.block = 'yes' if post.block else 'no'
        self.pubdate = formatdate(time.mktime(post.pub_date.timetuple()))

    def __unicode__(self):
        return self.title
  
    def get_absolute_url(self):
        return self.enclosure_url


class iTunesPodcastsFeed(RssPodcastFeed):
    """
    A feed of podcasts for iTunes and other compatible podcatchers.
    """
    feed_type = iTunesPodcastsFeedGenerator
    feed_copyright = "Copyright 2013"
  
    def items(self, obj):
        """
        Returns a list of items to publish in this feed.
        """
        posts = super(iTunesPodcastsFeed, self).items(obj)
        posts = [iTunesPodcastPost(item) for item in posts]
        return posts

    def image_url(self, obj):
        if obj.logo:
            return obj.image.image.url
        else:
            return ''

    def feed_extra_kwargs(self, obj):
        extra = {}
        author_name = str([author.get_full_name()+' ' for author in obj.authors.all()])
        subtitle = obj.subtitle
        summary = obj.description
        extra['iTunes_name'] = str([author.get_full_name() + ' ' for author in obj.authors.all()])
        extra['iTunes_email'] = str([author.email + ' ' for author in obj.authors.all()])
        extra['iTunes_image_url'] = self.image_url(obj)
        extra['explicit'] = 'yes' if post.explicit else 'no'
        return extra
    
    """
    #def item_extra_kwargs(self, item):
    #    return {'summary':item.summary, 'duration':item.duration,}

    def item_enclosure_url(self, item):
        return item.enclosure_url
    
    def item_enclosure_length(self, item):
        return item.enclosure_length
    
    def item_enclosure_mime_type(self, item):
        return item.enclosure_mime_type

    def item_description(self, item):
        return item.summary
    """
