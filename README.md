# 🏥 MedAnalytics | Gestão de Saúde <sup>1</sup> - Tech Challenge Fase 4 (FIAP)

> MedAnalytics | Gestão de Saúde¹ é um nome fictício utilizado para fins estritamente acadêmicos.

Este projeto é referente ao **Tech Challenge da 4ª fase da Pós-Tech FIAP (Data Analytics)**. O objetivo é fornecer uma ferramenta de suporte à decisão clínica, utilizando Machine Learning (ML) e o Streamlit para prever o risco de obesidade e insights para identificar padrões comportamentais em pacientes.

---

## 🎯 O Desafio

Este projeto visa entregar insumos para identificar de forma precoce aqueles pacientes que possuem tendência de obesidade para reduzir custos com doenças crônicas e melhorar a qualidade de vida dos mesmos através dos itens abaixo:

1.  **Visão Analítica:** Um dashboard para equipes médicas identificarem os principais perfis de risco na população atendida.
2.  **Visão Preditiva:** Uma interface clínica onde o médico insere os dados do paciente e recebe uma predição em tempo real com a probabilidade de risco.

---

## 🏗️ Arquitetura do Projeto

### Pipeline de Desenvolvimento
Todas as etapas do projeto foram disponibilizadas no arquivo `fiap_tech_challenge_fase_4.ipynb`, abrangendo:

* **ETL & Data Cleaning:** Tratamento de ruídos em variáveis categóricas e numéricas, além tradução completa dos labels para Português (PT-BR).
* **Feature Engineering:** Criação das features de **IMC** (Índice de Massa Corporal) e **Tendência de Obesidade** (Target binário).
* **Modelagem:** Testes comparativos entre os modelos Regressão Logística, XGBoost e Random Forest de Machine Learning (ML).
* **Seleção de Modelo:** O **Random Forest Classifier** foi o escolhido devido à sua superioridade no *Recall* e *F1-Score*, fundamentais para evitar falsos negativos na área da saúde.

---

## 📈 Performance do Modelo

O modelo **Random Forest Classifier** foi selecionado visando o foco na segurança do paciente e assertividade diagnóstica:

| Métrica | Valor | Importância para o Negócio |
| :--- | :--- | :--- |
| **Acurácia** | ~95% | Assertividade geral do sistema. |
| **Precision** | 94% | Minimiza falsos positivos (evita alarmes falsos). |
| **Recall (Sensibilidade)** | 96% | Garante que pacientes em risco real sejam identificados. |
| **F1-Score** | 95% | Equilíbrio ideal entre precisão e sensibilidade. |

---

## 📊 Insights de Negócio (Visão Dashboard)

Extraímos padrões fundamentais para a estratégia da equipe médica, como:
* **Preditor Genético:** O histórico familiar é a variável com maior ganho de informação.
* **Consumo de Lanches:** Correlação de **0.85** entre o consumo frequente de snacks e o aumento do IMC médio.
* **Hidratação vs. Tecnologia:** Pacientes com alto tempo de uso de tecnologia tendem a apresentar os menores índices de consumo de água.

---

### 🖥️ Streamlit
O modelo de predição com ML e os insights podem ser acessados através do link abaixo:

🏥 [MedAnalytics | Gestão de Saúde](https://medanalytics-fiaptechchallengefase4.streamlit.app/) 

---

## 📂 Estrutura do Repositório

```
├── data_raw/
│   ├── Obesity.csv                        # Base bruta original
│   └── dicionario_obesity_fiap.pdf        # Referência técnica das variáveis
├── data_processed/
│   └── df_base.csv                        # Base tratada após ETL
├── models/
│   └── modelo_final_random_forest.joblib  # Pipeline de ML pronto para produção
├── notebook/
│   └── fiap_tech_challenge_fase_4.ipynb   # Documentação do experimento (Notebook)
├── streamlit/
│   ├── pages/
│   │   └── Dashboard.py                   # Dashboard fo projeto / Visão Analítica (Streamlit)
│   └── Modelo.py                          # Interface de Predição Clínica (Streamlit)
├── requirements.txt                       # Dependências do ecossistema
└── README.md                              # Documentação do projeto
```

---

## 👨‍💻 Autor(a): 
  - [Geovane Ferreira](https://www.linkedin.com/in/geovanaferreira/)