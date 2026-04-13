import os
import requests
from dotenv import load_dotenv
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import TemplateView
from drf_spectacular.utils import extend_schema


load_dotenv()

class MedicineApiService:
    def __init__(self):
        self._base_url = 'https://medicines-api-innb.onrender.com'
        self._url_authentication = '/api/authentication/token/'
        self.username = os.getenv('API_USERNAME')
        self.password = os.getenv('API_PASSWORD')

    def get_valid_token(self):
        """Faz o login na conta fixa e retorna o token"""
        url = f'{self._base_url}{self._url_authentication}'
        payload = {"username": self.username, "password": self.password}
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get('access')
        return None
    

@extend_schema(
        summary="Lista todos os medicamentos",
        description="Busca a lista de medicamentos diretamente da API externa Medicines-API usando uma conta fixa.",
        responses={200},
        tags=['Medicamentos Externos']
    )
class GetMedicinesFixedView(APIView):
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        self._drug_endpoint = '/api/v1/drug/'

    def get(self, request):
        service = MedicineApiService()
        
        # 1. Obtém o token da conta fixa automaticamente
        token = service.get_valid_token()
        
        if not token:
            return Response(
                {"error": "Falha na autenticação com o provedor externo"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 2. Busca os dados usando o token obtido
        headers = {"Authorization": f"Bearer {token}"}
        try:
            external_response = requests.get(
                f"{service._base_url}{self._drug_endpoint}",
                headers=headers
            )
            
            if external_response.status_code == 200:
                raw_data = external_response.json()
                # Tratar os dados antes de entregar
                def treat_medical_data(raw_data):
                    if isinstance(raw_data, dict):
                        raw_data = [raw_data]

                    treated_list = []
                    
                    for item in raw_data:
                        # Extraindo listas aninhadas de forma limpa
                        forms = ", ".join([f.get('name') for f in item.get('pharmaceutical_form', [])])
                        routes = ", ".join([r.get('name') for r in item.get('routes_of_administration', [])])
                        manufacturers = ", ".join([m.get('name') for m in item.get('manufacturers', [])])

                        medical_profile = {
                            "identificacao": {
                                "nome_comercial": item.get('trade_name'),
                                "principio_ativo": item.get('active_ingredient'),
                                "concentracao": item.get('concentration'),
                                "apresentacao": item.get('presentation')
                            },
                            "clinica": {
                                "indicacoes": item.get('indications'),
                                "contraindicacoes": item.get('contraindications'),
                                "reacoes_adversas": item.get('adverse_reactions'),
                                "precaucoes": item.get('precautions_and_warnings')
                            },
                            "farmacologia": {
                                "formas_farmaceuticas": forms,
                                "vias_administracao": routes,
                                "tipo": "Referência" if item.get('type_of_medicine') == "REF" else "Genérico"
                            },
                            "seguranca": {
                                "prescricao_obrigatoria": item.get('medical_prescription'),
                                "alerta_doping": item.get('doping_alert'),
                                "cuidados_armazenamento": item.get('storage_care')
                            },
                            "rastreabilidade": {
                                "fabricante": manufacturers,
                                "lote": item.get('batch_number'),
                                "validade": item.get('validity')
                            }
                        }
                        treated_list.append(medical_profile)
    
                    return treated_list
                treated_data = treat_medical_data(raw_data)
                return Response(treated_data, status=status.HTTP_200_OK)
            
            return Response(external_response.json(), status=external_response.status_code)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class ExternalMedicineListView(TemplateView):
    template_name = 'medicine_list.html'
    paginate_by = 10

    def __init__(self, **kwargs):
        self._drug_endpoint = '/api/v1/drug/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Captura o que o usuário digitou na barra de busca (se houver)
        q = self.request.GET.get('q', '').strip().lower()
        
        service = MedicineApiService()
        token = service.get_valid_token()
        medicines = []
        api_error = None

        if token:
            headers = {"Authorization": f"Bearer {token}"}
            try:
                response = requests.get(f"{service._base_url}{self._drug_endpoint}", headers=headers)
                
                if response.status_code == 200:
                    raw_data = response.json()
                    # Passa a query de busca para o tratador de dados
                    medicines = self.treat_medical_data(raw_data, search_query=q)
                else:
                    api_error = "Não foi possível carregar os dados da API externa."
            except requests.exceptions.RequestException:
                api_error = "Erro de conexão com o servidor de medicamentos."
        else:
            api_error = "Falha na autenticação com o provedor externo."

        context['medicines'] = medicines
        context['api_error'] = api_error
        context['query'] = self.request.GET.get('q', '') # Devolve pro HTML manter na barra
        return context

    # Adiciona o parâmetro search_query na função
    def treat_medical_data(self, raw_data, search_query=''):
        if isinstance(raw_data, dict):
            raw_data = [raw_data]

        treated_list = []
        for item in raw_data:

            nome_comercial = str(item.get('trade_name', '')).lower()
            principio_ativo = str(item.get('active_ingredient', '')).lower()
            
            # Se o usuário pesquisou algo, e esse 'algo' não estiver nem no nome nem no princípio ativo, pula este item
            if search_query and (search_query not in nome_comercial and search_query not in principio_ativo):
                continue

            forms = ", ".join([f.get('name') for f in item.get('pharmaceutical_form', [])])
            routes = ", ".join([r.get('name') for r in item.get('routes_of_administration', [])])
            manufacturers = ", ".join([m.get('name') for m in item.get('manufacturers', [])])

            medical_profile = {
                "identificacao": {
                    "nome_comercial": item.get('trade_name'),
                    "principio_ativo": item.get('active_ingredient'),
                    "concentracao": item.get('concentration'),
                    "apresentacao": item.get('presentation')
                },
                "clinica": {
                    "indicacoes": item.get('indications'),
                    "contraindicacoes": item.get('contraindications'),
                    "reacoes_adversas": item.get('adverse_reactions'),
                    "precaucoes": item.get('precautions_and_warnings')
                },
                "farmacologia": {
                    "formas_farmaceuticas": forms,
                    "vias_administracao": routes,
                    "tipo": "Referência" if item.get('type_of_medicine') == "REF" else "Genérico"
                },
                "seguranca": {
                    "prescricao_obrigatoria": item.get('medical_prescription') == 'SIM',
                    "alerta_doping": item.get('doping_alert') =='SIM',
                    "cuidados_armazenamento": item.get('storage_care')
                },
                "rastreabilidade": {
                    "fabricante": manufacturers,
                    "lote": item.get('batch_number'),
                    "validade": item.get('validity')
                }
            }
            treated_list.append(medical_profile)
            
        return treated_list
