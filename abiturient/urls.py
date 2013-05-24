from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()
from form.views import *
from page.views import *
from information.views import *

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^faculty/$', faculty),
    url(r'^cost/', cost),
    url(r'^faculty/(?P<p>\d{1,})/$', faculty),
    url(r'^news/$', news),
    url(r'^mssql/$', test_mssql),
    url(r'^now/$', ninfo),
    url(r'^statistics/$', sinfo),
	url(r'^accounts/personal/$', main),
	url(r'^accounts/l/$', main),
	url(r'^data/$', get_data),
	url(r'^send/$', save_form),
	url(r'^g/$', generator),
	url(r'^', include('main.urls')),
)

urlpatterns += staticfiles_urlpatterns()