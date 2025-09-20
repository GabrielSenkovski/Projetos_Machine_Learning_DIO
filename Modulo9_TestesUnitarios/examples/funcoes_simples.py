# examples/funcoes_simples.py

def soma(a: int, b: int) -> int:
    """Retorna a soma de dois números inteiros."""
    return a + b

def divisao(a: float, b: float) -> float:
    """
    Retorna a divisão de a por b.
    Levanta um erro se b for zero.
    """
    if b == 0:
        raise ValueError("Não é possível dividir por zero.")
    return a / b

def is_par(numero: int) -> bool:
    """Verifica se um número é par."""
    return numero % 2 == 0