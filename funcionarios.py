#importando bibliotecas e frameworks
import pandas as pd 
import os
from openpyxl import load_workbook
import streamlit as st

#classe funcionários
class Funcionarios():
    """Classe responsável pelo cadastro dos funcionários e criação do arquivo principal. """

    #função inicial da classe
    def __init__(self):
        self.pathArquivo = "funcionarios.xlsx"
        
    #função que gera o funcionário apartir do seu nome e cargo, salva-o em um dicionário
    def Gerador_funcionarios(self):        
    #formulário para input de nome e cargo do funcionário
        with st.form("form_funcionario"):
            name = st.text_input("Digite seu nome:", key="nome_input")
            cargo = st.text_input("Digite seu cargo:", key="cargo_input")
            enviar = st.form_submit_button("Cadastrar")

        #após envio, verifica se o nome e cargo foram preenchidos e chama a função passando os inputs
        if enviar:
            if not name or not cargo:
                st.warning("⚠️ Preencha todos os campos antes de salvar.")
            else:
                funcionario = [{"nome": name, "cargo": cargo}]
                self.salvarFuncionarios(funcionario)
                st.success(f"✅ Funcionário {name} ({cargo}) cadastrado com sucesso!")

    #função responsável por salvar os funcionários cadastrados em uma aba especifica da planilha.          
    def salvarFuncionarios(self, funcionario):
        df_new = pd.DataFrame(funcionario)
        aba = "Funcionários"
        if not os.path.exists(self.pathArquivo):
            with pd.ExcelWriter(self.pathArquivo, engine="openpyxl") as writer:
                df_new.to_excel(writer, sheet_name=aba, index=False)
            st.write("✅ Arquivo criado. Dados salvos com sucesso!")
        else:
            with pd.ExcelWriter(self.pathArquivo, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                try:
                    df_existente = pd.read_excel(self.pathArquivo, sheet_name=aba)
                    df_atualizado = pd.concat([df_existente, df_new], ignore_index=True)
                except ValueError:
                    df_atualizado = df_new

                df_atualizado.to_excel(writer, sheet_name=aba, index=False)
            st.write(f"✅ Registro adicionado à aba '{aba}' com sucesso!")
