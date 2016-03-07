from django import template
from django.template.defaultfilters import stringfilter
from ast import literal_eval

register = template.Library()


@register.filter(name='coords_list')
@stringfilter
def coords_list(value):
    lst_int = literal_eval(value)
    lst_string = ",".join(str(i) for i in lst_int)
    return lst_string


@register.filter(name='shape')
@stringfilter
def shape(value):
    lst_int = literal_eval(value)
    if len(lst_int) == 4:
        return 'rect'
    else:
        return 'poly'
