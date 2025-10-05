# 📊 Dashboard de Análise de Viabilidade de Projetos

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.27%2B-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.1%2B-purple?style=for-the-badge&logo=pandas)](https://pandas.pydata.org/)

Uma aplicação web interativa construída para transformar a complexa análise financeira de projetos em uma ferramenta visual, intuitiva e data-driven, indo da análise determinística clássica até a simulação de risco probabilística com Monte Carlo.

## 🎯 O Problema Resolvido

Decidir se um novo projeto ou investimento vale a pena é uma das tarefas mais críticas em qualquer negócio. Tradicionalmente, isso envolve planilhas complexas e análises que são:
* **Estáticas:** Não exploram facilmente o impacto das incertezas.
* **Complexas:** Difíceis de interpretar por quem não é especialista em finanças.
* **Frágeis:** Baseadas em premissas "certas" em um mundo fundamentalmente incerto.

Esta ferramenta foi criada para democratizar a análise de viabilidade, permitindo que gestores e analistas não apenas calculem as métricas-chave, mas também entendam e visualizem o **risco** associado a cada projeto.

## ✨ Funcionalidades Principais

O dashboard é dividido em duas abas principais:

### 1. Análise Determinística
A visão clássica, porém interativa, da viabilidade de um projeto.
* **Cálculo das Métricas Essenciais:** VPL, TIR e Payback Simples.
* **Gráfico de Fluxo de Caixa:** Visualização instantânea do investimento e dos retornos anuais.
* **Análise de Sensibilidade:** Um slider interativo permite ver o impacto em tempo real no VPL e na TIR ao simular variações percentuais nos fluxos de caixa.

### 2. Simulação de Monte Carlo
A camada de Data Science que leva a análise a um novo patamar de sofisticação.
* **Modelagem de Incerteza:** Em vez de um único valor, o usuário insere cenários **pessimista, provável e otimista** para os fluxos de caixa de cada ano.
* **Simulação Massiva:** A aplicação roda 10.000 cenários diferentes, sorteando valores dentro das faixas definidas para criar uma visão completa das possibilidades.
* **Resultados Probabilísticos:** Responde a perguntas cruciais como:
    * Qual a **probabilidade** real do projeto ter lucro (VPL > 0)?
    * Qual o **VPL médio esperado**?
    * Qual o **intervalo de confiança** dos resultados?
* **Histograma de Frequência:** Um gráfico poderoso que mostra a distribuição de todos os VPLs possíveis, deixando claro o perfil de risco do investimento.

## 🧠 Desmistificando os Conceitos Financeiros

O coração deste projeto são as métricas financeiras. Aqui está uma explicação simples do que elas significam:

### **VPL (Valor Presente Líquido)**
* **A Ideia:** Dinheiro hoje vale mais do que dinheiro amanhã. O VPL traz todos os fluxos de caixa futuros esperados de um projeto para o seu valor "de hoje" e subtrai o investimento inicial.
* **Regra de Ouro:** Se `VPL > 0`, o projeto está gerando mais valor do que o mínimo que você esperava e é considerado viável.

### **TIR (Taxa Interna de Retorno)**
* **A Ideia:** Pense na TIR como a "taxa de juros" intrínseca do projeto. É a taxa de rentabilidade que ele gera por si só.
* **Regra de Ouro:** Se a `TIR > TMA` (sua Taxa Mínima de Atratividade, ou seja, seu custo de oportunidade), o projeto é atrativo, pois rende mais do que suas outras alternativas de investimento.

### **Simulação de Monte Carlo**
* **A Ideia:** Em vez de confiar em uma única previsão "perfeita", usamos o poder computacional para testar milhares de futuros possíveis. É como jogar um dado milhares de vezes para descobrir a probabilidade de cada resultado, em vez de tentar adivinhar o resultado de uma única jogada. Isso nos dá uma visão muito mais realista do risco.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Interface Web:** Streamlit
* **Manipulação de Dados:** Pandas
* **Cálculos Financeiros e Estatísticos:** NumPy, NumPy-Financial
* **Visualização de Dados:** Matplotlib

## 🚀 Como Executar o Projeto Localmente

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git)
    cd SEU-REPOSITORIO
    ```
2.  Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS / Linux
    source venv/bin/activate
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Execute a aplicação Streamlit:
    ```bash
    streamlit run app.py
    ```
5.  A aplicação abrirá automaticamente no seu navegador!
