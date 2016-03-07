# coding: utf-8

from django.shortcuts import render_to_response, get_object_or_404
from app.company.models import Company, Presence, CompanyStatus
from app.founder.models import Founder
from app.home.models import Rent
from app.company.forms import CompanyFilter, CompanyStatusForm, CompanyForm, MiniCompanyForm,\
    RentalForm, RentalFormUpdate
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.core.management import call_command
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext as _
from app.home.views import setCompanyInSession
from datetime import date


def filter(request):
    f = CompanyFilter(request.GET, queryset=Company.objects.filter(name__icontains= request.GET['name']))
    return render_to_response('company/filter.html', {'filter': f})


class CompanyIndex(generic.ListView):
    # List all companies in the Centech
    template_name = 'company/index.html'
    context_object_name = 'company'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CompanyIndex, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Company.objects.all()

    def get_context_data(self, **kwargs):
        cf = CompanyFilter(self.request.GET, queryset=Company.objects.order_by('name'))
        context = super(CompanyIndex, self).get_context_data(**kwargs)
        context['filter'] = cf

        return context


class CompanyView(generic.DetailView):
    # Display detail of the company
    model = Company
    template_name = 'company/detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        setCompanyInSession(self.request, self.kwargs['pk'])
        return super(CompanyView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CompanyView, self).get_context_data(**kwargs)

        company = Company.objects.get(id=self.kwargs['pk'])
        founder = Founder.objects.filter(company=company)

        context['isFounderOfCompany'] = bool(founder)
        context['rentals'] = company.rentals.all().order_by("date_start")
        return context


class CompanyStatusCreate(generic.CreateView):
    model = CompanyStatus
    template_name = 'company/company_form.html'
    form_class = CompanyStatusForm

    # You need to be connected, and you need to have access as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(CompanyStatusCreate, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, _(u'This status has been added.'))
        return reverse_lazy("company:index")


class CompanyCreate(generic.CreateView):
    model = Company
    template_name = 'company/company_form.html'
    fields = ['name', 'companyStatus', 'logo', 'description']

    # You need to be connected, and you need to have access as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(CompanyCreate, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, _(u'This company has been added.'))
        return reverse_lazy("company:index")


class CompanyUpdate(generic.UpdateView):
    model = Company
    template_name = "company/company_form.html"

    # You need to be connected, and you need to have access as founder or centech
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        company = get_object_or_404(Company, id=self.kwargs["pk"])

        # Let the centech in first for allow modify a company of a founder who work in the Centech
        if self.request.user.profile.isCentech():
            self.form_class = CompanyForm
            return super(CompanyUpdate, self).dispatch(*args, **kwargs)

        if self.request.user.profile.isFounder():
            if company in self.request.user.profile.isFounder().company.all():
                self.form_class = MiniCompanyForm
                return super(CompanyUpdate, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_success_url(self):
        return reverse_lazy("company:detail", kwargs={'pk': int(self.kwargs["pk"])})


class PresenceList(generic.ListView):
    # Display all presence
    template_name = 'company/presence.html'
    context_object_name = 'presence'

    # You need to be connected, and you need to have access as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(PresenceList, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_queryset(self):
        return Presence.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PresenceList, self).get_context_data(**kwargs)

        try:
            status = CompanyStatus.objects.get(id=self.kwargs['status'])
        except Exception:
            status = CompanyStatus.objects.filter()
            if status.count():
                status = status[0]
            else:
                status = None

        if status:
            context['status_selected'] = status
            companies = Company.objects.filter(companyStatus=status)
            if companies.count():
                context['companies'] = companies
                all_presences = Presence.objects.all()
                presences = []
                for presence in all_presences:
                    for company in presence.company.all():
                        if company.companyStatus == status:
                            print company.name
                            print presence
                            print len(presences)
                            presences.append(presence)
                            break

                context['presence_list'] = presences

        list_company_status = []
        for status in CompanyStatus.objects.all():
            if status.companies.count():
                list_company_status.append(status)

        context['list_company_status'] = list_company_status

        return context


class PresenceAdd(generic.CreateView):
    # Add a new presence
    model = Presence
    fields = ['company', 'date']

    # You need to be connected, and you need to have access as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(PresenceAdd, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def form_valid(self, form):
        return super(PresenceAdd, self).form_valid(form)


class PresenceUpdate(generic.UpdateView):
    # Update the presence
    model = Presence
    fields = ['company','date']

    def get_url(self):
        return reverse_lazy('company:presence_list', self.object.get_absolute_url())

    # You need to be connected, and you need to have access as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(PresenceUpdate, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")


class PresenceDelete(generic.DeleteView):
    # Delete the presence
    model = Presence

    # You need to be connected, and you need to have access as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(PresenceDelete, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_success_url(self, **kwargs):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(PresenceDelete, self).get_context_data(**kwargs)
        context['presence'] = kwargs['object']
        context['status'] = kwargs['object'].company.all()[0].companyStatus.id
        return context


class RentalCreate(generic.CreateView):
    # Add a new rental
    model = Rent
    template_name = 'company/rent_form.html'
    form_class = RentalForm

    # You need to be connected, and you need to have access as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(RentalCreate, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_initial(self):
        if 'pk' in self.kwargs:
            return {'company': int(self.kwargs['pk'])}

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, _(u'The rental has been saved.'))
        return reverse_lazy("company:detail", kwargs={'pk': self.request.POST['company']})

    def form_valid(self, form):
        redirect_url = super(RentalCreate, self).form_valid(form)
        if self.object.date_start <= date.today() <= self.object.date_end:
            call_command('updatefloormap')
        return redirect_url


class RentalUpdate(generic.UpdateView):
    # Update the rental
    model = Rent
    template_name = 'company/rent_form.html'
    form_class = RentalFormUpdate

    # You need to be connected, and you need to have access as Centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(RentalUpdate, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, _(u'The rental has been saved.'))
        return reverse_lazy("company:detail", kwargs={'pk': self.request.POST['company']})

    def form_valid(self, form):
        redirect_url = super(RentalUpdate, self).form_valid(form)
        if self.object.date_start <= date.today() <= self.object.date_end:
            call_command('updatefloormap')
        return redirect_url


class RentalDelete(generic.DeleteView):
    # Delete the rental
    model = Rent

    # You need to be connected, and you need to have access as centech only
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.profile.isCentech():
            return super(RentalDelete, self).dispatch(*args, **kwargs)

        # The visitor can't see this page!
        return HttpResponseRedirect("/user/noAccessPermissions")

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, _(u'The rental has been removed.'))
        return reverse_lazy("company:detail", kwargs={'pk': self.object.company.id})

    def get_context_data(self, **kwargs):
        context = super(RentalDelete, self).get_context_data(**kwargs)
        context['rental'] = kwargs['object']
        return context

    def delete(self, request, *args, **kwargs):
        redirect_url = super(RentalDelete, self).delete(request, *args, **kwargs)
        if self.object.date_start <= date.today() <= self.object.date_end:
            call_command('updatefloormap')
        return redirect_url
