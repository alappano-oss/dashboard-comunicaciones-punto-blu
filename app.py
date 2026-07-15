import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(page_title="Dashboard Punto Blu", layout="wide", page_icon="📊")

st.title("📊 Tablero de Rendimiento de Campañas - Punto Blu")
st.markdown("Analizá las métricas de tus envíos de forma rápida e interactiva.")
st.markdown("---")

# Carga de datos desde el archivo CSV
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("datos.csv")
        df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d-%m-%Y")
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo datos.csv: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Filtros laterales en barra de navegación
    st.sidebar.header("Filtros de Campaña")
    
    # Filtro de fecha
    min_date = df["Fecha"].min()
    max_date = df["Fecha"].max()
    start_date, end_date = st.sidebar.date_input(
        "Rango de Fechas",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Filtro de plantillas
    todas_plantillas = df["Plantilla"].unique()
    selected_template = st.sidebar.multiselect(
        "Seleccionar Plantilla", 
        options=todas_plantillas, 
        default=todas_plantillas
    )
    
    # Aplicar filtros
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df[
        (df["Plantilla"].isin(selected_template)) & 
        (df["Fecha"] >= start_date) & 
        (df["Fecha"] <= end_date)
    ]
    
    # Métricas clave (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    
    total_enviados = filtered_df["Enviados"].sum()
    total_entregados = filtered_df["Entregados"].sum()
    total_leidos = filtered_df["Leidos"].sum()
    total_clicks = filtered_df["Clicks"].sum()
    total_respuestas = filtered_df["Respuestas"].sum()
    
    tasa_lectura = (total_leidos / total_entregados * 100) if total_entregados > 0 else 0
    tasa_clics = (total_clicks / total_leidos * 100) if total_leidos > 0 else 0
    
    col1.metric("Total Enviados", f"{total_enviados:,}")
    col2.metric("Total Entregados", f"{total_entregados:,}")
    col3.metric("Tasa de Lectura", f"{tasa_lectura:.1f}%")
    col4.metric("Tasa de Clics (CTR)", f"{tasa_clics:.1f}%")
    
    st.markdown("---")
    
    # Visualizaciones
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("Embudo de Conversión Consolidado")
        fig_funnel = go.Figure(go.Funnel(
            y=["Enviados", "Entregados", "Leídos", "Clicks", "Respuestas"],
            x=[total_enviados, total_entregados, total_leidos, total_clicks, total_respuestas],
            textinfo="value+percent initial"
        ))
        fig_funnel.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_funnel, use_container_width=True)
        
    with col_right:
        st.subheader("Detalle por Campaña")
        st.dataframe(
            filtered_df.style.format({
                "Enviados": "{:,}",
                "Entregados": "{:,}",
                "Leidos": "{:,}",
                "Clicks": "{:,}",
                "Respuestas": "{:,}"
            }), 
            use_container_width=True,
            hide_index=True
        )
else:
    st.warning("No se encontraron datos disponibles para mostrar.")
