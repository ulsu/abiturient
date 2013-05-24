# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse
from models import *
from form.models import Faculty
from main.views import dev

@dev  
def faculty(request, p=1):
    if 'var' in request.COOKIES:
        var = True if int(request.COOKIES['var']) == 1 else False
    else:
        var = False
                
    t = loader.get_template("faculty.html")
    c = RequestContext(request, {
        'var':var,
        'faculty': Faculty.objects.all(),
        'spec': SpecPage.objects.all(),
        'page': p,
        })
    return HttpResponse(t.render(c))
    
@dev
def news(request):
    if 'var' in request.COOKIES:
        var = True if int(request.COOKIES['var']) == 1 else False
    else:
        var = False
    t = loader.get_template("news.html")
    c = RequestContext(request, { 
        'var':var,
        'news': NewsPage.objects.all(),
        })
    return HttpResponse(t.render(c))