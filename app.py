import streamlit as st
import pandas as pd
import libreria_funciones as lf
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression

st.image("Includata EC.png")

st.title("Dashboard Interactivo para el Monitoreo de la Discapacidad en el Sistema Educativo Ecuatoriano")

st.sidebar.image("Banner_IncludataEC2.png")


st.sidebar.markdown(f"""
    ## **Ojetivo de la aplicación:**
    Desarrollar un dashboard interactivo para el monitoreo de estudiantes con discapacidad en el sistema educativo ecuatoriano mediante técnicas de Ciencia de Datos y la plataforma Streamlit.""")

st.sidebar.markdown(f"""
    ## **Integrantes:**
    -  Luis Alberto Chicaiza González
    -  Juan Diego Romero Fernández """)

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

st.markdown(f"""
### Datos informativos
**Provincia:** {provincia}  
**Cantón:** {canton}  
**Año lectivo:** {año_lectivo}
""")

st.write("Vista previa de los datos filtados")
st.subheader("Datos filtrados")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

# Filtrar por año lectivo y provincia
df_provincia = df[
    (df['Provincia'] == provincia) &
    (df['Año_lectivo'] == año_lectivo)
] 

# Sumar estudiantes de toda la provincia
total_estudiantes_provincia = df_provincia['Total_Estudiantes'].sum()


# Filtrar por año lectivo, provincia y cantón
df_canton = df[
    (df['Provincia'] == provincia) &
    (df['Canton'] == canton) &
    (df['Año_lectivo'] == año_lectivo)
]

# Sumar estudiantes del cantón
total_estudiantes_canton = df_canton['Total_Estudiantes'].sum()

# Variables obtenidas de los filtros
provincia = provincia
canton = canton
año_lectivo = año_lectivo

grafico = px.histogram(
    df_filtrado,
    x="Discapacidad", 
    title=f"Distribución por Tipo de Discapacidad - {provincia} | {canton} | {año_lectivo}"
)

st.sidebar.markdown(f"""
### Datos Informativos
**Provincia:** {provincia}  
**Cantón:** {canton}  
**Año lectivo:** {año_lectivo}
""")

st.sidebar.markdown(f"""**Distribución por Tipo de Discapacidad - {provincia} | {canton} | {año_lectivo}**""")


grafico_barras = px.bar(
    df_filtrado,
    x="Discapacidad",
    color_discrete_sequence=["green"]
)
# Cantidad de registros del cantón filtrado
cant_canton = len(df_filtrado)

# Cantidad de registros de la provincia seleccionada
df_provincia = df[df["Provincia"] == provincia]
cant_provincia = len(df_provincia)

# Cantidad de estudiantes con discapacidad por cantón
# cant_estud_canton = df["Total_Estudiantes"].sum()
# sum_provincia = sum(df_provincia)


# Porcentaje del cantón respecto a la provincia
porcentaje = (total_estudiantes_canton / total_estudiantes_provincia * 100) if total_estudiantes_provincia > 0 else 0

st.plotly_chart(grafico, use_container_width=True)
st.sidebar.plotly_chart(grafico_barras, use_container_width = True) 


# CSS para los recuadros
st.markdown("""
<style>
.indicador{
    border:2px solid #c0392b;
    padding:15px;
    text-align:center;
    border-radius:8px;
    background-color:#111111;
    color:white;
    font-size:18px;
    font-weight:bold;
}
.valor{
    font-size:28px;
    color:#4FC3F7;
}
</style>
""", unsafe_allow_html=True)

# Crear columnas
col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.markdown(f"""
    <div class="indicador">
        Estudiantes provincia<br>
        <span class="valor"> {total_estudiantes_provincia:,.0f}</span>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="indicador">
        Estudiantes Cantón<br>
        <span class="valor">{total_estudiantes_canton:,.0f}</span>
    </div>
    """, unsafe_allow_html=True)
with col3:
   st.markdown(f"""
  <div class="indicador">
        % Cantón Vs Provincia<br>
    <span class="valor">{porcentaje:.2f}%</span>
   </div>
   """, unsafe_allow_html=True)

# Filtrar según la selección del usuario
df_pred = df[
    (df["Provincia"] == provincia) &
    (df["Canton"] == canton)
].copy()

# Agrupar por año lectivo
df_pred = (
    df_pred
    .groupby("Año_lectivo", as_index=False)
    ["Total_Estudiantes"]
    .sum()
)

# Ordenar por año
df_pred = df_pred.sort_values("Año_lectivo")

# Crear variable numérica para el modelo
df_pred["Periodo"] = np.arange(len(df_pred))

X = df_pred[["Periodo"]]
y = df_pred["Total_Estudiantes"]

# Entrenar modelo
modelo = LinearRegression()
modelo.fit(X, y)

# Número de años a proyectar
n_predicciones = 5

# Generar períodos futuros
ultimo_periodo = df_pred["Periodo"].max()

X_futuro = pd.DataFrame({
    "Periodo": range(
        ultimo_periodo + 1,
        ultimo_periodo + n_predicciones + 1
    )
}) 

# Predicciones
predicciones = modelo.predict(X_futuro)

ultimo_año = int(
    str(df_pred["Año_lectivo"].iloc[-1]).split("-")[0]
)

años_futuros = [
    f"{a}-{a+1}"
    for a in range(
        ultimo_año + 1,
        ultimo_año + n_predicciones + 1
    )
]

fig_pred = go.Figure()

# Datos históricos
fig_pred.add_trace(
    go.Scatter(
        x=df_pred["Año_lectivo"],
        y=df_pred["Total_Estudiantes"],
        mode="lines+markers",
        name="Histórico"
    )
)

# Proyección
fig_pred.add_trace(
    go.Scatter(
        x=años_futuros,
        y=predicciones,
        mode="lines+markers",
        line=dict(dash="dash"),
        name="Proyección"
    )
)

fig_pred.update_layout(
    title=f"Proyección de Estudiantes con Discapacidad - {provincia} - {canton}<br>",
    xaxis_title="Año Lectivo",
    yaxis_title="Total de Estudiantes",
    width= 500,
    height=450,
    template="plotly_white"
)


st.plotly_chart(
    fig_pred,
    use_container_width=True
)

df_proyeccion = pd.DataFrame({
    "Año_lectivo": años_futuros,
    "Estudiantes_Proyectados": predicciones.round().astype(int)
})
st.sidebar.subheader("Proyección de Estudiantes con Discapacidad")
st.sidebar.dataframe(df_proyeccion, use_container_width=True)

st.footer.image("Banner_IncludataEC2.png")

