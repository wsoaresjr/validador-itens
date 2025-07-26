from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import models


from .models import Item, Validacao
from .forms import ValidacaoForm

# --------------------
# Autenticação
# --------------------

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('core:dashboard')
        else:
            return render(request, 'core/login.html', {'form': {}, 'error': True})

    return render(request, 'core/login.html', {'form': {}})


@login_required
def logout_view(request):
    logout(request)
    return redirect('core:login')


# --------------------
# Dashboard
# --------------------

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Item, Validacao

@login_required
def dashboard(request):
    usuario = request.user
    grupos_usuario = usuario.groups.all()

    # Itens do grupo do usuário
    itens_do_grupo = Item.objects.filter(grupo__in=grupos_usuario)

    # IDs de itens já validados por esse usuário
    validacoes_usuario = Validacao.objects.filter(usuario=usuario)
    itens_validados_ids = validacoes_usuario.values_list('item_id', flat=True)

    # Itens ainda não validados por esse usuário
    itens_nao_validados = itens_do_grupo.exclude(id__in=itens_validados_ids)

    # Itens rejeitados por esse usuário
    itens_rejeitados_ids = validacoes_usuario.filter(status='nao_validado').values_list('item_id', flat=True)
    itens_rejeitados = Item.objects.filter(id__in=itens_rejeitados_ids)

    return render(request, 'core/dashboard.html', {
        'itens_nao_validados': itens_nao_validados,
        'itens_rejeitados': itens_rejeitados,
    })



# --------------------
# Histórico do usuário
# --------------------

@login_required
def historico_validacoes(request):
    validacoes = Validacao.objects.filter(usuario=request.user).select_related('item').order_by('-data')
    return render(request, 'core/historico.html', {'validacoes': validacoes})


# --------------------
# Validação de item
# --------------------

@login_required
def validar_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    usuario = request.user

    # Verifica se o grupo do item está entre os grupos do usuário
    if item.grupo not in usuario.groups.all():
        return redirect('core:dashboard')

    # Tenta recuperar a validação existente
    validacao, _ = Validacao.objects.get_or_create(item=item, usuario=usuario)

    if request.method == 'POST':
        form = ValidacaoForm(request.POST, instance=validacao)
        if form.is_valid():
            form.save()
            return redirect('core:dashboard')
    else:
        form = ValidacaoForm(instance=validacao)

    return render(request, 'core/validar_item.html', {'item': item, 'form': form})


# --------------------
# Upload em lote (via HTML)
# --------------------

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .models import Item
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

@login_required
def upload_lote(request):
    print("Método:", request.method)
    print("Grupos disponíveis:", Group.objects.all())

    if request.method == 'POST':
        grupo_id = request.POST.get('grupo')
        arquivos = request.FILES.getlist('pdfs')

        if not grupo_id or not arquivos:
            return render(request, 'core/upload_lote.html', {
                'grupos': Group.objects.all(),
                'error': 'Grupo e arquivos são obrigatórios.'
            })

        grupo = Group.objects.get(id=grupo_id)

        for arquivo in arquivos:
            nome = arquivo.name.rsplit('.', 1)[0]
            caminho = default_storage.save(f'pdfs/{arquivo.name}', ContentFile(arquivo.read()))

            Item.objects.create(
                titulo=nome,
                pdf=caminho,
                grupo=grupo
            )

        return redirect('core:dashboard')

    return render(request, 'core/upload_lote.html', {
        'grupos': Group.objects.all()
    })



