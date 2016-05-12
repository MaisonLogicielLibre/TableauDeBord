# coding: utf-8

from django.conf.urls import patterns, url

from app.floorMap import views

urlpatterns = patterns(
    '',

    # Floor map page
    url(r'^$', views.FloorMapIndex.as_view(), name='index'),

    # Settings page
    url(r'^settings$', views.SettingsUpdate.as_view(), name='settings'),

    # Forms for room details

    url(
        r'^room/(?P<pk>\d+)/$',
        views.RoomDetails.as_view(),
        name='room_details'
    ),
    url(
        r'^room/update/(?P<pk>\d+)/',
        views.RoomUpdate.as_view(),
        name='room_update'
    ),

    # Forms for rentals

    url(
        r'^rental/add$',
        views.RentalCreate.as_view(),
        name='rental_create'
    ),
    url(
        r'^rental/add/(?P<pk>\d+)/$',
        views.RentalCreate.as_view(),
        name='rental_create'
    ),
    url(
        r'^rental/update/(?P<pk>\d+)/$',
        views.RentalUpdate.as_view(),
        name='rental_update'
    ),
    url(
        r'^rental/delete/(?P<pk>\d+)/$',
        views.RentalDelete.as_view(),
        name='rental_delete'
    ),

    # Forms for invoicing

    url(
        r'^invoicing$',
        views.Invoicing.as_view(),
        name='invoicing'
    ),
)
