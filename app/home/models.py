# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import os
import datetime
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from embed_video.admin import AdminVideoMixin
from embed_video.fields import EmbedVideoField

#TODO delete foreign key
EDUCATION_CHOICES = (
    ('Doctorat', 'Doctorat'),
    ('Maitrise', 'Maitrise'),
    ('Baccalaureat', 'Baccalaureat'),
)


class Education(models.Model):
    # Education level
    class Meta:
        verbose_name_plural = _('Education')

    education = models.CharField(max_length=200, verbose_name=_('Education level'))

    def __unicode__(self):
        return self.education


class Expertise(models.Model):
    # Areas of expertise
    class Meta:
        verbose_name_plural = _('Expertise')

    expertise = models.CharField(max_length=200, verbose_name=_('Area of expertise'))

    def __unicode__(self):
        return self.expertise


class UserProfile(models.Model):
    # User, we can't extends auth_user without auxiliar conflits
    class Meta:
        ordering = ['user__last_name']

    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, related_name="profile", verbose_name=_('User'))
    userProfile_id = models.AutoField(primary_key=True, verbose_name=_('Identifiant'))

    # The additional attributes we wish to include.
    phone = models.CharField(max_length=10,verbose_name=_('Phone'),blank=True)
    website = models.URLField(blank=True,verbose_name=_('Web site'))
    picture = models.ImageField(upload_to='user_profile', blank=True,verbose_name=_('Picture'))

    facebook = models.URLField(blank=True, null=True, verbose_name=_('Facebook'))
    twitter = models.URLField(blank=True, null=True, verbose_name=_('Twitter'))
    googlePlus = models.URLField(blank=True, null=True, verbose_name=_('Google+'))
    linkedIn = models.URLField(blank=True, null=True, verbose_name=_('linkedIn'))

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwarg):
        if self.userProfile_id:
            origin = UserProfile.objects.get(userProfile_id=self.userProfile_id)
            if origin.picture != self.picture:
                self.picture.name = unicode(self.userProfile_id) + os.path.splitext(self.picture.name)[1]

        super(UserProfile, self).save(*args, **kwarg)

    def image_thumb(self):
        return '<img src="/media/%s" width="100" height="100" />' % (self.picture)
    image_thumb.allow_tags = True

    def isCentech(self):
        groups = self.user.groups.values()
        for group in groups:
            if group['name'] == 'Centech':
                return True
        return False

    def isExecutive(self):
        groups = self.user.groups.values()
        for group in groups:
            if group['name'] == 'Executive':
                return True
        return False

    def isFounder(self):
        from app.founder.models import Founder
        try:
            return Founder.objects.get(user = self.user)
        except:
            return False

    def isMentor(self):
        from app.mentor.models import Mentor
        try:
            return Mentor.objects.get(user = self.user)
        except:
            return False


class RoomType(models.Model):
    # Data
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.CharField(blank=True, max_length="100", verbose_name=_('Description'))
    is_rental = models.BooleanField(default=False, verbose_name=_('Is rental'))

    def __unicode__(self):
        return self.name


class Room(models.Model):
    # Data
    type = models.ForeignKey(RoomType, verbose_name=_('Type'))

    """
    CommaSeparatedIntegerField:
        Stores a string of integers separated by commas (e.g. "0,0,100,200")
        Therefore, max_length refers to the string length and not list capacity
        So to support the list [1,2,3,4] the lowest max_length would be 7 (no spaces allowed, brackets are excluded)

    Coordinates syntax:
        The system expects a list of integers to be interpreted as a list of points
        See HTML map tag for reference
    """
    coords = models.CommaSeparatedIntegerField(
        max_length=2000,
        verbose_name=_('Coordinates'),
        help_text=_("For a rectangle, please use the following format: <em>x1,y1,x2,y2</em>.<br>"
                    "For a polygon, please use the following format: <em>x1,y1,...,xn,yn</em>.")
    )

    code = models.CharField(blank=True, max_length=10, verbose_name=_('Code'))
    static_label = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Label'),
        help_text=_('<b>Warning:</b> Will be overwritten by rental owner, if any.')
    )

    text_coords = models.CommaSeparatedIntegerField(
        blank=True,
        null=True,
        max_length=50,
        verbose_name=_('Text area coordinates'),
        help_text=_("Area where the label should be displayed (defaults to room coordinates)<br>"
                    "Please use the following format: <em>x1,y1,x2,y2</em>. <b>Rectangle only!</b>")
    )

    def __unicode__(self):
        if self.code:
            return self.code
        else:
            return self.id

    def is_rental(self):
        return self.type.is_rental

    def get_owner_name(self):
        """
        get_owner_name():
        Returns:
            The company owner's name if the room type has the is_rental flag
            Otherwise returns boolean False
        """
        if self.is_rental():
            owner_result = self.rentals.filter(
                date_end__gte=datetime.date.today(),
                date_start__lte=datetime.date.today()
            ).first()

            if owner_result:
                return owner_result.company.name
            else:
                return False
        else:
            return False


class Rent(models.Model):
    # Identifiers
    room = models.ForeignKey(Room, verbose_name=_('Room'), related_name='rentals')
    company = models.ForeignKey('company.Company', verbose_name=_('Company'), related_name='rentals')

    # Data
    date_start = models.DateField(verbose_name=_('Start date'))
    date_end = models.DateField(verbose_name=_('End date'))








