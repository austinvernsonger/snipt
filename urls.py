import os

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.static import serve
from snipts.api import (PublicSniptResource,
                        PublicUserResource, PrivateSniptResource,
                        PrivateFavoriteResource, PrivateUserProfileResource,
                        PrivateUserResource, PublicTagResource)
from snipts.views import search
from tastypie.api import Api
from views import (homepage, lexers, login_redirect,
                   tags, user_api_key)

public_api = Api(api_name='public')
public_api.register(PublicSniptResource())
public_api.register(PublicTagResource())
public_api.register(PublicUserResource())

private_api = Api(api_name='private')
private_api.register(PrivateSniptResource())
private_api.register(PrivateUserResource())
private_api.register(PrivateFavoriteResource())
private_api.register(PrivateUserProfileResource())

urlpatterns = []

if os.environ.get("DISABLE_SIGNUP") == "true":
    urlpatterns += [
        url(r'^register/?$', lambda x: HttpResponseRedirect('/404/')),
        url(r'^signup/?$', lambda x: HttpResponseRedirect('/404/')),
    ]
else:
    urlpatterns += [
        url(r'^signup/?$', lambda x: HttpResponseRedirect('/register/')),
    ]


urlpatterns += [
    url(r'^$', homepage),
    url(r'', include('registration.backends.simple.urls')),
    url(r'^login/?$', login, name='login'),
    url(r'^login-redirect/$', login_redirect),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    url(r'^500/$', TemplateView.as_view(template_name='500.html')),
    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt')),
    url(r'^tags/$', tags),
    url(r'^account/', include('accounts.urls')),
    url(r'^api/public/lexer/$', lexers),
    url(r'^api/private/key/$', user_api_key),
    url(r'^api/', include(public_api.urls)),
    url(r'^api/', include(private_api.urls)),
    url(r'^search/$', search),
    url(r'^', include('teams.urls')),
    url(r'^', include('snipts.urls')),
    url(r'^(?P<path>favicon\.ico)$', serve, {
        'document_root': os.path.join(os.path.dirname(__file__), 'static/img')
    }),
    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': os.path.join(os.path.dirname(__file__), 'media')
    })
]
