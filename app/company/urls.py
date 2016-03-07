# coding: utf-8

from django.conf.urls import patterns, url
from app.company import views

urlpatterns = patterns(
    '',
    # List of all companies
    url(r'^$', views.CompanyIndex.as_view(), name='index'),
    # Detail of a company
    url(r'^(?P<pk>\d+)/$', views.CompanyView.as_view(), name='detail'),
    # Form for update the company
    url(r'^update/(?P<pk>\d+)$', views.CompanyUpdate.as_view(), name='update'),
    # Form for add a company
    url(r'^add/$', views.CompanyCreate.as_view(), name='create'),

    url(r'^filter$', views.filter, name='filter'),

    # System of status
    url(r'^status/add/$', views.CompanyStatusCreate.as_view(), name='status_create'),

    # System of presence
    url(r'^presence/$', views.PresenceList.as_view(), name='presence_list'),
    url(r'^presence/(?P<status>\d+)/$', views.PresenceList.as_view(), name='presence_list'),
    url(r'presence/add/$', views.PresenceAdd.as_view(), name='presence_add'),
    url(r'presence/update/(?P<pk>\d+)/$', views.PresenceUpdate.as_view(), name='presence_update'),
    url(r'presence/delete/(?P<pk>\d+)/$', views.PresenceDelete.as_view(), name='presence_delete'),

    # System of rental
    url(r'^rental/add$', views.RentalCreate.as_view(), name='rental_create'),
    url(r'^rental/add/(?P<pk>\d+)/$', views.RentalCreate.as_view(), name='rental_create'),
    url(r'^rental/update/(?P<pk>\d+)/$', views.RentalUpdate.as_view(), name='rental_update'),
    url(r'^rental/delete/(?P<pk>\d+)/$', views.RentalDelete.as_view(), name='rental_delete'),
)
