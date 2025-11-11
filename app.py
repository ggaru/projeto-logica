import streamlit as st
from funcionarios import Funcionarios
from ocorrencias import Ocorrencias
from relatorios import Relatorios

#### INICIO DO CÓDIGO -- MENU INICIAL

#Inicializa a instância das classes Funcionários, Ocorrencias e Relatórios para chamadas.
if "funcionarios" or "ocorrencias" or "relatorios" not in st.session_state:
    st.session_state.funcionarios = Funcionarios()
    st.session_state.ocorrencias = Ocorrencias()
    st.session_state.relatorios = Relatorios()

#titulo e sidebar
st.title("Registro de Ocorrências") 
st.sidebar.header("Menu")

#define a tela atual a ser exibida
if st.sidebar.button("Cadastrar Funcionários"):
    st.session_state.tela_atual = "funcionarios"
if st.sidebar.button("Cadastrar Ocorrências"):
    st.session_state.tela_atual = "ocorrencias"
if st.sidebar.button("Visualizar Funcionários"):
    st.session_state.tela_atual = "relatorio_func"
if st.sidebar.button("Relatório Ocorrências"):
    st.session_state.tela_atual = "relatorio_oc"
if "tela_atual" not in st.session_state:
    st.session_state.tela_atual = None

# Renderiza os inputs sempre que a flag estiver ativa
if st.session_state.tela_atual == "funcionarios":
    st.session_state.funcionarios.Gerador_funcionarios()
elif st.session_state.tela_atual == "ocorrencias":
    st.session_state.ocorrencias.registrarOcorrencia()
elif st.session_state.tela_atual == "relatorio_func":
    st.session_state.relatorios.relatorioFunc()
elif st.session_state.tela_atual == "relatorio_oc":
    st.session_state.relatorios.relatorioOc()