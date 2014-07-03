from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'home.views.slider', name='home'),
    url(r'^team/', 'staff.views.team_group', name='team'),
    url(r'^features/', 'features.views.features', name='features'),
    url(r'^contactos/', 'home.views.contactos', name='contactos'),
    url(r'^register', 'registers.views.register', name='register'),
    url(r'^login', 'registers.views.user_login', name='login'),
    url(r'^logout/', 'registers.views.user_logout', name='logout'),
    url(r'^error_login/', 'registers.views.login_error', name='login_error'),
    url(r'^access_denied/', 'registers.views.login_denied', name='login_denied'),
    url(r'^historia/', 'home.views.timeline', name='timeline'),
    url(r'^lista-indicadores/', 'indicators.views.indicators_list', name='list'),
    url(r'^detalle-indicador/(?P<indicator_id>\d+)/$', 'indicators.views.indicators_detail', name='detail'),
    url(r'^calculo-indicador/', 'indicators.views.indicator_calc', name='calc'),
    url(r'^recursos/boletines/', 'resources.views.bulletins', name='bulletins'),
    url(r'^recursos/enlaces-externos/', 'resources.views.links', name='links'),
    url(r'^list_denied', 'indicators.views.list_by_no_denied', name='list_denied'),
    url(r'^list/', 'indicators.views.list_desagregation', name='list_desagregation'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
