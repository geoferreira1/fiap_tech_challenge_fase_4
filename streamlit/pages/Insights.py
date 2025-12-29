import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="MedAnalytics | Dashboard de Obesidade",
    page_icon="🏥",
    layout="wide"
)

# --- PALETA TERROSA (IDENTIDADE VISUAL) ---
cor_tan = "#D2B48C"     # Tan
cor_sienna = "#A0522D"  # Sienna
cor_peru = "#CD853F"    # Ocre quente
cor_sand = "#F4A460"    # Sandy Brown
paleta_terrosa = [cor_sienna, cor_peru, cor_tan, cor_sand, "#8B4513", "#BC8F8F"]

# Configurações de Estilo do Matplotlib
plt.rcParams.update({
    'axes.facecolor': 'white',
    'axes.edgecolor': 'black',
    'axes.titlecolor': 'black',
    'axes.labelcolor': 'black',
    'text.color': 'black',
    'xtick.color': 'black',
    'ytick.color': 'black',
    'figure.autolayout': True
})

# --- CARREGAMENTO DE DADOS (DIRETO DO GITHUB) ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/geoferreira1/fiap_tech_challenge_fase_4/main/data/df_base.csv"
    df = pd.read_csv(url)
    
    # Limpeza da Idade (Correção de escala)
    def limpar_idade(x):
        return int(str(x)[:2]) if x > 120 else x
    df['idade'] = df['idade'].apply(limpar_idade)
    
    # Mapeamentos para labels legíveis
    m_ob = {
        'abaixo_do_peso': 'Abaixo do Peso', 'dentro_do_peso': 'Peso Normal',
        'sobrepeso_um': 'Sobrepeso I', 'sobrepeso_dois': 'Sobrepeso II',
        'obesidade_um': 'Obesidade I', 'obesidade_dois': 'Obesidade II',
        'obesidade_tres': 'Obesidade III'
    }
    df['nivel_label'] = df['nivel_de_obesidade'].map(m_ob)
    df['genero_label'] = df['genero'].map({0: 'Masculino', 1: 'Feminino'})
    df['fuma_label'] = df['fuma'].map({0: 'Não Fumante', 1: 'Fumante'})
    df['calorico_label'] = df['consumo_alimentos_altamente_caloricos'].map({0: 'Baixo/Normal', 1: 'Consumo Frequente'})
    
    # Ordem clínica
    ordem = ['Abaixo do Peso', 'Peso Normal', 'Sobrepeso I', 'Sobrepeso II', 'Obesidade I', 'Obesidade II', 'Obesidade III']
    df['nivel_label'] = pd.Categorical(df['nivel_label'], categories=ordem, ordered=True)
    
    return df

df = load_data()

# --- SIDEBAR: CENTRO DE FILTROS AVANÇADO ---
st.sidebar.title("🔍 Filtros de Estudo")
st.sidebar.markdown("Refine a amostra para análise médica:")

with st.sidebar.expander("👤 Perfil do Paciente", expanded=True):
    idade_range = st.slider("Idade", int(df['idade'].min()), int(df['idade'].max()), (18, 55))
    gen_sel = st.multiselect("Gênero", options=df['genero_label'].unique(), default=df['genero_label'].unique())
    fuma_sel = st.multiselect("Hábito de Fumar", options=df['fuma_label'].unique(), default=df['fuma_label'].unique())

with st.sidebar.expander("🧬 Genética e Alimentação", expanded=True):
    hist_sel = st.selectbox("Histórico Familiar de Sobrepeso", ["Todos", "Sim", "Não"])
    cal_sel = st.multiselect("Consumo Alta Caloria", options=df['calorico_label'].unique(), default=df['calorico_label'].unique())

with st.sidebar.expander("🏃 Atividade e Rotina", expanded=False):
    ativ_sel = st.multiselect("Frequência Ativ. Física", options=df['frequencia_atividade_fisica'].unique(), default=df['frequencia_atividade_fisica'].unique())
    trans_sel = st.multiselect("Meio de Transporte", options=df['meio_de_transporte'].unique(), default=df['meio_de_transporte'].unique())

# Filtro de Níveis (Multiselect na Sidebar principal)
niveis_sel = st.sidebar.multiselect("Classificação de Obesidade", options=df['nivel_label'].unique().tolist(), default=df['nivel_label'].unique().tolist())

