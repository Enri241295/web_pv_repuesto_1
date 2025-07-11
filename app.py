import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stock de Repuestos", page_icon="📦", layout="wide")
st.title("📦 Stock de Repuestos")
st.caption("Postventa")

@st.cache_data
def load_data():
    df = pd.read_csv("DATA_PILOTO_PV.csv", sep='|', encoding='utf-8', engine='python', on_bad_lines='skip')
    
    # Crear campo Tiene Stock
    stock_cols = [col for col in df.columns if 'STOCK' in col.upper()]
    df["Tiene Stock"] = df[stock_cols].sum(axis=1).apply(lambda x: "SI" if x > 0 else "NO")
    
    # Mapear centro a nombre de sucursal
    df["Sucursal"] = df["CENTRO"].replace({
        3001: "Sucursal Javier Prado",
        3101: "Sucursal Canadá"
    })

    # Renombrar columnas
    df = df.rename(columns={
        "cliente parque vehicular": "Cliente",
        "chasis": "Chasis",
        "placa": "Placa",
        "año de fabricación": "Año de fabricación",
        "familia": "Familia",
        "tipo vehiculo": "Tipo de Vehículo",
        "marca": "Marca",
        "modelo": "Modelo",
        "categoría": "Categoría",
        "grupo de repuesto": "Grupo de Repuesto",
        "cod. repuesto": "Cod. Repuesto",
        "repuesto": "Repuesto"
    })

    # Eliminar columnas no necesarias
    df = df.drop(columns=["CENTRO", "vehiculo divemotor", "vendido por divemotor"], errors='ignore')
    return df

df = load_data()

# Filtros
st.markdown("### 🔎 Filtros")

col1, col2, col3 = st.columns(3)
with col1:
    marca = st.selectbox("Marca", ["Todos"] + sorted(df["Marca"].dropna().unique()))
    tipo = st.selectbox("Tipo de Vehículo", ["Todos"] + sorted(df["Tipo de Vehículo"].dropna().unique()))
with col2:
    modelo = st.selectbox("Modelo", ["Todos"] + sorted(df["Modelo"].dropna().unique()))
    categoria = st.selectbox("Categoría", ["Todos"] + sorted(df["Categoría"].dropna().unique()))
with col3:
    sucursal = st.selectbox("Sucursal", ["Todos"] + sorted(df["Sucursal"].dropna().unique()))
    grupo = st.selectbox("Grupo de Repuesto", ["Todos"] + sorted(df["Grupo de Repuesto"].dropna().unique()))

col4, col5 = st.columns(2)
with col4:
    repuesto = st.selectbox("Repuesto", ["Todos"] + sorted(df["Repuesto"].dropna().unique()))
with col5:
    placa = st.selectbox("Placa", ["Todos"] + sorted(df["Placa"].dropna().unique()))

# Aplicar filtros
df_filtered = df.copy()
if marca != "Todos":
    df_filtered = df_filtered[df_filtered["Marca"] == marca]
if tipo != "Todos":
    df_filtered = df_filtered[df_filtered["Tipo de Vehículo"] == tipo]
if modelo != "Todos":
    df_filtered = df_filtered[df_filtered["Modelo"] == modelo]
if categoria != "Todos":
    df_filtered = df_filtered[df_filtered["Categoría"] == categoria]
if sucursal != "Todos":
    df_filtered = df_filtered[df_filtered["Sucursal"] == sucursal]
if grupo != "Todos":
    df_filtered = df_filtered[df_filtered["Grupo de Repuesto"] == grupo]
if repuesto != "Todos":
    df_filtered = df_filtered[df_filtered["Repuesto"] == repuesto]
if placa != "Todos":
    df_filtered = df_filtered[df_filtered["Placa"] == placa]

# Mostrar resultado
st.markdown("### 🧾 Resultado de Stock")
columnas_finales = [
    "Cliente", "Chasis", "Placa", "Año de fabricación", "Familia",
    "Tipo de Vehículo", "Marca", "Modelo", "Categoría", "Grupo de Repuesto",
    "Sucursal", "Cod. Repuesto", "Repuesto", "Tiene Stock"
]
st.dataframe(df_filtered[columnas_finales], use_container_width=True)
