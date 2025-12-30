import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="MedAnalytics | Gestão de Saúde",  # Título da aplicação
    page_icon="🏥",                               # Ícone temático de hospital
    layout="wide"                                 # Define que o conteúdo ocupará toda a largura da tela
)

# --- PALETA TERROSA (IDENTIDADE VISUAL) ---
cor_tan, cor_sienna, cor_peru, cor_sand = "#D2B48C", "#A0522D", "#CD853F", "#F4A460"
paleta_terrosa = [cor_sienna, cor_peru, cor_tan, cor_sand, "#8B4513", "#BC8F8F"]

# Aplica o estilo visual de grade branca do Seaborn em todos os gráficos
sns.set_theme(style="whitegrid")

# Atualiza os parâmetros globais do Matplotlib para fontes de eixos e ajuste automático de margens
plt.rcParams.update({'axes.labelsize': 12, 'axes.titlesize': 14, 'figure.autolayout': True})

# --- CARREGAMENTO E TRADUÇÃO DE DADOS (ETL) ---
@st.cache_data # Utiliza o cache do Streamlit para manter os dados na memória e acelerar o carregamento

# função de carregamento do dataset
def load_data():
    url = "https://raw.githubusercontent.com/geoferreira1/fiap_tech_challenge_fase_4/main/data_processed/df_base.csv"
    df = pd.read_csv(url)
    
    # Processa a coluna idade: converte para número e se o valor for impossível (>120), isola os dois primeiros dígitos
    df['idade'] = pd.to_numeric(df['idade'].apply(lambda x: str(x)[:2] if x > 120 else x), errors='coerce')
    
    # Elabora um dicionário para traduzir os termos originais para nomes amigáveis em português
    traducao_geral = {
        'baixa': 'Baixo', 'moderada': 'Moderado', 'alta': 'Alto', 'sempre': 'Sempre',
        'as_vezes': 'Às vezes', 'raramente': 'Raramente', 'nunca': 'Nunca',
        'sedentario': 'Sedentário', 'transporte_publico': 'Transporte Público',
        'caminhada': 'Caminhada', 'carro': 'Automóvel', 'moto': 'Motocicleta', 'bicicleta': 'Bicicleta',
        'tres_refeicoes_por_dia': '3 refeições', 'uma_refeicao_por_dia': '1 refeição',
        'duas_refeicoes_por_dia': '2 refeições', 'maior_que_tres_refeicoes_por_dia': 'Mais de 3'
    }
    
    # Relaciona as colunas do df que precisam passar pela tradução
    cols_para_traduzir = [
        'consumo_refeicoes_principais', 'consumo_vegetais', 'consumo_agua',
        'frequencia_atividade_fisica', 'tempo_uso_tecnologia', 
        'consumo_lanches_entre_refeicoes', 'consumo_alcool', 'meio_de_transporte'
    ]
    
    # Itera sobre cada coluna da lista e substitui os termos conforme o dicionário de tradução
    for col in cols_para_traduzir:
        df[col] = df[col].map(traducao_geral).fillna(df[col])

    # Cria o mapeamento para categorizar clinicamente os níveis de obesidade
    m_ob = {
        'insuficiencia_ponderal': 'Abaixo do Peso', 'dentro_do_peso': 'Peso Normal',
        'sobrepeso_um': 'Sobrepeso I', 'sobrepeso_dois': 'Sobrepeso II',
        'obesidade_um': 'Obesidade I', 'obesidade_dois': 'Obesidade II', 'obesidade_tres': 'Obesidade III'
    }
    
    # Gera a nova coluna 'categoria' baseada na tradução dos níveis de obesidade
    df['categoria'] = df['nivel_de_obesidade'].map(m_ob)
    # Traduz os indicadores de gênero 0 e 1 para Masculino e Feminino
    df['genero_label'] = df['genero'].map({0: 'Masculino', 1: 'Feminino'})
    # Cria uma flag booleana que detecta se o texto da categoria contém a palavra "obesidade"
    df['is_obese'] = df['nivel_de_obesidade'].str.contains('obesidade', case=False, na=False)
    
    # Entrega o DataFrame pronto para uso no dashboard
    return df