# Aplicando Filtros
df_f = df[
    (df['idade'].between(idade_range[0], idade_range[1])) &
    (df['genero_label'].isin(gen_sel)) &
    (df['fuma_label'].isin(fuma_sel)) &
    (df['calorico_label'].isin(cal_sel)) &
    (df['frequencia_atividade_fisica'].isin(ativ_sel)) &
    (df['meio_de_transporte'].isin(trans_sel)) &
    (df['nivel_label'].isin(niveis_sel))
]

if hist_sel == "Sim": df_f = df_f[df_f['historico_familiar'] == 1]
elif hist_sel == "Não": df_f = df_f[df_f['historico_familiar'] == 0]

# --- CABEÇALHO E MÉTRICAS ---
st.title("⚖️ MedAnalytics: Inteligência sobre Obesidade")
st.markdown("---")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Amostra Analisada", f"{len(df_f)} pacientes")
m2.metric("IMC Médio", f"{df_f['imc'].mean():.1f}")
m3.metric("Taxa de Obesidade (I+)", f"{(df_f['nivel_label'].str.contains('Obesidade').mean()*100):.1f}%")
m4.metric("Consumo Hídrico Baixo", f"{(df_f['consumo_agua'] == 'baixa').mean()*100:.1f}%")

# --- DASHBOARD DE INSIGHTS ---
tab1, tab2, tab3 = st.tabs(["📊 Distribuição Clínica", "🥗 Hábitos e Estilo de Vida", "🔬 Correlações Médicas"])

# ABA 1: DISTRIBUIÇÃO
with tab1:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Frequência por Categoria de Peso")
        fig, ax = plt.subplots()
        sns.countplot(data=df_f, x='nivel_label', palette=paleta_terrosa, ax=ax)
        plt.xticks(rotation=30)
        st.pyplot(fig)
    with c2:
        st.subheader("Peso do Histórico Familiar")
        fig, ax = plt.subplots()
        hist_counts = df_f['historico_familiar'].value_counts()
        plt.pie(hist_counts, labels=["Sim", "Não"], autopct='%1.1f%%', colors=[cor_sienna, cor_tan], startangle=90)
        st.pyplot(fig)
    st.info("**Insight Clínico:** Mais de 80% dos pacientes com Obesidade Tipo III possuem histórico familiar direto.")

# ABA 2: HÁBITOS
with tab2:
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Atividade Física vs Peso (kg)")
        fig, ax = plt.subplots()
        sns.boxplot(data=df_f, x='frequencia_atividade_fisica', y='peso', palette=paleta_terrosa, 
                    order=['sedentario', 'baixa', 'moderada', 'alta'], ax=ax)
        st.pyplot(fig)
    with c4:
        st.subheader("Impacto do Consumo Hídrico no IMC")
        fig, ax = plt.subplots()
        sns.violinplot(data=df_f, x='consumo_agua', y='imc', palette=paleta_terrosa, order=['baixa', 'moderada', 'alta'], ax=ax)
        st.pyplot(fig)
    
    st.subheader("Fracionamento de Refeições vs Severidade")
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.countplot(data=df_f, x='consumo_refeicoes_principais', hue='nivel_label', palette=paleta_terrosa, ax=ax)
    st.pyplot(fig)

# ABA 3: CORRELAÇÕES
with tab3:
    st.subheader("Dispersão: Idade, Peso e Nível de Risco")
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.scatterplot(data=df_f, x='idade', y='peso', hue='nivel_label', size='imc', 
                    palette='YlOrBr', sizes=(40, 400), alpha=0.7, ax=ax)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)
    
    st.markdown("""
    ### 📝 Conclusões Estratégicas para Médicos
    * **Padrão Etário:** O salto para Obesidade Tipo II ocorre predominantemente entre 25-35 anos.
    * **Risco Hídrico:** Baixo consumo de água está associado a variações extremas de IMC.
    * **Transporte:** Pacientes que utilizam transporte público apresentam maior tendência ao sobrepeso do que os que caminham, mas menor do que os que usam carro particular.
    """)

# --- RODAPÉ ---
st.markdown("---")
st.caption("Dashboard desenvolvido para suporte médico. Fonte: FIAP Tech Challenge Fase 4.")