# coding: utf-8

from django import forms
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from app.company.models import Company
from app.floorMap.models import Rent, Room, RoomType


class RoomFormUpdate(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['type', 'code', 'static_label', 'surface_size']

    type = forms.ModelChoiceField(
        label=_(u"Type"),
        queryset=RoomType.objects.all().order_by('name'),
        required=True,
        initial=0,
    )

    code = forms.CharField(
        label=_(u"Room code"),
        required=True,
    )

    static_label = forms.CharField(
        label=_(u"Static label"),
        required=False,
        help_text=_(u"Leave empty if room type is rental.")
    )

    surface_size = forms.IntegerField(
        label=_(u"Area size"),
        required=False,
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
        label=_(u"Start date"),
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
        label=_(u"End date"),
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
            raise forms.ValidationError(
                _(u"End date cannot be before the start date!"),
                code='invalid'
            )

        return date_end

    def clean(self):
        # Always check that key exists in cleaned_data
        # before using it in clean() method.
        if ('room' and 'date_start' and 'date_end') not in self.cleaned_data:
            return self.cleaned_data

        lst_room_conflicts = self.conflicts()

        if lst_room_conflicts:
            conflict_html_list = ""

            for rent in self.conflicts():
                conflict_html_list += mark_safe(
                    "<li>" + rent.company.name + "</li>"
                )

            raise forms.ValidationError({
                'room': [forms.ValidationError(
                    mark_safe(
                        u"{error_message} {lst_conflict_message} :<br>"
                        u"<ul>{lst_conflict}</ul>".format(
                            error_message=_(
                                u"Room not available at specified date."),
                            lst_conflict_message=_(u"Conflicts with"),
                            lst_conflict=conflict_html_list
                        )
                    ),
                    code='invalid'
                )]
            })

        return self.cleaned_data

    def conflicts(self):
        conflicting_period = [
            self.cleaned_data['date_start'],
            self.cleaned_data['date_end']
        ]

        results = Rent.objects.filter(
            room_id__exact=self.cleaned_data['room'].id
        ).filter(
            Q(
                date_start__range=conflicting_period
            ) | Q(
                date_end__range=conflicting_period
            )
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
        conflicting_period = [
            self.cleaned_data['date_start'],
            self.cleaned_data['date_end']
        ]

        results = Rent.objects.filter(
            room_id__exact=self.cleaned_data['room'].id
        ).filter(
            Q(
                date_start__range=conflicting_period
            ) | Q(
                date_end__range=conflicting_period
            )
        ).exclude(
            id=int(self.cleaned_data['id'])
        )

        return results
