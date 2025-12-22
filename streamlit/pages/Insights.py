# ==========================================================================
# Importe de bibliotecas
# ==========================================================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import joblib
import os

# ==========================================================================
# Config página
# ==========================================================================
st.set_page_config(
    page_title="Modelo de Predição sobre o risco de obesidade nas pessoas", # Define o nome na aba do navegador.
    page_icon="🎯", # Define o emoji que aparece na aba.
    layout="wide" # Define que o conteúdo do site ficará centralizado na tela.
)

# ==========================================================================
# Funções
# ==========================================================================

def setup_options(lista):
    """
    Ordena as opções de respostas em ordem crescente.
    """ 
    def chave_interna(texto):
        if not isinstance(texto, str):
            texto = str(texto) if texto is not None else ""
        return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ascii').lower()
    
    return sorted(lista, key=chave_interna)



def config_page(): # Configurar menu lateral
    """
    Desenha os elementos na barra lateral esquerda.
    """
    with st.sidebar: # Inicia o contexto da barra lateral.
         st.markdown("🎯 Desafio") # Título da seção.
         st.info("Modelo preditivo desenvolvivo para a pós graduação de **Data Analytics da FIAP**.") # Quadro informativo.
         st.markdown("---") # Linha horizontal divisória.
         st.markdown("👩🏽‍💻 Aluno(a):")
         st.write("""
         [Geovana dos Santos ferreira](https://www.linkedin.com/in/geovanaferreira/) 
         """)
         st.markdown("---")
         st.markdown("🔗 Repositório:")
         st.markdown("""
             <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
             <style>
                 .github-icon {
                     font-size: 35px;
                     color: #24292e; /* Cor padrão do GitHub */
                     text-decoration: none;
                     transition: 0.3s;
                 }
                 .github-icon:hover {
                     color: #6e5494; /* Cor roxa ao passar o mouse */
                 }
             </style>
     
             <a href="https://github.com/geoferreira1/fiap_tech_challenge_fase_4" target="_blank" class="github-icon">
                 <i class="fa-brands fa-github"></i>
             </a>
         """, unsafe_allow_html=True)

def main(): # Função princial
    # 1. Configura a Barra Lateral
    config_page()

    # 3. Página do cálculo predição
    st.title("🎯 Modelo de Predição sobre o risco de obesidade nas pessoas")
    st.markdown("""
    Preencha o formulário a seguir para que o modelo calcule a probabilidade do risco de obesidade do paciente.
    """)
    st.markdown("---")

if __name__ == "__main__":
    main()