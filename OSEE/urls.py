from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'home.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^historia/', 'home.views.timeline', name='timeline'),
    url(r'^lista-indicadores/', 'indicators.views.indicators_list', name='list'),
    url(r'^detalle-indicador/(?P<indicator_id>\d+)/$', 'indicators.views.indicators_detail', name='detail'),
    url(r'^calculo-indicador/', 'indicators.views.indicator_calc', name='calc'),
    url(r'^recursos/boletines/', 'resources.views.bulletins', name='bulletins'),
    url(r'^recursos/enlaces-externos/', 'resources.views.links', name='links'),
    url(r'^registro/', 'registers.views.signup', name='registro'),
    url(r'^UsuarioCreado/', 'registers.views.signupok', name='ok'),
    url(r'^list_denied', 'indicators.views.list_by_no_denied', name='list_denied'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
