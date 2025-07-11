import streamlit as st
import pandas as pd

# Configurar página
st.set_page_config(page_title="Stock de Repuestos", layout="wide")
st.title("📦 Stock de Repuestos")
st.caption("Postventa")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("DATA_PILOTO_PV.csv", sep='|', encoding='utf-8', engine='python', on_bad_lines='skip')

df = load_data()

# Filtro: Solo repuestos con stock
df = df[df['Tiene Stock'].str.upper() == "SI"]

# Crear columnas para filtros
col1, col2, col3, col4 = st.columns(4)
col5, col6, col7 = st.columns(3)

with col1:
    placa = st.selectbox("Placa", ["All"] + sorted(df['placa'].dropna().unique()), placeholder="Ejm: ABC123")
with col2:
    categoria = st.selectbox("Categoría", ["All"] + sorted(df['categoría'].dropna().unique()))
with col3:
    grupo = st.selectbox("Grupo de Repuesto", ["All"] + sorted(df['grupo de repuesto'].dropna().unique()))
with col4:
    sucursal = st.selectbox("Sucursal", ["All"] + sorted(df['sucursal (almacen)'].dropna().unique()))
with col5:
    tipo_vehiculo = st.selectbox("Tipo vehículo", ["All"] + sorted(df['tipo de vehículo'].dropna().unique()))
with col6:
    marca = st.selectbox("Marca", ["All"] + sorted(df['marca'].dropna().unique()))
with col7:
    modelo = st.selectbox("Modelo", ["All"] + sorted(df['modelo'].dropna().unique()))
with st.expander("🔎 Filtros activos"):
    st.write("Puedes usar los menús desplegables para filtrar por cada campo.")

# Aplicar filtros seleccionados
df_filtered = df.copy()
if placa != "All":
    df_filtered = df_filtered[df_filtered['placa'] == placa]
if categoria != "All":
    df_filtered = df_filtered[df_filtered['categoría'] == categoria]
if grupo != "All":
    df_filtered = df_filtered[df_filtered['grupo de repuesto'] == grupo]
if sucursal != "All":
    df_filtered = df_filtered[df_filtered['sucursal (almacen)'] == sucursal]
if tipo_vehiculo != "All":
    df_filtered = df_filtered[df_filtered['tipo de vehículo'] == tipo_vehiculo]
if marca != "All":
    df_filtered = df_filtered[df_filtered['marca'] == marca]
if modelo != "All":
    df_filtered = df_filtered[df_filtered['modelo'] == modelo]

# Mostrar tabla
st.subheader("📊 Stock de Repuestos")
st.dataframe(df_filtered, use_container_width=True)
