#importando bibliotecas e frameworks
import pandas as pd 
import os
from openpyxl import load_workbook
import streamlit as st

class Ocorrencias():
    """Classe responsável pelo registro de ocorrências e da criação de outra aba no arquivo principal"""

    #função de inicio da classe
    def __init__(self):
        self.pathArquivo = "funcionarios.xlsx"
        self.funcionario = {}
        

    #função responsável por achar um funcionárieo já cadastrado e retornar o seu cargo.
    def acharFuncionario(self, nome):
        #condicional que checa se o arquivo existe
        if not os.path.exists(self.pathArquivo):
            st.warning("Arquivo de funcionários não encontrado.")
        
        #guarda o arquivo na variavel
        df = pd.read_excel(self.pathArquivo)
        encontrado = df[df["nome"] == nome]

        #caso o arquivo exista:
        if not encontrado.empty:
            funcionario = encontrado.iloc[0]  
            st.success("Funcionário encontrado!")
            st.success(f"Nome: {funcionario['nome']} \nCargo: {funcionario['cargo']}")
            self.funcionario = {
                "nome": funcionario["nome"],
                "cargo": funcionario["cargo"]
            } 
            return True
        else:
            st.warning("Funcionário inexistente, cadastre-o primeiro.")
            return False

    #cadastra as ocorrências
    def calculosOcorrencia(self):
        name = st.text_input("Qual o nome do funcionário?", key="nome")
        button = st.button("Buscar")
        if button:
            registeredEmpl = self.acharFuncionario(name)
            if registeredEmpl != False:
                with st.form("form_ocorrencias", clear_on_submit=False):
                        days = st.number_input("Quantos dias afastados? ", key="dias",min_value=0,max_value=15,step=1)
                        injury = st.radio("Houve Lesão?", ['Sim', 'Não'])
                        type = st.radio("Tipo de acidente", ['Acidente', 'Incidente', 'Quase Acidente'])
                        date = st.date_input("Digite a data da ocorrência:")
                        submit = st.button("teste")
                        form = st.form_submit_button("Enviar")
                        if submit:
                            st.success("Teste")
                            self.funcionario.update({
                                "Dias afastados:":days,
                                "Lesão: ":injury,
                                "Tipo: ": type,
                                "Data: ": date,
                            })
        st.write(self.funcionario)   
    """def salvarOcorrencias(self, funcionario):
        df_new = pd.DataFrame([funcionario])
        aba = "Ocorrências"

        if not os.path.exists(self.pathArquivo):
            # Arquivo não existe → criar e adicionar a aba
            with pd.ExcelWriter(self.pathArquivo, engine="openpyxl") as writer:
                df_new.to_excel(writer, sheet_name=aba, index=False)
            print("✅ Arquivo criado. Dados salvos com sucesso!")

        else:
            # Arquivo existe
            with pd.ExcelWriter(self.pathArquivo, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                try:
                    # Tenta ler a aba existente
                    df_existente = pd.read_excel(self.pathArquivo, sheet_name=aba)
                    df_atualizado = pd.concat([df_existente, df_new], ignore_index=True)
                except ValueError:
                    # Aba não existe → criar novo DataFrame
                    df_atualizado = df_new

                # Salva/atualiza a aba
                df_atualizado.to_excel(writer, sheet_name=aba, index=False)
            print(f"✅ Registro adicionado à aba '{aba}' com sucesso!")

"""