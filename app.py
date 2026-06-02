import streamlit as st
import pandas as pd
import libreria_funciones as lf
import plotly.express as px

st.image("python.png")

st.title("Dashboard Interactivo para el Monitoreo de la Discapacidad en el Sistema Educativo Ecuatoriano")

st.sidebar.title("Parámetros")

st.sidebar.title("Contenidos")

# Cargar datos
df = pd.read_excel("Base_Inicio_Historico_Discapacidad.xlsx")

st.write("Vista previa de los datos")
st.dataframe(df.head())

# Selección de provincia
provincias = sorted(df["Provincia"].dropna().unique())

provincia = st.sidebar.selectbox(
    "Seleccione una provincia",
    provincias
)

cantones = sorted(
    df[df["Provincia"] == provincia]["Canton"]
    .dropna()
    .unique()
)

canton = st.sidebar.selectbox(
    "Selecciones un cantón", 
    cantones
)   

año_lectivo = sorted(
    df[
        (df["Provincia"] == provincia) &
        (df["Canton"] == canton)
      ]["Año_lectivo"]
      .dropna()
      .unique()
)

año_lectivo = st.sidebar.selectbox(
    "Selecciones el año lectivo", 
    año_lectivo
)  

df_filtrado = df[
    (df["Provincia"] == provincia) &
    (df["Canton"] == canton) &
    (df["Año_lectivo"] == año_lectivo)
]

st.write("Vista previa de los datos")
st.subheader("Datos filtrados")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

# Gráfico
#grafico = px.histogram(
#    df_filtrado,
 #    x="Discapacidad",
#     title="Distribución por Tipo de Discapacidad"
# )

# st.plotly_chart(grafico, use_container_width=True)

# Variables obtenidas de los filtros
provincia = provincia
canton = canton
año_lectivo = año_lectivo

grafico = px.histogram(
    df_filtrado,
    x="Discapacidad", 
    title=f"Distribución por Tipo de Discapacidad - {provincia} | {canton} | {año_lectivo}"
)

grafico_barras = px.bar(
    df_filtrado,
    x="Discapacidad", 
    title=f"Distribución por Tipo de Discapacidad <br> - Provincia: {provincia}  <br> | Cantón: {canton}  <br> | Año lectivo: {año_lectivo}",
    color_discrete_sequence=["green"]
)


st.plotly_chart(grafico, use_container_width=True)
st.sidebar.plotly_chart(grafico_barras, use_container_width = True)
