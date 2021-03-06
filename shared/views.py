from django.http import HttpResponseServerError
from django.template import loader, Context
from django.template.response import TemplateResponse
from django.conf import settings
from django_mongokit import get_database
import random
from django.contrib.auth.decorators import login_required


def home(request):
    db = get_database()
    pages = db.pages.find()
    return TemplateResponse(request, 'home.html', {'pages': pages})


    return TemplateResponse(request, 'home.html')

def js_templates(request):
    return TemplateResponse(request, 'js_templates.html')
