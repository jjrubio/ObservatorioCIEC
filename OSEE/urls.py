from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^$', 'home.views.slider', name='home'),
    url(r'^inicio/', 'home.views.slider', name='home2'),
    url(r'^equipo-trabajo/', 'staff.views.team_group', name='team'),
    url(r'^caracteristicas/', 'features.views.features', name='features'),
    url(r'^contactos/', 'home.views.contactos', name='contactos'),
    url(r'^registro/', 'registers.views.register', name='register'),
    url(r'^iniciar-sesion/', 'registers.views.user_login', name='login'),
    url(r'^cerrar-sesion/', 'registers.views.user_logout', name='logout'),
    url(r'^error-sesion/', 'registers.views.login_error', name='login_error'),
    url(r'^acceso-denegado/', 'registers.views.login_denied', name='login_denied'),
    url(r'^historia/', 'home.views.timeline', name='timeline'),
    url(r'^definicion-indicador/(?P<cat_id>\d+)/(?P<subcat_id>\d+)/(?P<ind_id>\d+)/$', 'indicators.views.indicator_def', name='def_mix'),
    url(r'^definicion-indicador/', 'indicators.views.indicator_def', name='def'),
    url(r'^calculo-indicador/(?P<cat_id>\d+)/(?P<subcat_id>\d+)/(?P<ind_id>\d+)/$', 'indicators.views.indicator_calc', name='calc_mix'),
    url(r'^calculo-indicador/', 'indicators.views.indicator_calc',name='calc'),
    url(r'^recursos/boletines/', 'resources.views.bulletins', name='bulletins'),
    url(r'^recursos/enlaces-externos/', 'resources.views.links', name='links'),
    url(r'^boletin/(?P<bulletin_id>\d+)/', 'resources.views.pdf_view', name='link-bulletin'),
    url(r'^list_denied/', 'indicators.views.list_by_no_denied', name='list_denied'),
    url(r'^list/', 'indicators.views.list_desagregation', name='list_desagregation'),
    url(r'^test/', 'indicators.views.test', name='test'),
    url(r'^result/', 'indicators.views.calc_result', name='result'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
