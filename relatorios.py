#importando bibliotecas e frameworks
import pandas as pd
import streamlit as st
import os

class Relatorios():
    """Classe responsável pela criação de relatórios com base nos registros já feitos."""
    #le as duas abas da planilha
    def __init__(self):
        self.path_arq = "funcionarios.xlsx"
        self.funcionarios = pd.read_excel(self.path_arq, sheet_name="Funcionários")
        self.ocorrencias = pd.read_excel(self.path_arq, sheet_name="Ocorrências")
        self.ocorrenciasMes = {}

    #relatório simples de quantidade de funcionários e cargos
    def relatorioFunc(self):
        func_df = pd.DataFrame(self.funcionarios)
        oc_df = pd.DataFrame(self.ocorrencias)
        cargos_validos = ["Gerente", "Supervisor", "Operário"]       
        st.write(func_df)
        num_func = 0
        leng = 0
        qnt_gerente = 0
        qnt_supervisor = 0
        qnt_invalid = 0
        qnt_operarios = 0
        for i in func_df['nome']:
            leng += 1
        for j in range(leng):
            cargo = func_df.iloc[j][1]
            if cargo == cargos_validos[1]:
                qnt_supervisor +=1
            elif cargo == cargos_validos[0]:
                qnt_gerente +=1
            elif cargo == cargos_validos[2]:
                qnt_operarios +=1
            else:
                qnt_invalid += 1
            num_func += 1
        st.write(f"Você possui {num_func} funcionários cadastrados.")
        st.write(f"Desses funcionários, você possui {qnt_gerente} Gerentes, {qnt_supervisor} Supervisores, {qnt_operarios} Operários.")
        if qnt_invalid != 0:
            st.warning(f"Atenção! Você possui {qnt_invalid} funcionários com cargo não válido. Favor verificar.")
        
        func_df_filtrado = func_df[func_df["cargo"].isin(cargos_validos)]
        cargo_num = func_df_filtrado['cargo'].value_counts().reset_index()
        cargo_num.columns = ['cargo', 'Quantidade']
        st.bar_chart(cargo_num.set_index('cargo'))
            
    def relatorioOc(self):
        st.subheader("Relatório de Ocorrências por Mês")

        def atualizaMes():
            st.session_state["mes"] = st.session_state["mes_selecionado"]

        st.selectbox( "Qual mês?",
            ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro", "Ano"),
            key="mes_selecionado",
            on_change=atualizaMes
        )
        enviar = st.button("Gerar Relatório")
        if enviar:
            if "mes_selecionado" in st.session_state:
                option = st.session_state["mes_selecionado"]
                st.write(f"Exibindo relatório de {option}")

                new_df = pd.DataFrame(self.ocorrencias)
                new_df["Data"] = pd.to_datetime(new_df["Data"])

                meses = {
                    "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4,
                    "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
                    "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12, "Ano":13
                }
                mes_num = meses[option]
                if mes_num != 13:
                    df_mes = new_df[new_df["Data"].dt.month == mes_num]                    
                    st.dataframe(df_mes)
                    efetivo = 223
                    hht = round(efetivo * 220, 2)
                    total_acidentes = (df_mes['Tipo'] == 'Acidente').sum()
                    total_dias_afastados = df_mes[df_mes['Tipo'] == 'Acidente']['Dias afastados'].sum()
                    tf = round((total_acidentes * 1_000_000) / hht, 2)
                    tg = round((total_dias_afastados * 1_000_000) / hht, 2)
                    
                    self.ocorrenciasMes = {
                        "Mês": option,
                        "Efetivo": efetivo,
                        "Hht": hht,
                        "Total Acidentes": total_acidentes,
                        "Dias afastados": total_dias_afastados,
                        "TF": tf,
                        "TG": tg,
                    }
                    df_ocorrencia_mes = pd.DataFrame([self.ocorrenciasMes])
                    st.write(df_ocorrencia_mes)

                    self.salvarRelatorio(self.ocorrenciasMes)
                elif mes_num == 13:
                    self.relatorioAnual()

    def salvarRelatorio(self,data):
        df_new = pd.DataFrame([data])
        aba = "Relatórios"
        mes_novo = df_new.loc[0, "Mês"]

        if not os.path.exists(self.path_arq):
            with pd.ExcelWriter(self.path_arq, engine="openpyxl") as writer:
                df_new.to_excel(writer, sheet_name=aba, index=False)
            st.success("✅ Arquivo criado e relatório salvo com sucesso!")
            return

        try:
            df_existente = pd.read_excel(self.path_arq, sheet_name=aba)
        except ValueError:
            df_existente = pd.DataFrame()

        if not df_existente.empty and "Mês" in df_existente.columns:
            df_existente = df_existente[df_existente["Mês"] != mes_novo]
            df_atualizado = pd.concat([df_existente, df_new], ignore_index=True)
        else:
            df_atualizado = df_new

        with pd.ExcelWriter(self.path_arq, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            df_atualizado.to_excel(writer, sheet_name=aba, index=False)

    def relatorioAnual(self):
        relatorioAnual = pd.read_excel(self.path_arq, sheet_name="Relatórios")
        df_anual = pd.DataFrame(relatorioAnual)
        meses = [
                    "Janeiro", "Fevereiro", "Março", "Abril",
                    "Maio", "Junho", "Julho", "Agosto",
                    "Setembro", "Outubro", "Novembro", "Dezembro"
                ]
        df_anual["Mês"] = pd.Categorical(df_anual["Mês"], categories=meses, ordered=True)

        # Reordena o DataFrame conforme os meses
        df_anual = df_anual.sort_values("Mês")


        st.write(df_anual)
        st.line_chart(df_anual, x= "Mês", y="TG")
        st.line_chart(df_anual, x= "Mês", y="TF")
        st.line_chart(df_anual, x= "Mês", y="Hht")
        