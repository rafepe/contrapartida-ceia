import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from assinatura.models import DocumentoAssinatura


@csrf_exempt
def zapsign_webhook(request):
    payload = json.loads(request.body)

    document_id = payload.get("document_id")
    status = payload.get("status")

    try:
        doc = DocumentoAssinatura.objects.get(zapsign_document_id=document_id)

        if status == "signed":
            doc.status = "signed"
        elif status == "refused":
            doc.status = "refused"

        doc.save()

    except DocumentoAssinatura.DoesNotExist:
        pass

    return JsonResponse({"ok": True})