# Lê a função de carga e armazena os dados processados na variável df
df = load_data()

# --- SIDEBAR: CENTRO DE FILTROS ---
# Insere o cabeçalho principal na barra lateral
st.sidebar.title("🔍 Filtros de Análise")
st.sidebar.info('Expanda os menus abaixo para filtrar e visualizar as informações desejadas.')

# Declara uma função que obtém valores únicos de uma coluna para preencher os menus de seleção
def get_options(column):
    return ["Todos"] + sorted(list(df[column].unique().astype(str)))

# Cria uma seção expansível para agrupar dados pessoais do paciente na barra lateral
with st.sidebar.expander("👤 Perfil do Paciente", expanded=False):
    # Adiciona um controle deslizante para filtrar a faixa etária desejada
    idade_range = st.slider("Faixa Etária", int(df['idade'].min()), int(df['idade'].max()), (14, 61))
    # Adiciona caixas de seleção para filtrar gênero, fumo, transporte e histórico familiar
    gen_sel = st.selectbox("Gênero", ["Todos", "Masculino", "Feminino"])
    fuma_sel = st.selectbox("Fumante?", ["Todos", "Sim", "Não"])
    trans_sel = st.selectbox("Meio de Transporte", get_options('meio_de_transporte'))
    hist_sel = st.selectbox("Histórico Familiar de Sobrepeso", ["Todos", "Sim", "Não"])

# Cria uma seção expansível para filtrar hábitos alimentares e de hidratação
with st.sidebar.expander("🥗 Alimentação", expanded=False):
    # Insere menus para consumo calórico, monitoramento, refeições, vegetais, lanches, água e álcool
    cal_sel = st.selectbox("Consumo Alimentos Calóricos", ["Todos", "Sim", "Não"])
    monit_sel = st.selectbox("Monitoramento de Calorias", ["Todos", "Sim", "Não"])
    refeicoes_sel = st.selectbox("Refeições Principais/Dia", get_options('consumo_refeicoes_principais'))
    veg_sel = st.selectbox("Consumo de Vegetais", get_options('consumo_vegetais'))
    lanches_sel = st.selectbox("Lanches entre Refeições", get_options('consumo_lanches_entre_refeicoes'))
    agua_sel = st.selectbox("Consumo de Água", get_options('consumo_agua'))
    alc_sel = st.selectbox("Consumo de Álcool", get_options('consumo_alcool'))

# Cria uma seção expansível para filtrar atividades físicas e tecnologia
with st.sidebar.expander("🏃 Rotina e Hábitos", expanded=False):
    # Adiciona caixas de seleção para frequência de exercícios e uso de tecnologia
    ativ_sel = st.selectbox("Atividade Física", get_options('frequencia_atividade_fisica'))
    tec_sel = st.selectbox("Uso de Tecnologia", get_options('tempo_uso_tecnologia'))

# --- LÓGICA DE FILTRAGEM ---
# Inicia a filtragem restringindo os dados à faixa de idade selecionada
df_f = df[df['idade'].between(idade_range[0], idade_range[1])].copy()
# Aplica o filtro de gênero se a opção selecionada não for "Todos"
if gen_sel != "Todos": df_f = df_f[df_f['genero_label'] == gen_sel]
# Filtra fumantes convertendo a escolha textual em 0 ou 1 conforme a coluna original
if fuma_sel != "Todos": df_f = df_f[df_f['fuma'] == (1 if fuma_sel == "Sim" else 0)]
# Filtra por histórico familiar transformando Sim/Não nos valores binários da tabela
if hist_sel != "Todos": df_f = df_f[df_f['historico_familiar'] == (1 if hist_sel == "Sim" else 0)]
# Segmenta a base pelo consumo de alimentos calóricos se houver seleção específica
if cal_sel != "Todos": df_f = df_f[df_f['consumo_alimentos_altamente_caloricos'] == (1 if cal_sel == "Sim" else 0)]
# Segmenta por monitoramento de calorias conforme a escolha do usuário
if monit_sel != "Todos": df_f = df_f[df_f['monitoramento_calorias'] == (1 if monit_sel == "Sim" else 0)]

