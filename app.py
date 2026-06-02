import streamlit as st
import pandas as pd
import libreria_funciones as lf


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





