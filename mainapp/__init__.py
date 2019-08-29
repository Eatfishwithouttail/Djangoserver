import os

from django.template.defaultfilters import register


@register.filter('ellipse')
def ellispe(value):
    file_name = os.path.split(value)
    return file_name[-1]


