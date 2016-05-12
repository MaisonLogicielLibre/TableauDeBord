# -*- coding:utf-8 -*-
from django.contrib import admin
from app.company.models import Company, CompanyStatus


class CompanyAdmin(admin.ModelAdmin):

    # Configuration of the list
    list_display = ('name', 'companyStatus')
    list_filter = ('name', 'founders')
    date_hierarchy = 'created'
    search_fields = ('name', 'founders')

    # Configuration of the edit form
    readonly_fields = ['image_thumb']
    fieldsets = (
        # Fieldset 1 : meta-info
        ('General', {
            'description': u'General informations:',
            'fields': ('name', 'logo', 'image_thumb'),

        }),

        # Fieldset 2 : promotion information
        ('Promotion', {
           'description': u'This information is the one present '
                          u'on the presentation page!',
           'fields': (
               'url',
               'video',
               'description',
               'phone',
           )
        }),

        # Fieldset 3 : centech
        ('Details', {
           'fields': (
               'companyStatus',
               'founders',
               'mentors',
               'created',
               'updated',
               'person_in_charge',
               'payment_method',
           )
        }),
    )

admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyStatus)
