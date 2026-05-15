import requests
from django.conf import settings
import base64

class ZapSignClient:
    def __init__(self):
        self.base_url = settings.ZAPSIGN['BASE_URL']
        self.headers = {
            "Authorization": f"Bearer {settings.ZAPSIGN['API_TOKEN']}"
        }
    
    def listar_usuarios(self):
        url= f"{self.base_url}/users/"
        response = requests.get(url, headers=self.headers)
        return response.json()
   
    def _file_to_base64(self, path_file: str) -> str:
        with open(path_file, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")
   

    def subir_documento_docx_base64(self, path_file: str):
        url = f"{self.base_url}/docs/"

        base64_file = self._file_to_base64(path_file)

        payload = {
            "name": "Teste DOCX via Base64",
            "base64_docx": base64_file,
            "signers": [
                {
                    "name": "Teste Assinante",
                    "email": "testeassintante@email.com"
                }
            ],
            "lang": "pt-br"
        }

        response = requests.post(url, json=payload, headers=self.headers)

        if not response.ok:
            print("Erro ZapSign:", response.status_code, response.text)

        return response.json()

        response = requests.post(url, json=payload, headers=self.headers)

        if not response.ok:
            print("Erro ZapSign:", response.status_code, response.text)

        return response.json()

    # def subir_documento(self, file_path):
    #     url = f"{self.base_url}/docs/"

    #     with open(file_path, "rb") as f:
    #         files = {"file": f}
    #         response = requests.post(url, headers=self.headers, files=files)

    #     response.raise_for_status()
    #     return response.json()

    # def criar_signatario(self, name, email):
    #     url = f"{self.base_url}/signers/"

    #     payload = {
    #         "name": name,
    #         "email": email
    #     }

    #     response = requests.post(url, headers=self.headers, json=payload)
    #     response.raise_for_status()
    #     return response.json()

    # def enviar_documento_assinar(self, document_id, signer_id):
    #     url = f"{self.base_url}/docs/{document_id}/send/"

    #     payload = {
    #         "signers": [
    #             {"id": signer_id}
    #         ]
    #     }

    #     response = requests.post(url, headers=self.headers, json=payload)
    #     response.raise_for_status()
    #     return response.json()