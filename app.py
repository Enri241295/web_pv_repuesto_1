import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stock de Repuestos", layout="wide")
st.title("📦 Stock de Repuestos")
st.caption("Postventa")

@st.cache_data
def load_data():
    return pd.read_csv("DATA_PILOTO_PV.csv", sep='|', encoding='utf-8', engine='python', on_bad_lines='skip')

df = load_data()

# Detectar columnas de stock
columnas_stock = [col for col in df.columns if "STOCK" in col.upper()]
df[columnas_stock] = df[columnas_stock].fillna(0).astype(float)

# Crear campo Tiene Stock
df["Tiene Stock"] = df[columnas_stock].gt(0).any(axis=1).map({True: "SI", False: "NO"})

# Crear campo Sucursal
df["Sucursal"] = df["CENTRO"].map({3001: "Sucursal Javier Prado", 3101: "Sucursal Canadá"})

# Renombrar columnas
df = df.rename(columns={
    "cliente parque vehicular": "Cliente",
    "vin": "Chasis",
    "placa": "Placa",
    "anofabricacion": "Año de fabricación",
    "familia": "Familia",
    "tipo": "Tipo de Vehículo",
    "marca": "Marca",
    "modelo": "Modelo",
    "categoria": "Categoría",
    "grupo repuesto": "Grupo de Repuesto",
    "codigo_catalogo": "Cod. Repuesto",
    "repuesto": "Repuesto"
})

# Seleccionar y ordenar columnas a mostrar
columnas_finales = [
    "Cliente", "Chasis", "Placa", "Año de fabricación", "Familia", "Tipo de Vehículo",
    "Marca", "Modelo", "Categoría", "Grupo de Repuesto", "Sucursal",
    "Cod. Repuesto", "Repuesto", "Tiene Stock"
]

# Filtrar solo columnas que existan
columnas_finales = [col for col in columnas_finales if col in df.columns]
df_mostrar = df[columnas_finales]

# Filtros
col1, col2, col3 = st.columns(3)
with col1:
    marca = st.selectbox("Marca", ["Todos"] + sorted(df_mostrar['Marca'].dropna().unique()))
with col2:
    modelo = st.selectbox("Modelo", ["Todos"] + sorted(df_mostrar['Modelo'].dropna().unique()))
with col3:
    sucursal = st.selectbox("Sucursal", ["Todos"] + sorted(df_mostrar['Sucursal'].dropna().unique()))

# Aplicar filtros
if marca != "Todos":
    df_mostrar = df_mostrar[df_mostrar['Marca'] == marca]
if modelo != "Todos":
    df_mostrar = df_mostrar[df_mostrar['Modelo'] == modelo]
if sucursal != "Todos":
    df_mostrar = df_mostrar[df_mostrar['Sucursal'] == sucursal]

# Mostrar resultados
st.subheader("📋 Resultado de Stock")
st.dataframe(df_mostrar, use_container_width=True)
