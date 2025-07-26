from django.urls import path
from . import views
from .views import upload_lote
from .views import UploadLoteAPIView

from .views import (
    dashboard,
    validar_item,
    login_view,
    logout_view,
    historico_validacoes,
    upload_lote,
    pagina_upload_lote, 
)


app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('validar/<int:item_id>/', views.validar_item, name='validar_item'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('historico/', views.historico_validacoes, name='historico'),
    path('upload-lote/', upload_lote, name='upload_lote'),
    path('api/upload-lote/', UploadLoteAPIView.as_view(), name='api_upload_lote'),
    path('relatorio/grupo/', views.relatorios_por_grupo, name='relatorio_grupo'),
    path('relatorio/usuario/', views.relatorios_por_usuario, name='relatorio_usuario'),
    path('relatorio/pdf/', views.gerar_pdf_validacoes, name='relatorio_pdf'),
]
