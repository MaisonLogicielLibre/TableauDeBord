# coding: utf-8

from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve, reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views import generic

from app.floorMap.forms import RentalForm, RentalFormUpdate, RoomFormUpdate, \
    InvoiceFilter, SettingsFormUpdate
from app.floorMap.models import Room, Rent, Settings
from app.floorMap.static.py.invoice_export import export_to_excel


class FloorMapIndex(generic.ListView):
    # Floor Plan Page
    model = Room
    template_name = 'floorMap/floorMap.html'
    context_object_name = 'list_room_data'

    # You need to be connected, and you need to have access as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech() or\
                self.request.user.profile.isFounder() or\
                self.request.user.profile.isMentor() or\
                self.request.user.profile.isExecutive():
            return super(FloorMapIndex, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")


class RoomDetails(generic.DetailView):
    # View room details
    model = Room
    template_name = 'room/room_details.html'

    # You need to be connected, and you need to have access as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech() or \
                self.request.user.profile.isFounder() or \
                self.request.user.profile.isMentor() or \
                self.request.user.profile.isExecutive():
            return super(RoomDetails, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_context_data(self, **kwargs):
        context = super(RoomDetails, self).get_context_data(**kwargs)

        room = Room.objects.get(id=self.kwargs['pk'])

        context['room_label'] = room.static_label
        context['room_color'] = room.type.bg_color

        if room.is_rental():
            active_rental = room.get_active_rental()

            if self.request.user.profile.isCentech():
                rentals = room.rentals.all().order_by("-date_start")
            else:
                upcoming = room.get_upcoming_rentals().order_by("-date_start")
                if active_rental:
                    rentals = list(chain(upcoming, [active_rental]))
                else:
                    rentals = upcoming

            if active_rental:
                context['room_label'] = active_rental.company.name
            else:
                context['room_label'] = _(u'Available')
                context['room_color'] = room.type.alt_bg_color

            context['rentals'] = rentals
            context['active_rental'] = active_rental
        return context


class RoomUpdate(generic.UpdateView):
    # Update a room
    model = Room
    template_name = 'room/room_update.html'
    form_class = RoomFormUpdate

    # You need to be connected, and you need to have access as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(RoomUpdate, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _(u'The room has been saved.')
        )
        return reverse_lazy(
            'floorMap:room_details',
            kwargs={'pk': int(self.kwargs["pk"])}
        )


class RentalCreate(generic.CreateView):
    # Add a new rental
    model = Rent
    template_name = 'rental/rent_form.html'
    form_class = RentalForm

    # You need to be connected, and you need to have access
    # as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(RentalCreate, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_initial(self):
        initials = {
            'pricing': Settings.load().default_annual_rental_rate
        }

        if 'next' in self.request.GET:
            origin = resolve(self.request.GET['next'])
            if origin.url_name == 'room_details':
                initials.update({'room': int(origin.kwargs['pk'])})
            elif origin.url_name == 'detail':
                initials.update({'company': int(origin.kwargs['pk'])})

        return initials

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _(u'The rental has been saved.')
        )
        if 'next' in self.request.GET:
            return self.request.GET['next']
        else:
            return reverse_lazy('floorMap:index')


class RentalUpdate(generic.UpdateView):
    # Update the rental
    model = Rent
    template_name = 'rental/rent_form.html'
    form_class = RentalFormUpdate

    # You need to be connected, and you need to have access
    # as Centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(RentalUpdate, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _(u'The rental has been saved.')
        )
        if 'next' in self.request.GET:
            return self.request.GET['next']
        else:
            return reverse_lazy('floorMap:index')


class RentalDelete(generic.DeleteView):
    # Delete the rental
    model = Rent
    template_name = 'rental/rent_confirm_delete.html'

    # You need to be connected, and you need to have access
    # as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(RentalDelete, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_success_url(self, **kwargs):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _(u'The rental has been removed.')
        )
        if 'next' in self.request.GET:
            return self.request.GET['next']
        else:
            return reverse_lazy('floorMap:index')

    def get_context_data(self, **kwargs):
        context = super(RentalDelete, self).get_context_data(**kwargs)
        context['rental'] = kwargs['object']
        return context


class Invoicing(generic.TemplateView):
    template_name = 'rental/invoicing.html'

    # You need to have access as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(Invoicing, self).dispatch(*args, **kwargs)
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_context_data(self, **kwargs):
        context = super(Invoicing, self).get_context_data(**kwargs)

        invoice_filter = InvoiceFilter(
            self.request.GET,
            queryset=Rent.objects.order_by('company__name', 'room__code')
        )
        context['filter'] = invoice_filter

        if 'date' in self.request.GET:
            context['invoice_date'] = self.request.GET['date']

            # Exports data to Excel file
            temp_file = export_to_excel(
                invoice_filter,
                "Facturation_entreprises.xlsx"
            )
        return context


class SettingsUpdate(generic.UpdateView):
    # Update app settings
    model = Settings
    template_name = 'floorMap/settings_form.html'
    form_class = SettingsFormUpdate
    pk_url_kwarg = '1'

    # You need to have access as Centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(SettingsUpdate, self).dispatch(*args, **kwargs)
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_object(self, queryset=None):
        return Settings.load()

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _(u'The settings have been saved.')
        )
        return reverse_lazy('floorMap:index')
