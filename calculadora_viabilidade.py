import numpy_financial as npf
import random  # ADICIONADO: Para gerar números aleatórios
import numpy as np  # ADICIONADO: Para análises estatísticas


# ... (funções calcular_vpl, calcular_payback_simples, calcular_tir permanecem as mesmas)
def calcular_vpl(tma: float, investimento_inicial: float, fluxos_de_caixa: list[float]) -> float:
    vpl = npf.npv(rate=tma, values=fluxos_de_caixa) + investimento_inicial
    return vpl


def calcular_payback_simples(investimento_inicial: float, fluxos_de_caixa: list[float]) -> str:
    investimento = abs(investimento_inicial)
    fluxo_acumulado = 0
    anos = 0
    for fluxo in fluxos_de_caixa:
        fluxo_acumulado += fluxo
        anos += 1
        if fluxo_acumulado >= investimento:
            meses_adicionais = (investimento - (fluxo_acumulado - fluxo)) / fluxo
            anos_completos = anos - 1
            meses = round(meses_adicionais * 12)
            return f"{anos_completos} anos e {meses} meses"
    return "Investimento não é recuperado no período do projeto."


def calcular_tir(investimento_inicial: float, fluxos_de_caixa: list[float]) -> float:
    fluxos_com_investimento = [investimento_inicial] + fluxos_de_caixa
    tir = npf.irr(fluxos_com_investimento)
    return tir


# ADICIONADO: A nova função de Simulação de Monte Carlo
def rodar_simulacao_monte_carlo(
        tma: float,
        investimento_inicial: float,
        cenarios_fluxos: list[tuple[float, float, float]],
        num_simulacoes: int = 10000
) -> list[float]:
    """
    Roda uma Simulação de Monte Carlo para calcular a distribuição de VPLs.

    Args:
        tma (float): A Taxa Mínima de Atratividade.
        investimento_inicial (float): O valor do investimento inicial (negativo).
        cenarios_fluxos (list[tuple]): Lista de tuplas, onde cada tupla contém o
                                       fluxo de caixa (pessimista, mais provável, otimista) para cada ano.
        num_simulacoes (int): O número de iterações a serem executadas.

    Returns:
        list[float]: Uma lista com todos os VPLs calculados em cada simulação.
    """
    resultados_vpl = []

    for _ in range(num_simulacoes):
        # Para cada simulação, geramos uma nova lista de fluxos de caixa
        fluxos_simulados = []
        for cenario in cenarios_fluxos:
            pessimista, provavel, otimista = cenario
            # Usamos a distribuição triangular para sortear um valor
            fluxo_sorteado = random.triangular(low=pessimista, high=otimista, mode=provavel)
            fluxos_simulados.append(fluxo_sorteado)

        # Calculamos o VPL para esta simulação específica
        vpl_simulado = calcular_vpl(tma, investimento_inicial, fluxos_simulados)
        resultados_vpl.append(vpl_simulado)

    return resultados_vpl


# --- Bloco de Teste ---
if __name__ == "__main__":
    # --- Teste da Calculadora Determinística (como antes) ---
    print("--- ANÁLISE DETERMINÍSTICA ---")
    taxa_minima_atratividade = 0.10
    investimento = -100000
    fluxos = [40000, 50000, 50000]
    # ... (o resto dos prints da análise determinística)

    # ADICIONADO: Teste para a Simulação de Monte Carlo
    print("\n" + "--- ANÁLISE PROBABILÍSTICA (MONTE CARLO) ---")

    # Cenários para cada ano: (Pessimista, Mais Provável, Otimista)
    cenarios = [
        (30000, 40000, 50000),  # Ano 1
        (40000, 50000, 65000),  # Ano 2
        (40000, 50000, 70000)  # Ano 3
    ]

    # Roda a simulação
    resultados_simulacao = rodar_simulacao_monte_carlo(
        tma=taxa_minima_atratividade,
        investimento_inicial=investimento,
        cenarios_fluxos=cenarios,
        num_simulacoes=10000
    )

    # Analisa os resultados
    vpl_medio = np.mean(resultados_simulacao)
    prob_vpl_positivo = np.sum(np.array(resultados_simulacao) > 0) / len(resultados_simulacao)

    print(f"Número de Simulações: {len(resultados_simulacao)}")
    print(f"VPL Médio Esperado: R$ {vpl_medio:,.2f}")
    print(f"Probabilidade de VPL ser positivo: {prob_vpl_positivo:.2%}")
    print(f"VPL (Pior Cenário - Percentil 5): R$ {np.percentile(resultados_simulacao, 5):,.2f}")
    print(f"VPL (Melhor Cenário - Percentil 95): R$ {np.percentile(resultados_simulacao, 95):,.2f}")
