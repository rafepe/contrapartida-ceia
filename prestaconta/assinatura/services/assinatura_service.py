from .zapsign_client import ZapSignClient
from assinatura.models import DocumentoAssinatura

from .zapsign_client import ZapSignClient
#from declaracao.models import Declaracao  ## olhar isso aqui
from assinatura.models import DocumentoAssinatura

class ServiceAssinatura:

    @staticmethod
    def listar_usuarios():
        client=ZapSignClient()
        get_response=client.listar_usuarios()
        print(get_response)
 
    @staticmethod
    def subir_docx_local(path_file: str):
        client = ZapSignClient()

        response = client.subir_documento_docx_base64(path_file)

        print("Resposta ZapSign docx base64:")
        print(response)

        return response


    # ### copy/paste tem que resccrever
    # @staticmethod
    # def eniar_para_assinatura(signature_document: DocumentoAssinatura):
    #     client = ZapSignClient()

    #     # 1. Upload do documento
    #     upload_response = client.subir_documento(signature_document.file.path)
    #     document_id = upload_response.get("id")

    #     # 2. Criar signatário
    #     signer_response = client.criar_signatario(
    #         name=signature_document.signatario_nome,
    #         email=signature_document.signatario_email
    #     )
    #     signer_id = signer_response.get("id")

    #     # 3. Enviar para assinatura
    #     client.enviar_documento_asinatura(document_id, signer_id)

    #     # 4. Atualizar banco
    #     signature_document.zapsign_document_id = document_id
    #     signature_document.status = "enviado"
    #     signature_document.save()
    

# def enviar_para_assinatura(declaracao_id):
#     declaracao = Declaracao.objects.get(id=declaracao_id)

#     client = ZapSignClient()

#     response = client.create_document(
#         file_url=declaracao.pdf_url,
#         signer_email=declaracao.coordenadora_email
#     )

#     Assinatura.objects.create(
#         declaracao=declaracao,
#         zapsign_doc_id=response["id"],
#         status="enviado"
#     )   