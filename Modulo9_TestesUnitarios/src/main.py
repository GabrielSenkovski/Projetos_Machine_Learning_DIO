# src/main.py
import os
import argparse
from dotenv import load_dotenv
from agent import gerar_testes_unitarios

def main():
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()

    # Configura o parser de argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Gera testes unitários para um arquivo Python.")
    parser.add_argument("filepath", type=str, help="O caminho para o arquivo Python a ser testado.")
    args = parser.parse_args()

    filepath = args.filepath

    # Verifica se o arquivo de entrada existe
    if not os.path.exists(filepath):
        print(f"Erro: O arquivo '{filepath}' não foi encontrado.")
        return

    print(f"Lendo o código do arquivo: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        codigo_python = f.read()

    print("Gerando testes unitários com a IA...")
    testes_gerados = gerar_testes_unitarios(codigo_python)

    # Define o nome do arquivo de saída
    diretorio, nome_arquivo = os.path.split(filepath)
    nome_arquivo_teste = f"test_{nome_arquivo}"
    caminho_saida = os.path.join(diretorio, nome_arquivo_teste)

    print(f"Salvando os testes em: {caminho_saida}")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(testes_gerados)

    print("Processo concluído com sucesso!")
    print(f"Para rodar os testes, use o comando: pytest {caminho_saida}")

if __name__ == "__main__":
    main()