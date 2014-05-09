from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from localflavor.us.models import USStateField, PhoneNumberField

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^localflavor\.us\.models\.USStateField"])
add_introspection_rules([], ["^localflavor\.us\.models\.PhoneNumberField"])

"""User Profile Elements"""
class JoatuLocation(models.Model):
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=200)
    street_address = models.CharField(max_length=250,)
    city = models.CharField(max_length=250,)
    state = USStateField()
    zipcode = models.CharField(max_length=5,)

    latitude = models.FloatField(blank=True, null=True, editable=False)
    longitude = models.FloatField(blank=True, null=True, editable=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('location_detail', kwargs={ 'slug': self.slug, })

    def save(self):
        self.slug = slugify(self.title)
        from geopy import geocoders
        google = geocoders.GoogleV3()
        address, (self.latitude, self.longitude) = google.geocode(' '.join([self.street_address, self.city, self.state, self.zipcode]))
        if address:
            self.street_address, self.city, state_zip, country = address.split(',')
            waste, self.state, self.zipcode = state_zip.split(' ')
        super(JoatuLocation, self).save()


class JoatuSkill(models.Model):
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=200)
    description = models.TextField()
    value = models.DecimalField(max_digits=6, decimal_places=2, editable=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('skill_detail', kwargs={ 'slug': self.slug, })

    def save(self):
        self.slug = slugify(self.title)
        super(JoatuSkill, self).save()


class JoatuUser(models.Model):
    user = models.ForeignKey(User)
    slug = models.SlugField(max_length=50, editable=False, unique=True)
    locations = models.ManyToManyField(JoatuLocation, blank=True)
    alternate_location = models.CharField(max_length=200, blank=True)
    skills = models.ManyToManyField(JoatuSkill, blank=True)

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={ 'slug': self.slug })

    def save(self):
        self.slug = slugify(self.user.username)
        return super(JoatuUser, self).save()


"""
try:
    from joatu.wp_models import *
except ImportError:
    pass
"""

