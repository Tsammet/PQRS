from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('pqrs/', views.creacion_pqrs, name='pqrs'),
    path('historia/', views.historia, name='historia'),
    path('agendar/', views.agendar, name='agendar'),
    path('registro_piano/', views.nuevo_piano, name='registro_piano'),
    path('registro/', login_required(views.registro_cliente), name='registro'),
    path('crm/', login_required(views.crm), name='crm'),
    path('crm_id/<id>', login_required(views.fcrm_id), name='crm_id'),
    path('clientes/', login_required(views.cliente), name='cliente'),
    path('cliente_pqr/<id>', login_required(views.cliente_pqr), name='cliente_pqr'),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)