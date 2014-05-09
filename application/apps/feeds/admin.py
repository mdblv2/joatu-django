from django.contrib import admin
from apps.feeds.models import Topic, Post, Feed
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE

class FeedAdmin(admin.ModelAdmin):

    #prepopulated_fields = {"slug": ("title",)}
    
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.has_perm('feeds.add_feed'):
            self.exclude.append('authors')
            self.exclude.append('public')
        return super(FeedAdmin, self).get_form(request, obj, **kwargs) 

    def queryset(self, request):
        qs = Feed.objects.all()
        if request.user.has_perm('feeds.add_feed'):
            return qs
        return qs.filter(authors=request.user)


class TopicAdmin(admin.ModelAdmin):
    #prepopulated_fields = {"slug": ("title",)}
    pass    

class PostAdmin(admin.ModelAdmin):
    
    #prepopulated_fields = {"slug": ("title",)}
    
    formfield_overrides = {
        HTMLField: {'widget': TinyMCE(
            attrs={'cols':50, 'rows':30},
            mce_attrs={'width':"655px"}
            )}
    }
    
    list_filter = ('status',)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.has_perm('feeds.add_feed'):
            self.exclude.append('on_front')
            self.exclude.append('featured')
        return super(PostAdmin, self).get_form(request, obj, **kwargs) 
    
    def queryset(self, request):
        qs = Post.objects.all()
        if request.user.has_perm('feeds.add_feed'):
            return qs
        return qs.filter(feed__authors=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'feed':
            qs = Feed.objects.all()
            if request.user.has_perm('feeds.add_feed'):
                kwargs['queryset'] = qs
            else:
                kwargs['queryset'] = qs.filter(authors=request.user)
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            LIVE_STATUS = 1
            SUBMITTED_STATUS = 2
            DRAFT_STATUS = 3
            if request.user.has_perm('feeds.add_post'):
                kwargs['choices'] = (
                        (LIVE_STATUS, 'Live'),
                        (DRAFT_STATUS, 'Draft'),)
            else:
                kwargs['choices'] = (
                        (SUBMITTED_STATUS, 'Submitted'),
                        (DRAFT_STATUS, 'Draft'),)
        return super(PostAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
                
admin.site.register(Feed, FeedAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)


