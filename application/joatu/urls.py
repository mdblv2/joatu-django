from django.conf.urls import patterns, include, url
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView

from joatu.models import JoatuUser
from joatu.views import JoatuUserCreateView
from apps.feeds.models import Post

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
 
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'joatu.views.home', name='home'),
    # url(r'^joatu/', include('joatu.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
 
    # Uncomment the next line to enable the admin:
    url(r'^$', ListView.as_view(
                    queryset=Post.live.filter(feed__title="Front Page"),
                    template_name='main.html')),
    #url(r'^feeds/', include('apps.feeds.urls')),
    
    
    url(r'^accounts/create/$', JoatuUserCreateView.as_view(), name='profile_create'),
    url(r'^accounts/edit/$', 'joatu.views.profile_edit', name='profile_edit'),
    url(r'^accounts/profile/$', 'joatu.views.profile_redirect', name='profile_redirect'),
    url(r'^accounts/profile/(?P<slug>[\d\w-]+)/$', DetailView.as_view(
                    queryset = JoatuUser.objects.filter(user__is_active=True)),
                    name='profile_detail'),

    url(r'^accounts/login/$', 
                    'django.contrib.auth.views.login',
                    {'template_name': 'password_form.html'},
                    name='profile_login'),
    url(r'^accounts/logout/$', 
                    'django.contrib.auth.views.logout', 
                    {'template_name': 'thanks.html'},
                    name='profile_logout'),
    
    
    url(r'^accounts/password/change/$', 
                    'django.contrib.auth.views.password_change', 
                    {'template_name': 'password_form.html'}, 
                    name='password_change'),
    url(r'^accounts/password/change/done/$', 
                    'django.contrib.auth.views.password_change_done', 
                    {'template_name': 'thanks.html'},
                    name='password_change_done'),


    url(r'^accounts/password/reset/$', 
                    'django.contrib.auth.views.password_reset',
                    {'template_name': 'password_form.html'},
                    name='password_reset'),
    url(r'^accounts/password/reset/confirm/(?P<uidb64>[\d\w]+)/(?P<token>[\d\w-]+)$', 
                    'django.contrib.auth.views.password_reset_confirm', 
                    {'template_name': 'password_form.html'},
                    name='password_reset_confirm'),
    url(r'^accounts/password/reset/complete/$', 
                    'django.contrib.auth.views.password_reset_done', 
                    {'template_name': 'password_complete.html'},
                    name='password_reset_complete'),
    url(r'^accounts/password/reset/done/$', 
                    'django.contrib.auth.views.password_reset_done', 
                    {'template_name': 'password_done.html'},
                    name='password_reset_done'),

    
    url(r'^thanks/$', TemplateView.as_view(template_name='thanks.html'), name='thanks'),
    
    
    url(r'^admin/', include(admin.site.urls)),


)
