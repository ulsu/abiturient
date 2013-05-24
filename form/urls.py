from django.conf.urls import patterns, include, url
from form.views import *
import main

urlpatterns = patterns('',
    # url(r'^$', show_form),
    url(r'^$', main),
    url(r'^edit/(?P<user>\d{1,})/$',edit),
    url(r'^print/(?P<id>\d{1,})/$', 'main.views.xls'),
    url(r'^data/$', get_data),
    url(r'^send/$', save_form),
    url(r'^add/$', add),
)