# Centraliza as variáveis categóricas em um dicionário para simplificar a filtragem em lote
filtros_cat = {
    'meio_de_transporte': trans_sel, 'consumo_refeicoes_principais': refeicoes_sel,
    'consumo_vegetais': veg_sel, 'consumo_lanches_entre_refeicoes': lanches_sel,
    'frequencia_atividade_fisica': ativ_sel, 'tempo_uso_tecnologia': tec_sel,
    'consumo_agua': agua_sel, 'consumo_alcool': alc_sel
}

# Percorre o dicionário e aplica cada filtro de texto ao DataFrame final
for col, val in filtros_cat.items():
    if val != "Todos": df_f = df_f[df_f[col] == val]

# --- DASHBOARD ---
# Exibe o título principal centralizado no topo do dashboard
st.caption("🏥 MedAnalytics | Gestão de Saúde <sup>1</sup>", unsafe_allow_html=True)
st.title("🏥 Painel Informativo")
st.markdown("""Acompanhamento de indicadores relacionados aos estilos de vidas coletados dos pacientes que passaram pela clínica.""")
st.markdown("---")

# Verifica se os filtros aplicados resultaram em uma tabela vazia
if df_f.empty:
    # Mostra mensagem de erro amigável se não houver dados para exibir
    st.error("Nenhum dado encontrado para os filtros selecionados.")
