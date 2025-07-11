import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("DATA_PILOTO_PV.csv", sep='|', encoding='utf-8', engine='python', on_bad_lines='skip'


df = load_data()

st.set_page_config(page_title="Dashboard Stock", layout="wide")
st.title("🚗 Dashboard de Repuestos - Postventa")

# Filtros
col1, col2 = st.columns(2)
with col1:
    marca = st.selectbox("Marca", ["Todos"] + sorted(df['marca'].dropna().unique()))
with col2:
    modelo = st.selectbox("Modelo", ["Todos"] + sorted(df['modelo'].dropna().unique()))

# Aplicar filtros
df_filtered = df.copy()
if marca != "Todos":
    df_filtered = df_filtered[df_filtered['marca'] == marca]
if modelo != "Todos":
    df_filtered = df_filtered[df_filtered['modelo'] == modelo]

# Mostrar
st.dataframe(df_filtered, use_container_width=True)
