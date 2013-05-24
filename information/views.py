# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext, Template
from django.http import HttpResponse
from models import *
from main.views import dev
from django.views.decorators.csrf import csrf_exempt
from information.models import InfoList

@dev
def rules(request):
    if 'var' in request.COOKIES:
        var = True if int(request.COOKIES['var']) == 1 else False
    else:
        var = False
    t = loader.get_template("rules.html")
    c = RequestContext(request, 
        { 'var':var,
          'blocks': InfoList.objects.all(),
        })
    return HttpResponse(t.render(c))

@csrf_exempt    
@dev
def rules_ajax(request):
    if 'var' in request.COOKIES:
        var = True if int(request.COOKIES['var']) == 1 else False
    else:
        var = False
        
    ids = 0
        
    if request.method == 'POST':
        ids = request.POST['id']
    
    t = loader.get_template("ajax-info.html")
    c = RequestContext(request, 
        { 'var':var,
          'id': InfoList.objects.get(id=ids),
        })
    return HttpResponse(t.render(c))


@dev
def cost(request):
    if 'var' in request.COOKIES:
        var = True if int(request.COOKIES['var']) == 1 else False
    else:
        var = False
    t = loader.get_template("cost.html")
    section = SectionList.objects.get(id=4)
    c = RequestContext(request,
                       { 'var':var,
                         'blocks': InfoList.objects.get(section=section),
                         })
    return HttpResponse(t.render(c))


@dev
def ninfo(request):
    if 'var' in request.COOKIES:
        var = True if int(request.COOKIES['var']) == 1 else False
    else:
        var = False
    t = loader.get_template("now-info.html")
    c = RequestContext(request,
    { 'var':var,
      'blocks': InfoList.objects.all(),
    })
    return HttpResponse(t.render(c))    

@dev
def sinfo(request):
    if 'var' in request.COOKIES:
        var = True if int(request.COOKIES['var']) == 1 else False
    else:
        var = False
    t = loader.get_template("stat-info.html")
    c = RequestContext(request, 
    { 'var': var,
      'blocks': InfoList.objects.all(),  
    })
    return HttpResponse(t.render(c)) 