import streamlit as st
import pandas as pd
import libreria_funciones as lf
import plotly.express as px

st.title("Dashboard Interactivo para el Monitoreo de la Discapacidad en el Sistema Educativo Ecuatoriano")

st.sidebar.title("Parámetros")

st.sidebar.title("Contenidos")

st.sidebar.image("python.png")


uploaded_files = st.file_uploader(
    "Upload data", accept_multiple_files=True, type="csv"
)
for uploaded_file in uploaded_files:
    df = pd.read_csv(uploaded_file)
    st.write(df)

st.title("Dashboard de Discapacidad Estudiantil")

st.write("Vista previa de los datos")
st.dataframe(df.head())

# Selección de provincia
provincias = sorted(df["PROVINCIA"].dropna().unique())

provincia = st.sidebar.selectbox(
    "Seleccione una provincia",
    provincias
)

df_filtrado = df[df["PROVINCIA"] == provincia]

# Gráfico
grafico = px.histogram(
    df_filtrado,
    x="TIPO_DISCAPACIDAD",
    title="Distribución por Tipo de Discapacidad"
)

st.plotly_chart(grafico, use_container_width=True)



