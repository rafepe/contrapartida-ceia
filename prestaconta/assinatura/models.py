from django.db import models

class DocumentoAssinatura(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("signed", "Signed"),
        ("refused", "Refused"),
        ("error", "Error"),
    ]
    declaracao_id = models.ForeignKey("declaracao.declaracao_documento" ,on_delete=models.CASCADE)
    zapsign_doc_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    signatario_nome = models.CharField(max_length=255)
    signatario_email = models.EmailField()
    arquivo_assinado_url = models.URLField(null=True, blank=True)
    arquivo_assinado_local = models.FileField(upload_to="doumentos_assinados/", null=True, blank=True)
    data_geracao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)