# --------------------
# Upload via API (POST /api/upload-lote/)
# --------------------

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UploadLoteAPIView(APIView):
    def post(self, request, *args, **kwargs):
        grupo_id = request.data.get('grupo')
        arquivos = request.FILES.getlist('arquivos')

        if not grupo_id or not arquivos:
            return Response({'erro': 'Grupo ou arquivos não fornecidos.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            grupo = Group.objects.get(id=grupo_id)
        except Group.DoesNotExist:
            return Response({'erro': 'Grupo não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        for arq in arquivos:
            Item.objects.create(
                titulo=arq.name,
                pdf=arq,
                grupo=grupo
            )

        return Response({'mensagem': 'Upload realizado com sucesso.'}, status=status.HTTP_201_CREATED)


# --------------------
# Página HTML para upload (caso queira usar rota dedicada)
# --------------------

@login_required
def pagina_upload_lote(request):
    grupos = Group.objects.all()
    return render(request, 'core/upload_lote.html', {'grupos': grupos})




from django.db.models import Q, Exists, OuterRef
from .models import Item, Validacao

@login_required
def lista_nao_validados(request):
    usuario = request.user

    # Subquery: verifica se o usuário atual já validou com status 'validado'
    validado_por_usuario = Validacao.objects.filter(
        item=OuterRef('pk'),
        usuario=usuario,
        status='validado'
    )

    # Retorna itens do grupo do usuário que:
    # (a) pertencem ao grupo dele
    # (b) ainda não foram validados por ele com status 'validado'
    itens = Item.objects.filter(
        grupo__in=request.user.groups.all()
    ).annotate(
        ja_validado=Exists(validado_por_usuario)
    ).filter(
        ja_validado=False
    )

    return render(request, 'core/lista_nao_validados.html', {'itens': itens})



# --------------------
# Relatorio por grupo
# --------------------

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.db.models import Count
from .models import Validacao, Item
from django.contrib.auth.models import Group

def is_admin(user):
    return user.groups.filter(name="administrador").exists()

@login_required
@user_passes_test(is_admin)
def relatorios_por_grupo(request):
    grupos = Group.objects.all()
    resultados = []

    for grupo in grupos:
        total_itens = Item.objects.filter(grupo=grupo).count()
        validacoes = Validacao.objects.filter(item__grupo=grupo)
        validados = validacoes.filter(status='validado').count()
        rejeitados = validacoes.filter(status='nao_validado').count()

        resultados.append({
            "grupo": grupo.name,
            "total_itens": total_itens,
            "validados": validados,
            "rejeitados": rejeitados,
        })

    return render(request, "core/relatorios_grupo.html", {"resultados": resultados})



# --------------------
# Relatorio por usuário
# --------------------

@login_required
@user_passes_test(is_admin)
def relatorios_por_usuario(request):
    validacoes = (
        Validacao.objects.values("usuario__username")
        .annotate(
            total=Count("id"),
            validados=Count("id", filter=models.Q(status="validado")),
            rejeitados=Count("id", filter=models.Q(status="nao_validado"))
        )
        .order_by("-total")
    )

    return render(request, "core/relatorios_usuario.html", {"relatorios": validacoes})


# --------------------
# Relatorio pdf
# --------------------
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
import os
from .models import Validacao

def is_admin(user):
    return user.groups.filter(name='administrador').exists()

@login_required
@user_passes_test(is_admin)
def gerar_pdf_validacoes(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="validacoes.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Logotipo
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        p.drawImage(ImageReader(logo_path), x=2*cm, y=height - 3*cm, width=3*cm, height=3*cm, mask='auto')

    # Título
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, height - 2.2 * cm, "Relatório de Validações de Itens")

    # Cabeçalhos
    p.setFont("Helvetica-Bold", 12)
    y = height - 4 * cm
    p.drawString(2 * cm, y, "Data")
    p.drawString(6 * cm, y, "Usuário")
    p.drawString(11 * cm, y, "Item")
    p.drawString(17 * cm, y, "Status")
    y -= 0.7 * cm

    # Dados
    p.setFont("Helvetica", 10)
    espacamento = 0.55 * cm
    validacoes = Validacao.objects.select_related('item', 'usuario').order_by('-data')

    for v in validacoes:
        p.drawString(2 * cm, y, v.data.strftime("%d/%m/%Y %H:%M"))
        p.drawString(6 * cm, y, v.usuario.username[:18])
        p.drawString(11 * cm, y, v.item.titulo[:25])
        p.drawString(17 * cm, y, v.get_status_display())

        y -= espacamento
        if y < 2 * cm:
            p.showPage()
            y = height - 3 * cm
            p.setFont("Helvetica-Bold", 12)
            p.drawString(2 * cm, y, "Data")
            p.drawString(6 * cm, y, "Usuário")
            p.drawString(11 * cm, y, "Item")
            p.drawString(17 * cm, y, "Status")
            y -= 0.7 * cm
            p.setFont("Helvetica", 10)

    p.save()
    return response
