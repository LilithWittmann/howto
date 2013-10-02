from django.http import HttpResponseServerError
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponsePermanentRedirect
from django.template import loader, Context
from django.template.response import TemplateResponse
from django.conf import settings
from django_mongokit import get_database
import random
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.views.decorators.http import require_http_methods
import json



@login_required
def create_view(request):
    db = get_database()
    return TemplateResponse(request, 'create_page.html')



def view(request, slug):
    db = get_database()
    page = db.pages.find_one({"slug": slug})
    if page is None:
        raise Http404


    return TemplateResponse(request, 'page.html', {'page': page})

@login_required
@require_http_methods(["POST"])
def create_page(request):
    if not request.is_ajax():
        return HttpResponse(status=400, content="Only ajax requests are accepted here")


    db = get_database()
    try:
        post_data = json.loads(request.body)
    except ValueError:
        resp = {'status': 'error', 'message': "Unable to parse json"}
        return HttpResponse(json.dumps(resp), content_type='application/json', status=400)

    post_data["slug"] = slugify(post_data["name"])
    db.pages.save(post_data)

    resp = {
        'status': 'ok',
        'message': 'Saved... Thanks!',
        'slug': post_data["slug"]
    }
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
@require_http_methods(["POST"])
def edit_page(request):
    if not request.is_ajax():
        return HttpResponse(status=400, content="Only ajax requests are accepted here")


    db = get_database()
    try:
        post_data = json.loads(request.body)
    except ValueError:
        resp = {'status': 'error', 'message': "Unable to parse json"}
        return HttpResponse(json.dumps(resp), content_type='application/json', status=400)

    post_data["id"]
    db.pages.save(post_data)

    resp = {
        'status': 'ok',
        'message': 'Saved... Thanks!',
        'slug': post_data["slug"]
    }
    return HttpResponse(json.dumps(resp), content_type='application/json')




@login_required
def view_tags(request, tag):
    db = get_database()
    pages = db.pages.find({"tags":  tag})
    return TemplateResponse(request, 'pages.html', {'pages': pages, "tag": tag})

