import streamlit as st
import pandas as pd
import libreria_funciones as lf
import plotly.express as px

st.title("Dashboard Interactivo para el Monitoreo de la Discapacidad en el Sistema Educativo Ecuatoriano")

st.sidebar.title("Parámetros")

st.sidebar.title("Contenidos")

st.sidebar.image("python.png")

# Cargar datos
df = pd.read_excel("Base_Inicio_Historico_Discapacidad.xlsx")

#st.write("Vista previa de los datos")
#st.dataframe(df.head())

st.subheader("Datos filtrados")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

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

# Gráfico
grafico = px.histogram(
    df_filtrado,
    x="Discapacidad",
    title="Distribución por Tipo de Discapacidad"
)

st.plotly_chart(grafico, use_container_width=True)


