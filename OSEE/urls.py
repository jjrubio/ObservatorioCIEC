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
    url(r'^mailing_test/', 'registers.views.test', name='mailing_test'),
    url(r'^confirm/([0-9A-Za-z]{32})', 'registers.views.confirm', name='confirm'),
    url(r'^cambio-contrasenia', 'registers.views.form_reset', name='form_reset'),
    url(r'^reset-contrasenia', 'registers.views.reset_password', name='reset_password'),
    url(r'^envio_cambio_contrasenia/([0-9A-Za-z]{32})', 'registers.views.confirm_reset_password', name='confirm_reset_password'),
    url(r'^formulario/', 'registers.views.form_reset_password', name='form_reset_password'),
    url(r'^cambio-expirado/', 'registers.views.reset_password_expires', name='reset_password_expires'),
    url(r'^historia/', 'home.views.timeline', name='timeline'),
    url(r'^definicion-indicador/(?P<cat_id>\d+)/(?P<subcat_id>\d+)/(?P<ind_id>\d+)/$', 'indicators.views.indicator_def', name='def_mix'),
    url(r'^definicion-indicador/', 'indicators.views.indicator_def', name='def'),
    url(r'^calculo-indicador/(?P<cat_id>\d+)/(?P<subcat_id>\d+)/(?P<ind_id>\d+)/$', 'indicators.views.indicator_calc', name='calc_mix'),
    url(r'^calculo-indicador/', 'indicators.views.indicator_calc',name='calc'),
    url(r'^last-full-year/', 'indicators.views.get_last_full_year',name='last_full_year'),
    url(r'^comercio-exterior/', 'comercio.views.comercio_page',name='comercio_page'),
    url(r'^recursos/boletines/', 'resources.views.bulletins', name='bulletins'),
    url(r'^recursos/enlaces-externos/', 'resources.views.links', name='links'),
    url(r'^boletin/(?P<bulletin_id>\d+)/', 'resources.views.pdf_view', name='link_bulletin'),
    url(r'^list_denied/', 'indicators.views.list_by_no_denied', name='list_denied'),
    url(r'^list/', 'indicators.views.list_desagregation', name='list_desagregation'),
    url(r'^result/', 'indicators.views.calc_result', name='result'),
    url(r'^indicadorFiltro/', 'indicators.views.indicador_filtro', name='indicador_filtro'),
    url(r'^numero_consultas/', 'indicators.views.numero_consultas', name='num_consultas'),
    url(r'^total_consultas/', 'indicators.views.total_consultas', name='tot_consultas'),
    url(r'^cache/', 'indicators.views.cache_page', name='pcache'),
    url(r'^generar_cache/', 'indicators.views.generar_cache', name='gcache'),
    url(r'^subir_csv/', 'ENEMDU.views.insert_data_enemdu', name='insert_data_enemdu'),
    url(r'^acceso_denegado/', 'ENEMDU.views.access_denied', name='access_denied'),
    url(r'^error-extension/', 'ENEMDU.views.error_extension', name='error_extension'),
    url(r'^comercio/', 'comercio.views.comercio',name='comercio'),
    url(r'^subir_csv_comercio/', 'comercio.views.insert_data_comercio',name='insert_data_comercio'),
    url(r'^error-subida/', 'comercio.views.error_subida', name='error_subida'),
    url(r'^actualizar-datos/', 'comercio.views.actualizar_datos', name='actualizar_datos'),
    url(r'^data/', 'comercio.views.option', name='datos'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
