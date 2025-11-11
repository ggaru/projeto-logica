import pandas as pd 
import os
from openpyxl import load_workbook
import streamlit as st

#classe responsável pelo cadastro de ocorrencias
class Ocorrencias:
    def __init__(self):
        self.pathArquivo = "funcionarios.xlsx"
        self.ocorrencia = {}

    #função que verifica se o funcionário está ou não cadastrado
    def acharFuncionario(self):
        if not os.path.exists(self.pathArquivo):
            st.warning("Arquivo de funcionários não encontrado.")
            return False
        
        #input do nome
        nome = st.text_input("Qual o nome do funcionário?", key="nome")
        #busca do funcionário
        if st.button("Buscar"):
            df = pd.read_excel(self.pathArquivo)
            encontrado = df[df["nome"] == nome]
            #retorna true ou false se o funcionário existe e armazena seu cargo e nome em um dicionário 
            if not encontrado.empty:
                funcionario = encontrado.iloc[0]
                st.success("Funcionário encontrado!")
                st.success(f"Nome: {funcionario['nome']} \nCargo: {funcionario['cargo']}")
                st.session_state.funcionario_encontrado = {
                    "nome": funcionario["nome"],
                    "cargo": funcionario["cargo"]
                }
                return True
            else:
                st.warning("Funcionário inexistente, cadastre-o primeiro.")
                return False

        #se já encontrou antes, mantém
        if "funcionario_encontrado" in st.session_state:
            return True
        return False

    #recebe e registra a ocorrência em um dicionário
    def registrarOcorrencia(self):
        #chama a função para achar o funcionário
        if self.acharFuncionario():
            funcionario = st.session_state.get("funcionario_encontrado", {})
            st.info(f"Registrando ocorrência para: **{funcionario.get('nome', '')}**")

            #formulário de cadastro
            with st.form("form_ocorrencias"):
                days = st.number_input("Quantos dias afastados?", min_value=0, max_value=15, step=1)
                injury = st.radio("Houve Lesão?", ['Sim', 'Não'])
                tipo = st.radio("Tipo de acidente", ['Acidente', 'Incidente', 'Quase Acidente'])
                date = st.date_input("Digite a data da ocorrência:")
                submit = st.form_submit_button("Enviar")

            #envio de inputs para o dicionário
            if submit:
                self.ocorrencia = {
                    **funcionario,
                    "Dias afastados": days,
                    "Lesão": injury,
                    "Tipo": tipo,
                    "Data": str(date),
                }
                #chamada de função para salvar ocorrencia
                self.salvarOcorrencias(self.ocorrencia)
                st.success(f"✅ Ocorrência de {funcionario['nome']} cadastrada com sucesso!")

    #função que salvará a ocorrencia em uma aba diferente da planilha
    def salvarOcorrencias(self, funcionario):
        df_new = pd.DataFrame([funcionario])
        aba = "Ocorrências"
        if not os.path.exists(self.pathArquivo):
            with pd.ExcelWriter(self.pathArquivo, engine="openpyxl") as writer:
                df_new.to_excel(writer, sheet_name=aba, index=False)
            st.success("✅ Arquivo criado. Dados salvos com sucesso!")
        else:
            with pd.ExcelWriter(self.pathArquivo, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                try:
                    df_existente = pd.read_excel(self.pathArquivo, sheet_name=aba)
                    df_atualizado = pd.concat([df_existente, df_new], ignore_index=True)
                except ValueError:
                    df_atualizado = df_new
                df_atualizado.to_excel(writer, sheet_name=aba, index=False)
            st.success(f"✅ Registro adicionado à aba '{aba}' com sucesso!")
