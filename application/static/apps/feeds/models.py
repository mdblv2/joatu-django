import datetime
import os

from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from tinymce.models import HTMLField
from photologue.models import Gallery, Photo
from tagging.fields import TagField
from tagging.managers import ModelTagManager, ModelTaggedItemManager

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^tagging\.fields\.TagField"])
except ImportError:
    pass


def content_file_name(instance, filename):
    today = datetime.datetime.strftime(datetime.datetime.now(), '%Y/%m/%d')
    return '/'.join(['content', os.path.splitext(filename)[1][1:], today, filename])


class Feed(models.Model):
    
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text="Automatically comes from title. Must be unique.", blank=True, editable=False)
    description = HTMLField()
    image = models.ForeignKey(Photo, blank=True, null=True, on_delete=models.SET_NULL)
    authors = models.ManyToManyField(User)
    public = models.BooleanField()
    
    class Meta:
        ordering = ['title']

    def save(self):
        self.slug = slugify(self.title)
        super(Feed, self).save()

    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('feed_detail', (), {'slug': self.slug })

    def live_entry_set(self):
        from apps.feeds.models import Post
        return self.entry_set.filter(status=Post.LIVE_STATUS)


class Topic(models.Model):

    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text="Automatically comes from title. Must be unique.", blank=True, editable=False)
    description = HTMLField()
    image = models.ForeignKey(Photo, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['title']

    def save(self):
        self.slug = slugify(self.title)
        super(Topic, self).save()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('topic_detail', (), {'slug': self.slug })
    
    def live_entry_set(self):
        from apps.feeds.models import Post
        return self.entry_set.filter(status=Post.LIVE_STATUS)


class LivePostManager(models.Manager):
    def get_query_set(self):
        return super(LivePostManager,self).get_query_set().filter(status=self.model.LIVE_STATUS).filter(pub_date__lte=datetime.datetime.now())


class Post(models.Model):
    LIVE_STATUS = 1
    SUBMITTED_STATUS = 2
    DRAFT_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (SUBMITTED_STATUS, 'Submitted'),
        (DRAFT_STATUS, 'Draft'),)

    
    live = LivePostManager()
    objects = models.Manager()
    tags = ModelTagManager()
    tagged = ModelTaggedItemManager()

    feed = models.ForeignKey(Feed)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
    title = models.CharField(max_length=250)
    body = HTMLField()
    summary = models.CharField(max_length=250)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    posted = models.DateTimeField(default=datetime.datetime.now, editable=False)
    slug = models.SlugField(unique_for_date='pub_date', blank=True, editable=False)
    topics = models.ManyToManyField(Topic, blank=True)
    cover = models.ForeignKey(Photo, blank=True, null=True)
    gallery = models.ForeignKey(Gallery, blank=True, null=True, default=None)
    tags = TagField(help_text="Seperate with spaces. Put multi-word tags in quotes.", verbose_name='tags')

    class Meta:
        ordering = ['-pub_date']
        permissions = (('can_publish_entry', 'Can publish entry'), ('can_publish_front', 'Can post on front page'))
    
    def save(self):
        self.slug = slugify(self.title)
        if len(self.slug) > 50:
            self.slug = self.slug[:49]
        return super(Post, self).save()

    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', (), { 'feed': self.feed.slug,
                                        'year': self.pub_date.strftime("%Y"),
                                        'month': self.pub_date.strftime("%b").lower(),
                                        'day': self.pub_date.strftime("%d"),
                                        'slug': self.slug })

