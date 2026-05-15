from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from assinatura.models import DocumentoAssinatura
from assinatura.services.assinatura_service import ServiceAssinatura


def listar_usuarios(request):
    try:
        ServiceAssinatura.listar_usuarios()
        return JsonResponse({"status": "recebido"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# def subir_documento(request, document_id):
#     document = get_object_or_404(DocumentoAssinatura, id=document_id)

#     try:
#         ServiceAssinatura.eniar_para_assinatura(document)
#         return JsonResponse({"status": "sent"})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)