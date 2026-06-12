from collections import defaultdict
from datetime import datetime, date
from decimal import Decimal

def format_br(value):
    if value is None:
        return "0,00"
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def gerar_meses_entre(inicio: date, fim: date) -> list[date]:
    meses = []
    ano, mes = inicio.year, inicio.month

    fim_ano, fim_mes = fim.year, fim.month
    if fim.day < 15:
        if fim_mes == 1:
            fim_mes = 12
            fim_ano -= 1
        else:
            fim_mes -= 1

    while (ano, mes) <= (fim_ano, fim_mes):
        meses.append(date(ano, mes, 1))

        if mes == 12:
            mes = 1
            ano += 1
        else:
            mes += 1

    return meses



def aplicar_filtro(queryset, request,filtros):
    for nome_filtro ,nome_model in filtros.items():
        valor = request.get(nome_filtro, "").strip()
        if valor:
            queryset = queryset.filter(**{f"{nome_model}__icontains": valor})
    return queryset

def aplicar_filtro_data(queryset, request,filtros):
    for nome_filtro,nome_model in filtros.items():
        valor = request.get(nome_filtro, "").strip()
        if valor:
            queryset = queryset.filter(**{f"{nome_model}": valor})
    return queryset


def tabela_calculo_contrapartidas(proj):
    # lazy import para evitar importação circular (models.py já importa utils.py)
    from .models import (
        contrapartida_so_projeto,
        contrapartida_pesquisa,
        contrapartida_rh,
        contrapartida_equipamento,
    )

    vlr_mensal_devido = (proj.contrapartida / proj.num_mes
                         if proj.num_mes else proj.contrapartida)

    contrapartidas_por_mes = defaultdict(lambda: {
        'so': Decimal(0),
        'rh': Decimal(0),
        'pesquisa': Decimal(0),
        'equipamento': Decimal(0),
        'prospeccao': Decimal(0),
        'total': Decimal(0),
        'diferenca': Decimal(0),
        'saldo': Decimal(0),
    })

    todos_meses = gerar_meses_entre(proj.data_inicio, proj.data_fim)
    for d in todos_meses:
        contrapartidas_por_mes[f"{d.year}-{d.month:02d}"]

    for so in contrapartida_so_projeto.objects.filter(id_projeto=proj):
        contrapartidas_por_mes[f"{so.ano}-{so.mes:02d}"]['so'] += Decimal(so.valor or 0)

    for c in contrapartida_pesquisa.objects.filter(id_projeto=proj):
        contrapartidas_por_mes[f"{c.id_salario.ano}-{c.id_salario.mes:02d}"]['pesquisa'] += c.valor_cp

    for c in contrapartida_rh.objects.filter(id_projeto=proj):
        contrapartidas_por_mes[f"{c.id_salario.ano}-{c.id_salario.mes:02d}"]['rh'] += c.valor_cp

    for ce in contrapartida_equipamento.objects.filter(id_projeto=proj):
        contrapartidas_por_mes[f"{ce.ano}-{ce.mes:02d}"]['equipamento'] += ce.valor_cp

    saldo = Decimal(0)
    contrapartidas_ordenadas = {}
    for key, valores in sorted(contrapartidas_por_mes.items()):
        valores['total'] = (valores['equipamento'] + valores['pesquisa']
                            + valores['so'] + valores['rh'])
        valores['diferenca'] = valores['total'] - Decimal(vlr_mensal_devido)
        saldo += valores['diferenca']
        valores['saldo'] = saldo
        contrapartidas_ordenadas[key] = valores

    return contrapartidas_ordenadas, vlr_mensal_devido


def contexto_filtros(params, campos):
    """
    Retorna apenas os filtros ativos definidos em `campos`.
    Ex:
        contexto_filtros(request.GET, ["nome", "ano", "mes"])
    """
    return {
        campo: params.get(campo, "").strip()
        for campo in campos
    }