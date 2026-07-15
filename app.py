import streamlit as st  
import pandas as pd  
import plotly.express as px  
import plotly.graph_objects as go  
  
st.set_page_config(page_title="Dashboard Punto Blu", layout="wide")  

# Estilos CSS para inyectar tus colores en la interfaz de Streamlit
st.markdown("""
    <style>
    /* Cambiar color de fondo del sidebar */
    [data-testid="stSidebar"] {
        background-color: #024099;
    }
    /* Cambiar color de los textos del sidebar a blanco */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    /* Estilos para las tarjetas de métricas */
    div[data-testid="stMetricValue"] {
        color: #0760f7 !important;
        font-weight: bold;
    }
    div[data-testid="stMetricLabel"] {
        color: #024099 !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Tablero de Rendimiento de Campañas - Punto Blu")  
  
# Carga de datos
@st.cache_data  
def load_data():  
    data = {  
        "Fecha": ["01-04-2026", "06-04-2026", "06-04-2026", "08-04-2026", "08-04-2026", "14-04-2026", "16-04-2026", "20-04-2026", "21-04-2026", "22-04-2026", "27-04-2026", "27-04-2026", "04-05-2026", "07-05-2026", "01-07-2026", "02-07-2026", "03-07-2026", "06-07-2026", "07-07-2026", "08-07-2026", "10-07-2026"],  
        "Plantilla": ["lineablanca b", "Lineablanca_b2", "televisores 12si", "lineablanca a", "televisoresb12si", "electro_cocina", "celulares 12si", "accion_paracocina260420", "accion 9si260421", "sommiers24si", "linea hogar260427", "teles_celus260427", "tv mayo260504", "calefa 260507", "alto_sommiers", "alto_herramientas", "minicuotas_celulares", "flash_tromen", "Linea_blanca", "faustina", "Flash Smart"],  
        "Enviados": [935, 1100, 645, 533, 874, 747, 228, 378, 1700, 378, 1600, 1300, 1800, 935, 791, 775, 797, 796, 795, 797, 792],  
        "Entregados": [908, 1100, 629, 526, 847, 734, 214, 364, 1700, 363, 1500, 1200, 1700, 912, 716, 708, 732, 730, 731, 701, 714],  
        "Leidos": [752, 903, 518, 430, 691, 625, 157, 298, 1400, 279, 1200, 974, 1300, 742, 603, 555, 620, 611, 596, 589, 571],  
        "Respuestas": [112, 139, 93, 119, 120, 114, 22, 27, 146, 26, 104, 120, 126, 88, 98, 87, 212, 141, 93, 116, 78],  
        "Clicks": [108, 143, 98, 128, 110, 123, 17, 22, 114, 10, 81, 102, 88, 82, 98, 86, 212, 141, 93, 114, 78]  
    }  
    df = pd.DataFrame(data)  
    df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d-%m-%Y", errors="coerce")  
    return df  
  
df = load_data()  
  
# Filtros laterales en el Sidebar
st.sidebar.header("🔍 Filtros de Campaña")  
selected_template = st.sidebar.multiselect(
    "Seleccionar Plantilla", 
    options=df["Plantilla"].unique(), 
    default=df["Plantilla"].unique()
)  
filtered_df = df[df["Plantilla"].isin(selected_template)]  
  
# KPIs Principales en tarjetas
col1, col2, col3, col4 = st.columns(4)  
col1.metric("Total Enviados", f"{filtered_df['Enviados'].sum():,}")  
col2.metric("Total Entregados", f"{filtered_df['Entregados'].sum():,}")  
col3.metric("Lectura Promedio", f"{(filtered_df['Leidos'].sum() / filtered_df['Entregados'].sum() * 100):.1f}%")  
col4.metric("Clicks / Lecturas", f"{(filtered_df['Clicks'].sum() / filtered_df['Leidos'].sum() * 100):.1f}%")  

st.write("---")

# Organización en dos columnas para gráficos
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("🎯 Embudo de Conversión Consolidado")  
    # Embudo con escala de azules (Azul Oscuro a Azul Eléctrico)
    fig_funnel = go.Figure(go.Funnel(  
        y=["Enviados", "Entregados", "Leídos", "Clicks", "Respuestas"],  
        x=[
            filtered_df["Enviados"].sum(), 
            filtered_df["Entregados"].sum(), 
            filtered_df["Leidos"].sum(), 
            filtered_df["Clicks"].sum(), 
            filtered_df["Respuestas"].sum()
        ],
        marker={"color": ["#024099", "#044cb8", "#0760f7", "#3a82f9", "#70a4fc"]},
        textinfo="value+percent initial"
    ))  
    fig_funnel.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=400)
    st.plotly_chart(fig_funnel, use_container_width=True)  

with col_graf2:
    st.subheader("⚔️ Clicks vs. Respuestas por Campaña")
    # Gráfico de barras usando Azul Eléctrico y Amarillo para contrastar acciones
    fig_compare = go.Figure()
    fig_compare.add_trace(go.Bar(
        y=filtered_df["Plantilla"],
        x=filtered_df["Clicks"],
        name="Clicks",
        orientation='h',
        marker_color='#0760f7'
    ))
    fig_compare.add_trace(go.Bar(
        y=filtered_df["Plantilla"],
        x=filtered_df["Respuestas"],
        name="Respuestas",
        orientation='h',
        marker_color='#FBBA00'
    ))
    fig_compare.update_layout(
        barmode='group',
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_compare, use_container_width=True)

st.write("---")

# Gráfico de línea temporal para ver el impacto a lo largo de los días
st.subheader("📈 Evolución Temporal del Rendimiento")
df_timeline = filtered_df.sort_values(by="Fecha")
fig_line = px.line(
    df_timeline, 
    x="Fecha", 
    y=["Leidos", "Clicks", "Respuestas"],
    labels={"value": "Cantidad de Eventos", "variable": "Métrica"},
    color_discrete_map={
        "Leidos": "#024099",      # Azul Oscuro
        "Clicks": "#0760f7",      # Azul Eléctrico
        "Respuestas": "#FBBA00"   # Amarillo
    }
)
fig_line.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_line, use_container_width=True)
