from django.conf import settings
from django import template
from django_mongokit import get_database
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='taggify')
def taggify(value):
    return mark_safe(re.sub(r"#(?P<ht>([a-zA-Z0-9_])+)", r"<a href='/pages/tags/\g<ht>' target='_blank'>#\g<ht></a>", value))
taggify.mark_safe=True
