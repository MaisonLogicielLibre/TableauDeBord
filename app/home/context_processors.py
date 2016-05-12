# coding: utf-8

from django.conf import settings

from app.company.models import Company
from app.home.views import setCompanyInSession

"""
    A context processor with all APP settings.
"""


def app_settings(request):
    return {'app': settings.DASHBOARD_APP}


def company_select(request):
    """
    Make a list of company to insert in the main menu
    :param request:
    :return:
    """
    if request.user.is_active:
        # To know if the user is in the group "Centech"
        isCentech = request.user.profile.isCentech()

        # To know if the user is in the group "Centech"
        isExecutive = request.user.profile.isExecutive()

        # To know if the user is a mentor
        isMentor = request.user.profile.isMentor()

        # To know if the user is a founder
        isFounder = request.user.profile.isFounder()

        # For the list of company and menu
        list_company = []
        list_menu = []
        if isCentech:
            list_company = Company.objects.all().order_by('name')
            list_menu = [
                'companies',
                'floorMap',
                'invoicing',
                'mentors',
                'founders',
                'road_map',
                'summary',
                'presence'
            ]
        else:
            if isMentor:
                list_company += isMentor.company.all()
                list_menu += [
                    'companies',
                    'floorMap',
                    'mentors',
                    'founders',
                    'road_map'
                ]
            if isFounder:
                list_company += isFounder.company.all()
                list_menu += [
                    'companies',
                    'floorMap',
                    'mentors',
                    'founders',
                    'road_map'
                ]
            if isExecutive:
                list_menu = [
                    'companies',
                    'summary',
                    'mentors',
                    'founders',
                    'floorMap',
                ]

        # To set the default company selected
        if list_company:
            if 'companySelected' not in request.session.keys():
                setCompanyInSession(request, list_company[0].id)

    else:
        isCentech = False
        isExecutive = False
        isFounder = False
        isMentor = False
        list_company = ""
        list_menu = ""

    return {
        "isCentech": isCentech,
        "isExecutive": isExecutive,
        "isMentor": isMentor,
        "isFounder": isFounder,
        "list_company": list_company,
        "list_menu": list_menu
    }
