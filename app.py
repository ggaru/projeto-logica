import streamlit as st
from funcionarios import Funcionarios
from ocorrencias import Ocorrencias


# Inicializa a instância da classe
if "callFunc" not in st.session_state:
    st.session_state.callFunc = Funcionarios()
if "callOc" not in st.session_state:
    st.session_state.callOc = Ocorrencias()

# Flags para controlar as telas
if "mostrar_func" not in st.session_state:
    st.session_state.mostrar_func = False
if "cadastrar_oc" not in st.session_state:
    st.session_state.cadastrar_oc = False
if "relatorios" not in st.session_state:
    st.session_state.relatorios = False


st.title("Registro de Ocorrências") 
st.sidebar.header("Menu")

# Botão apenas altera a flag
if st.sidebar.button("Cadastrar Funcionários"):
    st.session_state.mostrar_func = True
    st.session_state.cadastrar_oc = False   
    st.session_state.relatorios = False
if st.sidebar.button("Cadastrar Ocorrências"):
    st.session_state.mostrar_func = False   # reseta a outra tela
    st.session_state.cadastrar_oc = True
    st.session_state.relatorios = False
if st.sidebar.button("Relatórios"):
    st.session_state.mostrar_func = False   # reseta a outra tela
    st.session_state.cadastrar_oc = False
    st.session_state.relatorios = True


# Renderiza os inputs sempre que a flag estiver ativa
if st.session_state.mostrar_func:
    st.session_state.callFunc.Gerador_funcionarios()
elif st.session_state.cadastrar_oc:
    st.session_state.callOc.calculosOcorrencia()
elif st.session_state.relatorios:
    st.write("relatorios")