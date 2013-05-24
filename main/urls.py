from django.conf.urls import *
from main.views import *
from information.views import *
from form.views import edit, add

urlpatterns = patterns('',
    url(r'^$', hello),
    url(r'^accounts/register/$', register),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^edit/(?P<user>\d{1,})/$', edit),
    url(r'^add/$', add),
    url(r'^print/(?P<ab>\d{1,})/$', xls),
    url(r'^rules/$', rules),
    url(r'^rules/ajax/$', rules_ajax),
    url(r'^speciality/$', my_speciality),
    url(r'^media/(?P<path>.*)$', mediaserver),
)