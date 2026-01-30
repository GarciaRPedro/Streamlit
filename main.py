import streamlit as st
from PIL import Image
import pandas as pd
# import pandas_gbq
import os

img = Image.open(r"data/BRASÃO PREFEITURA LARANJA.png")


st.set_page_config(page_title="Consulta Sql", page_icon=img)
## DEFS

def consulta():
    try:
        df = pd.read_gbq(
            select,
            project_id=project_id,
            dialect="standard"
        )
        # st.success("Consulta executada com sucesso!")
        st.session_state.tabela = df
    except Exception as e:
        st.session_state.erro= e
         
def exportar():   # ["Parquet", "Excel", "CSV"]
    if formato == 'CSV':
        df.to_csv(caminho, sep= f"{separador}", encoding= 'utf-8')
        
    elif formato == 'Parquet':
        df.to_parquet(caminho)

    elif formato == 'Excel':
        df.to_excel(caminho, engine= 'xlsxwriter')



## End Defs
st.markdown("""
# Aplicação de consulta SQL 

##### Digite a baixo o Project_id e o Select
            """)
st.space(size='small')

select = st.text_input('Select', placeholder='Ex.: SELECT * FROM project_id.dataset.nome_da_tabela')

st.space('xxsmall')

project_id = st.text_input('Project ID', placeholder= 'Ex.: infra-itaborai')

esquerda, direita= st.columns([3, 1])

with direita:
        st.space('xxsmall')
        st.button("Query", type="secondary", 
                on_click= consulta, icon= "🔎",
                icon_position="right")
        
if "tabela" in st.session_state:
    st.markdown("### Resultado da consulta")
    st.dataframe(st.session_state.tabela)
    df = st.session_state.tabela
elif "erro" in st.session_state:
    st.markdown("### Erro na consulta")
    st.exception(st.session_state.erro)
st.space('small')
# Formato exportação


if "disabled" not in st.session_state:
    st.session_state.disabled = True



col1, col2= st.columns([2, 2])
with col1:
    formato = st.radio("Formato exportação",
             ["Parquet", "Excel", "CSV"], 
             index= None)


if formato == 'CSV':
    st.session_state.disabled = False
else:
    st.session_state.disabled = True


with col2:
    
    st.write("Separador do CSV")
    separador = st.text_input('Separador', 
                            placeholder="Insira o caractere Ex.:  ' ; ' ",
                            value= ";",
                            disabled= st.session_state.disabled)
    st.markdown("""
                obs.:
                Encoding por padrão será UTF-8
""")

caminho = st.text_input('Caminho export')
st.write("Obs.: Adicione o caminho com o nome esperado do arquivo e a extensao")


col1, col2, col3= st.columns([2, 3, 1])

# if "export_dis" not in st.session_state:
#     st.session_state.export_dis = True

with col1:
    export_dis  = st.checkbox("Ciente do Formato escolhido e do caminho do Save", 
                              value=False)

if export_dis :
    st.session_state.export_dis = False
else:
    st.session_state.export_dis= True

with col2: 
    st.space('small')
    if st.button("Exportar", type="secondary", disabled= st.session_state.export_dis, 
                 on_click= exportar):
        st.success(" Exportação cocluida com sucesso")

