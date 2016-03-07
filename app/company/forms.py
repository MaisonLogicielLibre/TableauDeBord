# coding: utf-8

from django import forms
from django.db.models import Q
import django_filters
from app.company.models import Company, CompanyStatus, Presence
from app.founder.models import Founder
from app.mentor.models import Mentor
from app.home.models import Rent, Room, RoomType
from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, \
    Submit, Field, ButtonHolder, Hidden, Div
from django.utils.translation import ugettext_lazy as _


class CompanyFilter(django_filters.FilterSet):
    # http://django-filter.readthedocs.org/en/latest/usage.html
    class Meta:
        model = Company
        fields = {'companyStatus': ['exact'], 'name': ['icontains']}


class PresenceForm(forms.ModelForm):
    class Meta:
        model = Presence
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'type':'date', 'class':'datepicker'})
        }

    date = forms.DateField()


class CompanyStatusForm(forms.ModelForm):
    class Meta:
        model = CompanyStatus
        fields = ['status']

    status = forms.CharField(
        label=_('Name'),
        required=True,
    )
    status.widget.attrs.update({'placeholder': _(u'Name of the new status')})


class MiniCompanyStatusUpdateForm(forms.Form):
    comment = forms.CharField(
        label=_('Comment'),
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': _(u'Write here a comment about this group.'),
                'class': 'md-editor'
            }
        )
    )

    def __init__(self, status, *args, **kwargs):
        super(MiniCompanyStatusUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'content-wrapper'
        self.helper.form_method = 'post'

        self.status = status
        self.fields['comment'].initial = status.comment

        self.helper.layout = Layout(
            Field('comment'),
            StrictButton(_('Save'), type="submit")
        )

    def save(self):
        self.status.save()


class MiniCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'logo', 'video', 'url', 'facebook', 'googlePlus', 'linkedIn', 'twitter', 'description']

    name = forms.CharField(
        label=_('Name'),
        required=True,
    )
    name.widget.attrs.update({'placeholder': _(u'Name of the company')})

    logo = forms.ImageField(
        label=_('Logo'),
        required=False,
    )

    video = forms.URLField(
        label=_('Video'),
        required=False,
    )
    video.widget.attrs.update({'placeholder': _(u'https://urlvideo.com/')})

    url = forms.URLField(
        label=_('Web site'),
        required=False,
    )
    url.widget.attrs.update({'placeholder': _(u'https://example.com')})

    facebook = forms.URLField(
        label=_('Facebook'),
        required=False,
    )
    facebook.widget.attrs.update({'placeholder': _(u'https://www.facebook.com/lastname.firstname')})

    twitter = forms.URLField(
        label=_('Twitter'),
        required=False,
    )
    twitter.widget.attrs.update({'placeholder': _(u'https://twitter.com/username')})

    googlePlus = forms.URLField(
        label=_('Google+'),
        required=False,
    )
    googlePlus.widget.attrs.update({'placeholder': _(u'https://plus.google.com/id')})

    linkedIn = forms.URLField(
        label=_('linkedIn'),
        required=False,
    )
    linkedIn.widget.attrs.update({'placeholder': _(u'https://ca.linkedin.com/in/username')})

    description = forms.CharField(
        label=_('Description'),
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': _(u'Write here a brief summary of your business.'),
                'class': 'md-editor'
            }
        )
    )


class CompanyForm(MiniCompanyForm):
    class Meta:
        model = Company
        fields = ['name', 'companyStatus', 'incubated_on', 'endOfIncubation', 'logo', 'video', 'url', 'facebook',
                  'googlePlus', 'linkedIn', 'twitter', 'description', 'founders', 'mentors']

    companyStatus = forms.ModelChoiceField(
        label=_(u"Incubation phase"),
        queryset=CompanyStatus.objects.all(),
        required=True,
    )

    incubated_on = forms.DateField(
        label=_('Incubated on'),
        required=False,
        input_formats=('%Y-%m-%d',),
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'datepicker'
            }
        )
    )

    endOfIncubation = forms.DateField(
        label=_('Incubation end on'),
        required=False,
        input_formats=('%Y-%m-%d',),
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'datepicker'
            }
        )
    )

    founders = forms.ModelMultipleChoiceField(
        label=_(u"Founders"),
        queryset=Founder.objects.all(),
        required=False,
        widget=forms.SelectMultiple()
    )

    mentors = forms.ModelMultipleChoiceField(
        label=_(u"Mentors"),
        queryset=Mentor.objects.all(),
        required=False,
        widget=forms.SelectMultiple()
    )


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ['company', 'room', 'date_start', 'date_end']

    company = forms.ModelChoiceField(
        label=_(u"Company"),
        queryset=Company.objects.all().order_by('name'),
        required=True,
        initial=0,
    )

    room = forms.ModelChoiceField(
        label=_(u"Room code"),
        queryset=Room.objects.filter(type__is_rental=True).order_by('code'),
        required=True,
    )

    date_start = forms.DateField(
        label=_('Start date'),
        required=True,
        input_formats=('%Y-%m-%d',),
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'datepicker'
            }
        )
    )

    date_end = forms.DateField(
        label=_('End date'),
        required=True,
        input_formats=('%Y-%m-%d',),
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'datepicker'
            }
        )
    )

    def clean_date_end(self):
        date_start = self.cleaned_data['date_start']
        date_end = self.cleaned_data['date_end']

        if date_start > date_end:
            raise forms.ValidationError(_("End date cannot be before the start date!"), code='invalid')

        return date_end

    def clean(self):
        # Always check that key exists in cleaned_data before using it in clean() method.
        if ('room' and 'date_start' and 'date_end') not in self.cleaned_data:
            return self.cleaned_data

        lst_conflicting = []

        for rent in self.conflicts():
            lst_conflicting.append(rent.company.name)

        if lst_conflicting:
            str_conflicts = lst_conflicting[0]

            for name in lst_conflicting[1:-1]:
                str_conflicts = ", ".join([str_conflicts, name])

            if len(lst_conflicting) > 1:
                str_conflicts = " ".join([str_conflicts, str(_("and")), lst_conflicting[-1:][0]])

            raise forms.ValidationError({
                'room': [forms.ValidationError(
                    _("Room and date conflicts with existing rental(s) by: %(conflicting)s."),
                    code='invalid',
                    params={'conflicting': str_conflicts}
                )]
            })

        return self.cleaned_data

    def conflicts(self):
        conflicting_period = [self.cleaned_data['date_start'], self.cleaned_data['date_end']]

        results = Rent.objects.filter(
            room_id__exact=self.cleaned_data['room'].id
        ).filter(
            Q(date_start__range=conflicting_period) | Q(date_end__range=conflicting_period)
        )

        return results


class RentalFormUpdate(RentalForm):
    class Meta:
        model = Rent
        fields = ['id', 'company', 'room', 'date_start', 'date_end']

    id = forms.CharField(
        widget=forms.HiddenInput,
    )

    def conflicts(self):
        conflicting_period = [self.cleaned_data['date_start'], self.cleaned_data['date_end']]

        results = Rent.objects.filter(
            room_id__exact=self.cleaned_data['room'].id
        ).filter(
            Q(date_start__range=conflicting_period) | Q(date_end__range=conflicting_period)
        ).exclude(
            id=int(self.cleaned_data['id'])
        )

        return results