import streamlit as st
import pandas as pd
import locale
import numpy as np
import matplotlib.pyplot as plt

# Importa as funções de cálculo do nosso outro arquivo
from calculadora_viabilidade import calcular_vpl, calcular_payback_simples, calcular_tir, rodar_simulacao_monte_carlo

# --- Configuração da Página e Funções Auxiliares ---
st.set_page_config(
    page_title="Análise de Viabilidade",
    page_icon="📊",
    layout="wide"
)

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')


def formatar_moeda(valor):
    return locale.currency(valor, grouping=True)


# --- Título Principal ---
st.title("📊 Análise de Viabilidade de Projetos")

# --- Criação das Abas ---
tab1, tab2 = st.tabs(["Análise Determinística", "Simulação de Monte Carlo"])

# --- Aba 1: Análise Determinística ---
with tab1:
    st.header("Análise de Ponto Fixo (Determinística)")

    # Coluna de inputs na lateral
    with st.sidebar:
        st.header("Parâmetros do Projeto")
        investimento_inicial = st.number_input(
            "Investimento Inicial (R$)", help="Insira o valor total do investimento. Deve ser um número negativo.",
            value=-100000.0, step=1000.0, format="%.2f", key="det_investimento"
        )
        tma = st.number_input(
            "Taxa Mínima de Atratividade (TMA) % a.a.", help="Insira a taxa de desconto anual (ex: 10 para 10%).",
            value=10.0, step=0.5, format="%.2f", key="det_tma"
        )
        fluxos_caixa_str = st.text_area(
            "Fluxos de Caixa Anuais (R$)", help="Insira os fluxos de caixa de cada ano, separados por vírgula.",
            value="40000, 50000, 50000", key="det_fluxos"
        )
        st.markdown("---")
        st.header("Análise de Sensibilidade")
        variacao_fluxos = st.slider(
            "Variação nos Fluxos de Caixa (%)", min_value=-30, max_value=30, value=0, step=5,
            help="Arraste para simular um aumento ou diminuição percentual em TODOS os fluxos de caixa anuais.",
            key="det_slider"
        )

    # Lógica da Aba 1
    try:
        fluxos_de_caixa = [float(f.strip()) for f in fluxos_caixa_str.split(',')]
        tma_decimal = tma / 100.0
        fator_variacao = 1 + (variacao_fluxos / 100.0)
        fluxos_ajustados = [fluxo * fator_variacao for fluxo in fluxos_de_caixa]

        vpl_calculado = calcular_vpl(tma_decimal, investimento_inicial, fluxos_ajustados)
        payback_calculado = calcular_payback_simples(investimento_inicial, fluxos_ajustados)
        tir_calculada = calcular_tir(investimento_inicial, fluxos_ajustados)

        st.subheader("Resultados da Análise")
        col1, col2, col3 = st.columns(3)
        col1.metric("VPL", formatar_moeda(vpl_calculado))
        col2.metric("Payback Simples", payback_calculado)
        col3.metric("TIR", f"{tir_calculada:.2%}")

        st.subheader("Visualização dos Fluxos de Caixa (Ajustado)")
        fluxos_grafico = [investimento_inicial] + fluxos_ajustados
        df_fluxos = pd.DataFrame({'Ano': range(len(fluxos_grafico)), 'Fluxo de Caixa': fluxos_grafico})
        st.bar_chart(df_fluxos.set_index('Ano'))
    except Exception as e:
        st.error(f"Ocorreu um erro na análise determinística. Verifique os dados. Detalhes: {e}")

# --- Aba 2: Simulação de Monte Carlo ---
with tab2:
    st.header("Análise de Risco com Simulação de Monte Carlo")

    col_params, col_cenarios = st.columns([1, 2])

    with col_params:
        st.subheader("Parâmetros Gerais")
        mc_investimento = st.number_input("Investimento Inicial (R$)", value=-100000.0, step=1000.0, format="%.2f",
                                          key="mc_investimento")
        mc_tma = st.number_input("TMA % a.a.", value=10.0, step=0.5, format="%.2f", key="mc_tma")
        mc_anos = st.number_input("Vida útil do projeto (anos)", min_value=1, max_value=20, value=3, step=1,
                                  key="mc_anos")
        num_simulacoes = st.number_input("Número de Simulações", min_value=1000, max_value=50000, value=10000,
                                         step=1000, key="mc_simulacoes")

    with col_cenarios:
        st.subheader("Cenários de Fluxo de Caixa Anual (R$ K)")
        cenarios_fluxos = []
        for i in range(mc_anos):
            cols = st.columns(3)
            pessimista = cols[0].number_input(f"Pessimista Ano {i + 1}", key=f"pess_{i}", value=30, step=5) * 1000
            provavel = cols[1].number_input(f"Provável Ano {i + 1}", key=f"prov_{i}", value=40, step=5) * 1000
            otimista = cols[2].number_input(f"Otimista Ano {i + 1}", key=f"otim_{i}", value=50, step=5) * 1000
            cenarios_fluxos.append((pessimista, provavel, otimista))

    if st.button("Rodar Simulação Monte Carlo"):
        with st.spinner("Rodando simulação... Isso pode levar alguns segundos."):
            resultados_simulacao = rodar_simulacao_monte_carlo(
                tma=mc_tma / 100.0,
                investimento_inicial=mc_investimento,
                cenarios_fluxos=cenarios_fluxos,
                num_simulacoes=num_simulacoes
            )

            # Análise dos resultados
            vpl_medio = np.mean(resultados_simulacao)
            prob_vpl_positivo = np.sum(np.array(resultados_simulacao) > 0) / len(resultados_simulacao)
            perc_5 = np.percentile(resultados_simulacao, 5)
            perc_95 = np.percentile(resultados_simulacao, 95)

            st.subheader("Resultados da Simulação")
            res_cols = st.columns(3)
            res_cols[0].metric("VPL Médio Esperado", formatar_moeda(vpl_medio))
            res_cols[1].metric("Probabilidade de Lucro (VPL>0)", f"{prob_vpl_positivo:.2%}")
            res_cols[2].metric("Número de Simulações", f"{num_simulacoes:,}".replace(",", "."))
            st.info(
                f"Intervalo de 90% de Confiança para o VPL: **{formatar_moeda(perc_5)}** a **{formatar_moeda(perc_95)}**")

            # Histograma
            fig, ax = plt.subplots()
            ax.hist(resultados_simulacao, bins=50, edgecolor='black', alpha=0.7)
            ax.set_title("Distribuição de Frequência dos VPLs Simulados")
            ax.set_xlabel("Valor Presente Líquido (VPL)")
            ax.set_ylabel("Frequência")
            ax.axvline(x=0, color='r', linestyle='--', label='VPL = 0 (Breakeven)')
            ax.legend()
            st.pyplot(fig)