# src/agent.py
import os
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

def gerar_testes_unitarios(codigo_python: str) -> str:
    """
    Usa o LangChain e o Azure OpenAI para gerar testes unitários
    para um dado trecho de código Python.
    """
    # 1. Definição do Prompt Template
    # Este prompt é a instrução principal para a IA.
    # Ele define o papel da IA e as regras para a geração do código.
    template_string = """
    Você é um assistente de IA especialista em desenvolvimento de software e testes em Python.
    Sua tarefa é criar testes unitários usando a biblioteca pytest para o código Python fornecido.

    Regras para a geração dos testes:
    1.  O arquivo de teste deve começar com `import pytest`.
    2.  O nome de cada função de teste deve começar com `test_`.
    3.  Crie testes para casos de sucesso (o caminho feliz).
    4.  Crie testes para casos de falha e casos extremos (edge cases), como entradas inválidas, tipos de dados incorretos ou divisão por zero.
    5.  Para testes que esperam um erro, use `with pytest.raises(TipoDoErro):`.
    6.  Responda APENAS com o código Python puro, sem nenhuma explicação, introdução ou comentário adicional.

    Código Python para testar:
    ```python
    {code}
    ```
    """
    prompt_template = ChatPromptTemplate.from_template(template_string)

    # 2. Inicialização do Modelo
    # Carrega as configurações do Azure OpenAI a partir das variáveis de ambiente
    model = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )

    # 3. Criação da Chain
    # A "chain" conecta o prompt, o modelo e o parser de saída.
    chain = prompt_template | model | StrOutputParser()

    # 4. Execução da Chain
    # Passamos o código para o template e invocamos a chain
    testes_gerados = chain.invoke({"code": codigo_python})

    return testes_gerados