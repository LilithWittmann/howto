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
from bson.json_util import dumps
from bson import ObjectId


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

def edit_page_view(request, slug):
    db = get_database()
    page = db.pages.find_one({"slug": slug})
    if page is None:
        raise Http404

    page["json"] = dumps(page)


    return TemplateResponse(request, 'edit_page.html', {'page': page})

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

    if "items" not in post_data:
        resp = {"status": "error", "message": "need param 'items'"}
        return HttpResponse(json.dumps(resp), content_type='application/json', status=400)
    elif "tags" not in post_data:
        resp = {"status": "error", "message": "need param 'tags'"}
        return HttpResponse(json.dumps(resp), content_type='application/json', status=400)
    elif "name" not in post_data:
        resp = {"status": "error", "message": "need param 'name'"}
        return HttpResponse(json.dumps(resp), content_type='application/json', status=400)


    post_data["slug"] = slugify(post_data["name"])
    post_data["user"] = request.user.id
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


    if "id" not in post_data:
        resp = {"status": "error", "message": "need param id"}
        return HttpResponse(json.dumps(resp), content_type='application/json', status=400)

    page = db.pages.find_one({"_id": ObjectId(post_data["id"])})

    if page is None:
        resp = {"status": "error", "message": "howto not found"}
        return HttpResponse(json.dumps(resp), content_type='application/json', status=404)

    if "items" not in post_data:
        resp = {"status": "error", "message": "need param 'items'"}
        return HttpResponse(json.dumps(resp), content_type='application/json', status=400)
    elif "tags" not in post_data:
        resp = {"status": "error", "message": "need param 'tags'"}
        return HttpResponse(json.dumps(resp), content_type='application/json', status=400)
    elif "change_reason" not in post_data:
        resp = {"status": "error", "message": "need param 'change_reason'"}
        return HttpResponse(json.dumps(resp), content_type='application/json', status=400)


    page_revision = page
    page_revision["change_reason"] = post_data["change_reason"]
    page_revision["page_id"] = page_revision["_id"]
    del page_revision["_id"]
    db.pages.revisions.save(page)

    del page["change_reason"]
    page["items"] = post_data["items"]
    page["tags"] = post_data["tags"]
    page["name"] = post_data["name"]
    page["user"] = request.user.id
    page["_id"] = ObjectId(post_data["id"])

    db.pages.save(page)
    resp = {
        'status': 'ok',
        'message': 'Saved... Thanks!',
        'slug': page["slug"],
        "data": page
    }
    return HttpResponse(dumps(resp), content_type='application/json')




@login_required
def view_tags(request, tag):
    db = get_database()
    pages = db.pages.find({"tags":  tag})
    return TemplateResponse(request, 'pages.html', {'pages': pages, "tag": tag})

