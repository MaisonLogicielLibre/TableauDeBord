# coding: utf-8

from __future__ import division

from django import template

from app.floorMap.models import Settings

register = template.Library()


@register.filter
def tax_tps(before_taxes):
    tax_pct = float(Settings.load().taxes_tps / 100)
    return round(before_taxes * tax_pct, 2)


@register.filter
def tax_tvq(before_taxes):
    tax_pct = float(Settings.load().taxes_tvq / 100)
    return round(before_taxes * tax_pct, 2)


@register.filter
def tax_both(before_taxes):
    return before_taxes + tax_tps(before_taxes) + tax_tvq(before_taxes)


@register.filter
def currency(value):
    return "{:.2f} $".format(value)


@register.filter
def total_due(rents):
    return sum(r.get_monthly_fee() for r in rents)


@register.filter
def grand_total_due(rents):
    return sum(tax_both(r.get_monthly_fee()) for r in rents)
