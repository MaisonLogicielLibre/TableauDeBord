# coding: utf-8

from django.db import models
from datetime import datetime
import os
from django.utils import timezone
from embed_video.fields import EmbedVideoField
from django.utils.translation import ugettext_lazy as _
from app.founder.models import Founder
from app.mentor.models import Mentor
from django.core.urlresolvers import reverse


class CompanyStatus(models.Model):
    # Status of a company in the Centech (ex: emergence)
    class Meta:
        verbose_name = _('Company status')
        verbose_name_plural = _('Company status')

    status = models.CharField(
        max_length=50,
        verbose_name=_('Name')
    )
    comment = models.TextField(
        verbose_name=_('Comment'),
        blank=True
    )

    def __unicode__(self):
        return self.status


class Company(models.Model):
    class Meta:
        verbose_name_plural = _('Companies')

    PAYMENT_METHODS = (
        ('CHQ', 'Cheque'),
        ('PPA', 'PPA'),
    )

    # General information
    name = models.CharField(
        max_length=200,
        verbose_name=_('Name')
    )
    logo = models.ImageField(
        upload_to='logo',
        blank=True,
        verbose_name=_('Logo')
    )
    url = models.URLField(
        blank=True,
        verbose_name=_('URL')
    )
    video = EmbedVideoField(
        blank=True,
        verbose_name=_('Video')
    )
    description = models.TextField(
        blank=True,
        max_length=2000,
        verbose_name=_('Description')
    )
    companyStatus = models.ForeignKey(
        CompanyStatus,
        verbose_name=_('Status'),
        related_name="companies"
    )

    # List of founders
    founders = models.ManyToManyField(
        Founder,
        blank=True,
        verbose_name=_('Founders'),
        related_name="company"
    )

    # List of mentors
    mentors = models.ManyToManyField(
        Mentor,
        blank=True,
        verbose_name=_('Mentors'),
        related_name="company"
    )

    facebook = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('Facebook')
    )
    twitter = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('Twitter')
    )
    googlePlus = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('Google+')
    )
    linkedIn = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('linkedIn')
    )

    incubated_on = models.DateField(
        blank=True,
        null=True
    )
    endOfIncubation = models.DateField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=12,
        blank=True,
        verbose_name=_('Phone number')
    )

    person_in_charge = models.ForeignKey(
        'founder.Founder',
        blank=True,
        null=True,
        verbose_name=_('Person in charge'),
        related_name='in_charge_of'
    )

    payment_method = models.CharField(
        blank=True,
        max_length=3,
        choices=PAYMENT_METHODS,
        verbose_name=_('Payment method')
    )

    created = models.DateTimeField(blank=True)
    updated = models.DateTimeField(blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwarg):
        if not self.id:
            self.created = timezone.now()
        else:
            origin = Company.objects.get(id=self.id)
            if origin.logo != self.logo:
                self.logo.name = unicode(self.id) + \
                                 os.path.splitext(self.logo.name)[1]

        self.updated = timezone.now()
        super(Company, self).save(*args, **kwarg)

    def get_users(self):
        users = []

        founders = self.founders.all()
        for founder in founders:
            users.append(founder.user)

        mentors = self.mentors.all()
        for mentor in mentors:
            users.append(mentor.user)

        return users

    def get_last_irl(self):
        irls = self.KPIs.filter(type="IRL").order_by("-period_start")
        if irls:
            return irls[0]
        else:
            return None

    def get_last_trl(self):
        trls = self.KPIs.filter(type="TRL").order_by("-period_start")
        if trls:
            return trls[0]
        else:
            return None

    def get_last_experiment(self):
        experiments = self.experiments.order_by("-dateFinish")
        if experiments:
            return experiments[0]
        else:
            return None

    def get_percentage_incubation_time(self):
        if self.incubated_on and self.endOfIncubation:
            now = datetime.date(datetime.today())
            delta_days = (now - self.incubated_on).days
            time_of_incubation = (self.endOfIncubation-self.incubated_on).days
            delta_days = float(delta_days)
            percentage = int(round((delta_days/time_of_incubation)*100, 0))
            if percentage > 100:
                return 100
            else:
                return percentage
        else:
            return None

    def image_thumb(self):
        return '<img src="/media/%s" width="100" height="100" />' % self.logo
    image_thumb.allow_tags = True


class Presence(models.Model):
    # Presence of companies
    class Meta:
        verbose_name_plural = _('Presences')

    # List of company
    company = models.ManyToManyField(Company, verbose_name=_('Companies'))
    # Date of the meeting
    date = models.DateTimeField(verbose_name=_('Date'))

    def __unicode__(self):
        return str(self.date)

    def get_absolute_url(self):
        return reverse(
            'company:presence_list',
            args={self.company.all()[0].companyStatus.id}
        )
