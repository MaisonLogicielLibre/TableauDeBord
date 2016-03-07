# coding: utf-8

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from app.home.models import UserProfile,Expertise
from app.founder.models import Founder

MENTOR_TYPE_CHOICES = (
    (u'1', 'Affaires'),
    (u'2', 'Technologiques'),
)

#Mentors
class Mentor(UserProfile):
    expertise = models.ManyToManyField(Expertise, verbose_name=_('Areas of expertise'), blank=True)
    about = models.CharField(max_length=2000,blank=True, verbose_name=_('About'))
    type = models.CharField(max_length=20, choices=MENTOR_TYPE_CHOICES, null=True, blank=True, verbose_name=_('Type'))
    url = models.URLField(blank=True, null=True, verbose_name=_('URL'))

    def __unicode__(self):
        return self.user.username

    def get_queryset(self):
        return Mentor.objects.all()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = timezone.now()
        self.updated = timezone.now()
        super(Mentor, self).save(*args, **kwargs)

    def get_type(self):
        if self.type:
                return 'Mentor ' + MENTOR_TYPE_CHOICES[int(self.type)-1][1]
        else:
                return 'Mentor'

    def image_thumb(self):
        return '<img src="/media/%s" width="100" height="100" />' % (self.picture)
    image_thumb.allow_tags = True