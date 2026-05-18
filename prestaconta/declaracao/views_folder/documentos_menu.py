from django.shortcuts import render
from declaracao.models import declaracao_documento
from django.contrib.auth.decorators import login_required

@login_required
def documentos_menu(request):
    ano = request.GET.get("ano")
    semestre = request.GET.get("semestre")

    # fallback para semestre atual
    from datetime import date
    today = date.today()

    if not ano:
        ano = today.year

    if not semestre:
        mes = today.month
        semestre = 1 if mes <= 6 else 2

    ano = int(ano)
    semestre = int(semestre)

    documentos = declaracao_documento.objects.filter(
        ano=ano,
        semestre=semestre
    ).order_by("-criado_em")

    context = {
        "documentos": documentos,
        "ano": ano,
        "semestre": semestre
    }

    return render(request, "declaracao/documentos_menu.html", context)