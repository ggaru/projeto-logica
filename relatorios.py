#importando bibliotecas e frameworks
import pandas as pd

class Relatorios():
    """Classe responsável pela criação de relatórios com base nos registros já feitos."""

    def __init__(self):
        self.gerarRelatorio()

    #função que gera o relatório automaticamente apartir da leitura do arquivo já criado e dos registros feitos.
    def gerarRelatorio(self):
        #seleção de tipos de relatório
        relatorio = int(input("Lista de relatórios disponiveis: \n1 - Funcionários cadastrados\n2 - Ocorrências\n"))
        df = pd.read_excel("funcionarios.xlsx", sheet_name=None)

        if relatorio == 1:
            n = 0
            print(df["Funcionários"])
            for i in df["Funcionários"]["nome"]:
                n += 1
            print(f"\nVocê tem {n} funcionários cadastrados. \n")

        elif relatorio == 2:
            print(df["Ocorrências"])
            n = 0
            dias = 0
            for i in df["Ocorrências"]["Dias afastados:"]:
                n+= 1
            dias = df["Ocorrências"]["Dias afastados:"].sum()
            print(f"Você teve um total de {n} acidentes e o total de dias afastados foi de {dias}")
        