else:
    # Cria quatro colunas para exibir os números de destaque (Big Numbers)
    c1, c2, c3, c4 = st.columns(4)
    # Exibe a contagem total de pacientes filtrados
    c1.metric("Pacientes Analisados", f"{len(df_f)}")
    # Calcula e exibe o IMC médio do grupo
    c2.metric("Média de IMC", f"{df_f['imc'].mean():.1f} kg/m²")
    # Calcula e exibe a porcentagem de pacientes com obesidade no grupo
    c3.metric("Taxa de Obesidade", f"{(df_f['is_obese'].mean()*100):.1f}%")
    # Calcula e exibe a média de idade da amostra
    c4.metric("Idade Média", f"{df_f['idade'].mean():.0f} anos")

    # Define a estrutura de abas para organizar os diferentes tipos de análise
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Perfil Clínico", "🥗 Comportamento", "❗️ Fatores de Risco", "🔬 Análises de IMC"])

    # --- ABA 1: PERFIL CLÍNICO ---
    with tab1:
        # Divide a aba em duas colunas de tamanho igual
        col1, col2 = st.columns(2)
        with col1:
            # Título do gráfico de categorias clínicas
            st.subheader("Categoria Clínica vs Quantidade de Pacientes")
            # Cria a figura e o eixo do gráfico
            fig, ax = plt.subplots()
            # Conta a frequência de cada categoria clínica no grupo filtrado
            contagem = df_f['categoria'].value_counts()
            # Desenha barras horizontais com a paleta de cores terrosas definida
            sns.countplot(data=df_f, y='categoria', palette=paleta_terrosa, order=contagem.index, ax=ax)
            # Adiciona os números (rótulos) ao final de cada barra para facilitar a leitura
            for container in ax.containers: ax.bar_label(container, padding=5)
            # Define o nome dos eixos X e Y e desativa as linhas de grade
            ax.set_xlabel("Quantidade de Pacientes"); ax.set_ylabel("Categoria Clínica"); ax.grid(False)
            # Remove as molduras externas do gráfico e renderiza na tela
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)

        with col2:
            # Título da análise de prevalência por gênero
            st.subheader("Obesidade por Gênero (%)")
            # Agrupa os dados por gênero e calcula o percentual de pacientes obesos
            df_prev = df_f.groupby('genero_label')['is_obese'].mean() * 100
            # Formata a tabela resultante para ser usada no gráfico
            df_prev = df_prev.reset_index().rename(columns={'genero_label': 'Gênero', 'is_obese': 'Prevalência (%)'})
            # Inicializa a figura para a análise de gênero
            fig, ax = plt.subplots()
            # Desenha as colunas verticais com a porcentagem de obesos por sexo
            sns.barplot(data=df_prev, x='Gênero', y='Prevalência (%)', palette=[cor_tan, cor_sienna], ax=ax)
            # Coloca o rótulo de dado com o símbolo de porcentagem em cada coluna
            for container in ax.containers: ax.bar_label(container, fmt='%.1f%%', padding=3)
            # Calcula o percentual médio de obesidade para todo o grupo filtrado
            media_geral = df_f['is_obese'].mean() * 100
            # Traça uma linha pontilhada indicando a média geral da população selecionada
            ax.axhline(media_geral, color=cor_peru, linestyle=':', linewidth=2, label=f"Média do Grupo ({media_geral:.1f}%)")
            # Adiciona a legenda informativa no gráfico
            ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor=cor_tan)
            # Define os títulos dos eixos e ajusta a escala vertical para 100%
            ax.set_ylabel("Percentual (%)"); ax.set_xlabel("Gênero"); ax.set_ylim(0, 100); ax.grid(False)
            # Conclui e exibe o gráfico de prevalência
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)

    # --- ABA 2: COMPORTAMENTO ---
    with tab2:
        # Divide a aba em duas colunas para os hábitos alimentares principais
        col1, col2 = st.columns(2)
        with col1:
            # Título do gráfico de consumo de vegetais
            st.subheader("Consumo de Vegetais")
            # Define a sequência lógica das respostas para o gráfico
            ordem_veg = ["Raramente", "Às vezes", "Sempre"]
            # Cria a figura para o gráfico de frequência
            fig, ax = plt.subplots()
            # Desenha a contagem de pacientes para cada nível de consumo de vegetais
            sns.countplot(data=df_f, x='consumo_vegetais', palette=paleta_terrosa, order=ordem_veg, ax=ax)
            # Adiciona o número total de pacientes acima de cada barra (rótulo)
            for container in ax.containers: ax.bar_label(container, padding=3)
            # Formata as legendas e remove a grade visual
            ax.set_xlabel("Frequência"); ax.set_ylabel("Quantidade de Pacientes"); ax.grid(False)
            # Renderiza o gráfico comportamental de vegetais
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)

        with col2:
            # Título da análise de volume de refeições principais
            st.subheader("Refeições Principais por Dia")
            # Define a ordem crescente de quantidade de refeições no eixo X
            ordem_ref = ["1 refeição", "2 refeições", "3 refeições", "Mais de 3"]
            # Inicializa a figura para contagem de refeições
            fig, ax = plt.subplots()
            # Desenha as barras de frequência de refeições principais diárias
            sns.countplot(data=df_f, x='consumo_refeicoes_principais', palette=paleta_terrosa, order=ordem_ref, ax=ax)
            # Coloca o rótulo de dado numérico em cada coluna
            for container in ax.containers: ax.bar_label(container, padding=3)
            # Configura títulos e desativa grades
            ax.set_xlabel("Frequência"); ax.set_ylabel("Quantidade de Pacientes"); ax.grid(False)
            # Renderiza o gráfico de volume de refeições
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)
            

        st.markdown("---")

        col3, col4 = st.columns(2)
        with col3:
            # Título do gráfico de hidratação
            st.subheader("Hidratação Diária")
            # Ordena os níveis de consumo de água
            ordem_agua = ["Baixo", "Moderado", "Alto"]
            # Inicializa a figura para análise hídrica
            fig, ax = plt.subplots()
            # Desenha a frequência de pacientes por nível de hidratação declarado
            sns.countplot(data=df_f, x='consumo_agua', palette=paleta_terrosa, order=ordem_agua, ax=ax)
            # Adiciona os rótulos de dados numéricos acima das barras
            for container in ax.containers: ax.bar_label(container, padding=3)
            # Formata eixos e remove grades
            ax.set_xlabel("Frequência"); ax.set_ylabel("Quantidade de Pacientes"); ax.grid(False)
            # Exibe o gráfico de hidratação no dashboard
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)

        with col4:
            # Título do gráfico de lanches intermediários
            st.subheader("Consumo de Lanches entre as Refeições")
            # Define a ordem lógica para a frequência de beliscar/lanches
            ordem_lanche = ["Nunca", "Baixo", "Moderado", "Alto"]
            # Cria a figura para o gráfico de snacks
            fig, ax = plt.subplots()
            # Desenha as barras de frequência de lanches entre as refeições principais
            sns.countplot(data=df_f, x='consumo_lanches_entre_refeicoes', palette=paleta_terrosa, order=ordem_lanche, ax=ax)
            # Adiciona rótulos de dados numéricos em cada coluna
            for container in ax.containers: ax.bar_label(container, padding=3)
            # Configura eixos e desativa as grades visuais
            ax.set_xlabel("Frequência"); ax.set_ylabel("Quantidade de Pacientes"); ax.grid(False)
            # Renderiza o gráfico de lanches intermediários
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)

    # --- ABA 3: FATORES DE RISCO ---
    with tab3:
        # Divide a aba em duas colunas para análise de genética e vícios
        col1, col2 = st.columns(2)
        with col1:
            # Título da análise de genética familiar
            st.subheader("Histórico Familiar de Sobrepeso")
            # Converte a coluna binária de histórico familiar em texto Sim/Não
            df_f['hist_label'] = df_f['historico_familiar'].map({1: 'Possui', 0: 'Não possui'})
            # Inicializa a figura para o histórico genético
            fig, ax = plt.subplots()
            # Desenha as barras comparando quem possui ou não histórico na família
            sns.countplot(data=df_f, x='hist_label', palette=[cor_sienna, cor_tan], ax=ax)
            # Adiciona rótulos de dados numéricos para facilitar a leitura médica
            for container in ax.containers: ax.bar_label(container, padding=3)
            # Configura títulos de eixos e desativa grades
            ax.set_xlabel("Histórico Familiar de sobrepeso"); ax.set_ylabel("Quantidade de Pacientes"); ax.grid(False)
            # Exibe o gráfico genético
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)

        with col2:
            # Título da análise de consumo alcoólico
            st.subheader("Consumo de Álcool")
            # Define a sequência lógica da frequência de ingestão alcoólica
            ordem_alc = ["Nunca", "Baixo", "Moderado", "Alto"]
            # Cria a figura para o gráfico de álcool
            fig, ax = plt.subplots()
            # Desenha a distribuição de pacientes por frequência de consumo de álcool
            sns.countplot(data=df_f, x='consumo_alcool', palette=paleta_terrosa, order=ordem_alc, ax=ax)
            # Adiciona os rótulos de dados numéricos em cada barra
            for container in ax.containers: ax.bar_label(container, padding=3)
            # Formata legendas e remove grades
            ax.set_xlabel("Frequência"); ax.set_ylabel("Quantidade de Pacientes"); ax.grid(False)
            # Renderiza o gráfico de álcool no dashboard
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)


        st.markdown("---") 

        col3, col4 = st.columns(2)
        with col3:
            # Título da análise de tabagismo
            st.subheader("Perfil de Tabagismo (Fumantes)")
            # Transforma o indicador binário de fumo em etiquetas textuais
            df_f['fuma_label'] = df_f['fuma'].map({1: 'Fumante', 0: 'Não Fumante'})
            # Inicializa a figura para o perfil de fumantes
            fig, ax = plt.subplots()
            # Desenha a proporção de fumantes versus não fumantes no grupo
            sns.countplot(data=df_f, x='fuma_label', palette=[cor_tan, cor_sienna], ax=ax)
            # Coloca o número exato de pacientes acima das barras (rótulo)
            for container in ax.containers: ax.bar_label(container, padding=3)
            # Configura legendas e desativa grades visuais
            ax.set_xlabel("Perfil de Tabagismo"); ax.set_ylabel("Qtd de Pacientes"); ax.grid(False)
            # Exibe o gráfico de tabagismo
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)

        with col4:
            # Título do gráfico de monitoramento calórico
            st.subheader("Monitoramento de Calorias Diárias")
            # Converte a coluna de monitoramento em texto amigável para o eixo X
            df_f['monit_label'] = df_f['monitoramento_calorias'].map({1: 'Monitora', 0: 'Não Monitora'})
            # Cria a figura para o engajamento preventivo
            fig, ax = plt.subplots()
            # Desenha a contagem de pacientes que monitoram ativamente a ingestão de calorias
            sns.countplot(data=df_f, x='monit_label', palette=[cor_tan, cor_sienna], ax=ax)
            # Adiciona os rótulos de dados numéricos no topo das colunas
            for container in ax.containers: ax.bar_label(container, padding=3)
            # Formata legendas e remove grades
            ax.set_xlabel("Monitoramento de Calorias"); ax.set_ylabel("Qtd de Pacientes"); ax.grid(False)
            # Renderiza o gráfico de monitoramento no dashboard
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)

    # --- ABA 4: INSIGHTS ESTRATÉGICOS (CAUSALIDADE DO IMC) ---
    with tab4:
        # Define a primeira linha para analisar fatores Biológicos e Alimentares
        col1, col2 = st.columns(2)
        
        with col1:
            # Título da análise de impacto da idade no peso médio
            st.subheader("Faixa Etária")
            # Agrupa as idades em blocos clínicos para identificar tendências geracionais
            df_f['faixa_etaria'] = pd.cut(df_f['idade'], bins=[0, 25, 40, 60, 100], labels=['Até 25', '26-40', '41-60', '60+'])
            # Calcula a média aritmética do IMC para cada grupo etário definido
            imc_idade = df_f.groupby('faixa_etaria', observed=True)['imc'].mean().reset_index()
            # Inicializa a estrutura da figura para o gráfico de barras
            fig, ax = plt.subplots()
            # Desenha as colunas verticais utilizando a paleta de cores terrosa
            sns.barplot(data=imc_idade, x='faixa_etaria', y='imc', palette=paleta_terrosa, ax=ax)
            # Adiciona rótulos de dados decimais no topo de todas as colunas
            for container in ax.containers: ax.bar_label(container, fmt='%.1f', padding=3)
            # Traça a linha de alerta de obesidade clínica (IMC 30)
            ax.axhline(30, color=cor_sienna, linestyle='--', linewidth=2, label="Alerta Obesidade (IMC 30)")
            # Ativa a legenda dentro de um retângulo branco com borda terrosa
            ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor=cor_tan)
            # Define as legendas dos eixos e desativa as grades de fundo
            ax.set_xlabel("Faixa Etária (Anos)"); ax.set_ylabel("IMC Médio"); ax.set_ylim(0, 50); ax.grid(False)
            # Remove bordas externas e renderiza o gráfico na interface
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)

        with col2:
            # Título da análise de impacto do consumo de calorias no peso
            st.subheader("Consumo de Alimentos Calóricos")
            # Agrupa os pacientes pelo hábito de consumo de alimentos altamente calóricos
            df_cal_imc = df_f.groupby('consumo_alimentos_altamente_caloricos')['imc'].mean().reset_index()
            # Mapeia os indicadores 1 e 0 para os rótulos textuais 'Consome' e 'Não Consome'
            df_cal_imc['label'] = df_cal_imc['consumo_alimentos_altamente_caloricos'].map({1: 'Consome', 0: 'Não Consome'})
            # Inicializa a figura para o gráfico comparativo dietético
            fig, ax = plt.subplots()
            # Desenha as colunas comparativas com as cores específicas da paleta
            sns.barplot(data=df_cal_imc, x='label', y='imc', palette=[cor_tan, cor_sienna], ax=ax)
            # Insere os rótulos de dados numéricos no topo das colunas
            for container in ax.containers: ax.bar_label(container, fmt='%.1f', padding=3)
            # Adiciona a linha de referência de obesidade clínica
            ax.axhline(30, color=cor_sienna, ls='--', lw=2, label="Alerta Obesidade (IMC 30)")
            # Exibe a legenda em moldura retangular para destaque
            ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor=cor_tan)
            # Configura legendas de eixos, escala e desativa grades
            ax.set_ylabel("IMC Médio"); ax.set_xlabel("Alimentos Calóricos"); ax.set_ylim(0, 45); ax.grid(False)
            # Finaliza e exibe o gráfico de impacto dietético
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)

        # Adiciona uma linha de separação visual entre os blocos
        st.markdown("---")
        
        # Define a segunda linha para focar em Estilo de Vida e Atividade
        col3, col4 = st.columns(2)
        
        with col3:
            # Título da análise de impacto do exercício no indicador de peso
            st.subheader("Prática de Exercícios")
            # Define a ordem lógica de intensidade física para o gráfico
            ordem_ativ = ["Sedentário", "Baixo", "Moderado", "Alto"]
            # Calcula o IMC médio reindexando para seguir a ordem de esforço físico
            df_ativ_imc = df_f.groupby('frequencia_atividade_fisica', observed=True)['imc'].mean().reindex(ordem_ativ).reset_index()
            # Inicializa a figura para o gráfico de exercício
            fig, ax = plt.subplots()
            # Desenha colunas verticais com a relação entre atividade física e IMC
            sns.barplot(data=df_ativ_imc, x='frequencia_atividade_fisica', y='imc', palette=paleta_terrosa, ax=ax)
            # Adiciona rótulos de dados numéricos acima de cada barra
            for c in ax.containers: ax.bar_label(c, fmt='%.1f', padding=3)
            # Traça linha de alerta e insere a legenda informativa
            ax.axhline(30, color=cor_sienna, ls='--', lw=2, label="Alerta Obesidade (IMC 30)")
            ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor=cor_tan)
            # Formata eixos e desativa as grades visuais
            ax.set_xlabel("Frequência"); ax.set_ylabel("IMC Médio"); ax.set_ylim(0, 45); ax.grid(False)
            # Renderiza o gráfico de atividade física
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)

        with col4:
            # Título da análise de impacto do meio de transporte no peso
            st.subheader("Meio de Transporte")
            # Calcula o IMC médio por transporte e ordena do menor valor para o maior
            df_transp_imc = df_f.groupby('meio_de_transporte')['imc'].mean().sort_values().reset_index()
            # Inicializa a figura para análise de mobilidade
            fig, ax = plt.subplots()
            # Desenha colunas comparando como cada transporte afeta o IMC do grupo
            sns.barplot(data=df_transp_imc, x='meio_de_transporte', y='imc', palette=paleta_terrosa, ax=ax)
            # Percorre os recipientes e adiciona os rótulos de dados decimais
            for c in ax.containers: ax.bar_label(c, fmt='%.1f', padding=3)
            # Adiciona a linha de alerta e a legenda em destaque
            ax.axhline(30, color=cor_sienna, ls='--', lw=2, label="Alerta Obesidade (30)")
            ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor=cor_tan)
            # Rotaciona os nomes do eixo X e define escala vertical
            ax.set_xlabel("Transporte"); ax.set_ylabel("IMC Médio"); ax.set_ylim(0, 45); plt.xticks(rotation=15); ax.grid(False)
            # Exibe o gráfico de mobilidade estratégica
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)

        # Adiciona a terceira linha para tecnologia e hábitos de snacks
        st.markdown("---")
        col5, col6 = st.columns(2)

        with col5:
            # Título da análise de impacto do uso de tecnologia no peso
            st.subheader("Uso de Tecnologia")
            # Estabelece a ordem de exposição às telas para o eixo X
            ordem_tec = ["Baixo", "Moderado", "Alto"]
            # Calcula o IMC médio por nível de uso tecnológico respeitando a ordem
            df_tec_imc = df_f.groupby('tempo_uso_tecnologia', observed=True)['imc'].mean().reindex(ordem_tec).reset_index()
            # Inicializa a figura para o gráfico de telas
            fig, ax = plt.subplots()
            # Desenha as barras verticais com o perfil de exposição digital
            sns.barplot(data=df_tec_imc, x='tempo_uso_tecnologia', y='imc', palette=paleta_terrosa, ax=ax)
            # Adiciona os rótulos de dados decimais em todas as barras
            for c in ax.containers: ax.bar_label(c, fmt='%.1f', padding=3)
            # Traça a linha de alerta de obesidade e legenda técnica
            ax.axhline(30, color=cor_sienna, ls='--', lw=2, label="Alerta Obesidade (IMC 30)")
            ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor=cor_tan)
            # Finaliza eixos e remove grades visuais
            ax.set_xlabel("Frequência"); ax.set_ylabel("IMC Médio"); ax.set_ylim(0, 45); ax.grid(False)
            # Exibe o gráfico de impacto tecnológico
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)

        with col6:
            # Título da análise de impacto nutricional de lanches extras
            st.subheader("Consumo de Lanches")
            # Ordena a frequência de lanches intermediários para o gráfico
            ordem_lanche = ["Nunca", "Baixo", "Moderado", "Alto"]
            # Agrupa e calcula a média do IMC para cada nível de consumo de snacks
            df_lanche_imc = df_f.groupby('consumo_lanches_entre_refeicoes', observed=True)['imc'].mean().reindex(ordem_lanche).reset_index()
            # Inicializa a figura para o impacto nutricional estratégico
            fig, ax = plt.subplots()
            # Desenha as colunas comparativas de IMC conforme a frequência de lanches
            sns.barplot(data=df_lanche_imc, x='consumo_lanches_entre_refeicoes', y='imc', palette=paleta_terrosa, ax=ax)
            # Coloca rótulos de dados numéricos decimais em cada barra individual
            for c in ax.containers: ax.bar_label(c, fmt='%.1f', padding=3)
            # Adiciona a linha horizontal de referência e a legenda destacada
            ax.axhline(30, color=cor_sienna, ls='--', lw=2, label="Alerta Obesidade (IMC 30)")
            ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor=cor_tan)
            # Define os limites de visualização e remove grades
            ax.set_xlabel("Frequência"); ax.set_ylabel("IMC Médio"); ax.set_ylim(0, 45); ax.grid(False)
            # Finaliza e exibe o último gráfico estratégico da aba
            sns.despine(ax=ax); st.pyplot(fig); plt.close(fig)

st.markdown("---")

# Adiciona o crédito final da aplicação centralizado no rodapé
st.caption("Dashboard MedAnalytics | Projeto do curso de Pós Graduação de Data Analytics da FIAP.")
st.caption("* MedAnalytics | Gestão de Saúde é um nome fictício utilizado para fins estritamente acadêmicos.")