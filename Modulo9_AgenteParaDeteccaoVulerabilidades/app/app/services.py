# app/services.py
import os
import base64
import json
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

def encode_image_to_base64(image_bytes: bytes) -> str:
    """Codifica os bytes de uma imagem para uma string base64."""
    return base64.b64encode(image_bytes).decode('utf-8')

def analyze_architecture_image(image_bytes: bytes) -> dict:
    """
    Analisa uma imagem de arquitetura usando o Azure OpenAI com capacidade de visão
    e retorna uma análise de ameaças STRIDE em formato JSON.
    """
    base64_image = encode_image_to_base64(image_bytes)

    # Inicializa o modelo.
    # IMPORTANTE: O deployment DEVE ser de um modelo com capacidade de visão (como gpt-4-vision-preview ou gpt-4o).
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0.1, # Baixa temperatura para respostas mais consistentes
    )
    
    # Prompt Engineering: A instrução para a IA.
    prompt = """
    Você é um especialista em cibersegurança e threat modeling. Sua tarefa é analisar a imagem de um diagrama de arquitetura de software fornecida.
    
    Siga estes passos:
    1.  Identifique os componentes principais da arquitetura (ex: frontend, backend, banco de dados, APIs externas, usuários, etc.).
    2.  Analise as interações entre esses componentes.
    3.  Com base na sua análise, realize um Threat Modeling completo usando a metodologia STRIDE.
    4.  Para cada categoria STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege), liste ao menos duas ameaças potenciais específicas para esta arquitetura.
    5.  Para cada ameaça, descreva-a brevemente e sugira uma possível mitigação.
    
    Retorne sua análise ESTRITAMENTE no seguinte formato JSON, sem nenhum texto ou formatação adicional antes ou depois:
    
    {
      "analysis": {
        "spoofing": [{"threat_description": "...", "mitigation_suggestion": "..."}],
        "tampering": [{"threat_description": "...", "mitigation_suggestion": "..."}],
        "repudiation": [{"threat_description": "...", "mitigation_suggestion": "..."}],
        "information_disclosure": [{"threat_description": "...", "mitigation_suggestion": "..."}],
        "denial_of_service": [{"threat_description": "...", "mitigation_suggestion": "..."}],
        "elevation_of_privilege": [{"threat_description": "...", "mitigation_suggestion": "..."}]
      }
    }
    """

    # Cria a mensagem com conteúdo misto (texto e imagem)
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image}"},
            },
        ]
    )
    
    # Invoca o modelo e obtém a resposta
    response = llm.invoke([message])
    
    try:
        # Tenta converter a string de resposta em um dicionário Python
        return json.loads(response.content)
    except json.JSONDecodeError:
        # Se a IA não retornar um JSON válido, levanta um erro
        raise ValueError("A resposta da IA não é um JSON válido.")