import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stock de Repuestos", layout="wide")
st.title("📦 Stock de Repuestos")
st.caption("Postventa")

@st.cache_data
def load_data():
    return pd.read_csv("DATA_PILOTO_PV.csv", sep='|', encoding='utf-8', engine='python', on_bad_lines='skip')

df = load_data()

# Columnas de stock
columnas_stock = [
    'STOCK_IMPORTER', 'STOCK_DEALER', 'STOCK_TOTAL',
    'STOCK_GRANDES_CLIENTES', 'STOCK_OTROS_ALMACENES', 'STOCK_TRANSITO_INTERNO'
]

# Asegurar que los campos de stock sean numéricos
df[columnas_stock] = df[columnas_stock].fillna(0).astype(float)

# Crear campo FLG_STOCK
df["FLG_STOCK"] = df[columnas_stock].gt(0).any(axis=1).map({True: "SI", False: "NO"})

# Crear campo Sucursal
df["Sucursal"] = df["CENTRO"].map({3001: "Sucursal Javier Prado", 3101: "Sucursal Canadá"})

# Eliminar columnas innecesarias
columnas_ocultar = ["CENTRO", "vehiculo divemotor", "vendido por divemotor"]
df = df.drop(columns=[col for col in columnas_ocultar if col in df.columns])

# Filtros
col1, col2, col3 = st.columns(3)
with col1:
    marca = st.selectbox("Marca", ["Todos"] + sorted(df['marca'].dropna().unique()))
with col2:
    modelo = st.selectbox("Modelo", ["Todos"] + sorted(df['modelo'].dropna().unique()))
with col3:
    tipo = st.selectbox("Tipo Vehículo", ["Todos"] + sorted(df['tipovehiculo'].dropna().unique()))

# Aplicar filtros
df_filtered = df.copy()
if marca != "Todos":
    df_filtered = df_filtered[df_filtered['marca'] == marca]
if modelo != "Todos":
    df_filtered = df_filtered[df_filtered['modelo'] == modelo]
if tipo != "Todos":
    df_filtered = df_filtered[df_filtered['tipovehiculo'] == tipo]

# Eliminar columnas de stock (para que no se muestren)
df_filtered = df_filtered.drop(columns=columnas_stock)

# Mostrar
st.subheader("📋 Resultado de Stock")
st.dataframe(df_filtered, use_container_width=True)

