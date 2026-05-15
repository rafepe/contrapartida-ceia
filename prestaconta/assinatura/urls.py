from django.urls import path
from . import views

urlpatterns = [
    path("config/listar_usuarios", views.listar_usuarios, name='lista_usuarios'),
    # path("send/<int:document_id>/", send_document),
    # path("webhook/zapsign/", zapsign_webhook),
]