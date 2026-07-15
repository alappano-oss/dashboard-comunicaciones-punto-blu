import streamlit as st  
import pandas as pd  
import plotly.express as px  
import plotly.graph_objects as go  
  
st.set_page_config(page_title="Dashboard Punto Blu", layout="wide")  

# ==============================================================================
# 1. ESTILOS PERSONALIZADOS (Paleta de colores Punto Blu)
# ==============================================================================
st.markdown("""
    <style>
    /* Fondo del sidebar en Azul Oscuro */
    [data-testid="stSidebar"] {
        background-color: #024099;
    }
    /* Textos del sidebar en Blanco */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    /* Estilo de los títulos de las métricas en Azul Oscuro */
    div[data-testid="stMetricLabel"] {
        color: #024099 !important;
        font-weight: bold;
    }
    /* Estilo de los valores numéricos de las métricas en Azul Eléctrico */
    div[data-testid="stMetricValue"] {
        color: #0760f7 !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Tablero de Rendimiento de Campañas - Punto Blu")  
st.write("---")

# ==============================================================================
# 2. CARGA, LIMPIEZA Y CLASIFICACIÓN DE DATOS
# ==============================================================================
@st.cache_data  
def load_data():  
    data = {  
        "Fecha": ["01-04-2026", "06-04-2026", "06-04-2026", "08-04-2026", "08-04-2026", "14-04-2026", "16-04-2026", "20-04-2026", "21-04-2026", "22-04-2026", "27-04-2026", "27-04-2026", "04-05-2026", "07-05-2026", "19-05-2026", "01-07-2026", "02-07-2026", "03-07-2026", "06-07-2026", "07-07-2026", "08-07-2026", "10-07-2026"],  
        "Plantilla": ["lineablanca b", "Lineablanca_b2", "televisores 12si", "lineablanca a", "televisoresb12si", "electro_cocina", "celulares 12si", "accion_paracocina260420", "accion 9si260421", "sommiers24si", "linea hogar260427", "teles_celus260427", "tv mayo260504", "calefa 260507", "sucus 260519", "alto_sommiers", "alto_herramientas", "minicuotas_celulares", "flash_tromen", "Linea_blanca", "faustina", "Flash Smart"],  
        "Enviados": [935, 1100, 645, 533, 874, 747, 228, 378, 1700, 378, 1600, 1300, 1800, 935, 839, 791, 775, 797, 796, 795, 797, 792],  
        "Entregados": [908, 1100, 629, 526, 847, 734, 214, 364, 1700, 363, 1500, 1200, 1700, 912, 809, 716, 708, 732, 730, 731, 701, 714],  
        "Leidos": [752, 903, 518, 430, 691, 625, 157, 298, 1400, 279, 1200, 974, 1300, 742, 641, 603, 555, 620, 611, 596, 589, 571],  
        "Respuestas": [112, 139, 93, 119, 120, 114, 22, 27, 146, 26, 104, 120, 126, 88, 13, 98, 87, 212, 141, 93, 116, 78],  
        "Clicks": [108, 143, 98, 128, 110, 123, 17, 22, 114, 10, 81, 102, 88, 82, 0, 98, 86, 212, 141, 93, 114, 78], 
        "Conversión %": ["2.0%", "1.5%", "0.6%", "1.1%", "0.2%", "1.2%", "0.0%", "0.8%", "0.9%", "0.3%", "0.2%", "1.3%", "0.7%", "0.5%", "0.0%", "-", "-", "-", "-", "-", "-", "-"]
    }  
    df = pd.DataFrame(data)  
    df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d-%m-%Y", errors="coerce")  
    
    # Limpieza de conversión
    df["Conversión %"] = df["Conversión %"].replace("-", None)
    df["Conversión %"] = df["Conversión %"].str.rstrip('%').astype('float') / 100.0
    
    # Clasificación automática por Categorías
    def clasificar_categoria(nombre):
        nombre_lower = str(nombre).lower()
        if "tele" in nombre_lower or "tv" in nombre_lower or "smart" in nombre_lower:
            return "TV y Pantallas"
        elif "lineablanca" in nombre_lower or "cocina" in nombre_lower or "hogar" in nombre_lower:
            return "Línea Blanca / Hogar"
        elif "celu" in nombre_lower:
            return "Celulares"
        elif "sommier" in nombre_lower:
            return "Sommiers"
        elif "calefa" in nombre_lower:
            return "Climatización"
        else:
            return "Otros / Genéricos"
            
    df["Categoría"] = df["Plantilla"].apply(clasificar_categoria)
    return df  
  
df = load_data()  
  
# ==============================================================================
# 3. FILTROS LATERALES (Sidebar)
# ==============================================================================
st.sidebar.header("🔍 Filtros de Campaña")  
selected_template = st.sidebar.multiselect(
    "Seleccionar Plantilla", 
    options=df["Plantilla"].unique(), 
    default=df["Plantilla"].unique()
)  
filtered_df = df[df["Plantilla"].isin(selected_template)]  

st.sidebar.markdown("---")
st.sidebar.header("Filtros de Conversión")
filtrar_conversiones = st.sidebar.checkbox(
    "Mostrar solo campañas con datos de Conversión", 
    value=False
)

if filtrar_conversiones:
    filtered_df = filtered_df[filtered_df["Conversión %"].notna()]
  
# ==============================================================================
# 4. KPIs PRINCIPALES DINÁMICOS
# ==============================================================================
col1, col2, col3, col4 = st.columns(4)  

# Identificar campañas que tienen datos de conversiones
campanas_con_conversion = filtered_df[filtered_df["Conversión %"].notna()]

if len(campanas_con_conversion) > 0:
    # Promedio ponderado de la conversión de las campañas seleccionadas que tienen datos
    conversion_promedio = campanas_con_conversion["Conversión %"].mean() * 100
    label_conversion = "Conversión Promedio"
else:
    conversion_promedio = 0.0
    label_conversion = "Conversión (Sin datos)"

col1.metric("Total Enviados", f"{filtered_df['Enviados'].sum():,}")  
col2.metric("Total Entregados", f"{filtered_df['Entregados'].sum():,}")  
col3.metric("Tasa de Lectura", f"{(filtered_df['Leidos'].sum() / filtered_df['Entregados'].sum() * 100):.1f}%")  
col4.metric(label_conversion, f"{conversion_promedio:.1f}%")  

st.write("---")

# ==============================================================================
# 5. BLOQUE DE GRÁFICOS PRINCIPALES (Embudo y Categorías)
# ==============================================================================
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Embudo de Conversión Consolidado")  
    etapas = ["Enviados", "Entregados", "Leídos", "Clicks", "Respuestas"]
    valores = [
        filtered_df["Enviados"].sum(), 
        filtered_df["Entregados"].sum(), 
        filtered_df["Leidos"].sum(), 
        filtered_df["Clicks"].sum(), 
        filtered_df["Respuestas"].sum()
    ]  

    if len(campanas_con_conversion) > 0:
        # Estimación de ventas reales (Enviados * % de Conversión)
        ventas_reales = (campanas_con_conversion["Enviados"] * campanas_con_conversion["Conversión %"]).sum()
        etapas.append("Conversión (Venta)")
        valores.append(int(ventas_reales))

    # Gráfico con degradado de colores de marca
    fig_funnel = go.Figure(go.Funnel(  
        y=etapas,  
        x=valores,
        marker={"color": ["#024099", "#044cb8", "#0760f7", "#3a82f9", "#70a4fc", "#FBBA00"]},
        textinfo="value+percent initial"
    ))  
    fig_funnel.update_layout(height=380, margin=dict(l=20, r=20, t=10, b=10))
    st.plotly_chart(fig_funnel, use_container_width=True)

with col_graf2:
    st.subheader("Tasa de Respuesta por Categoría")
    # Agrupación y cálculo por categorías de producto
    df_cat = filtered_df.groupby("Categoría").agg({
        "Leidos": "sum",
        "Respuestas": "sum"
    }).reset_index()
    
    # Previene división por cero
    df_cat["Tasa Respuesta %"] = df_cat.apply(
        lambda r: (r["Respuestas"] / r["Leidos"] * 100) if r["Leidos"] > 0 else 0, axis=1
    )
    
    fig_bar_cat = px.bar(
        df_cat, 
        x="Categoría", 
        y="Tasa Respuesta %", 
        text_auto='.1f',
        color_discrete_sequence=["#0760f7"] # Azul Eléctrico
    )
    fig_bar_cat.update_layout(
        height=380, 
        margin=dict(l=20, r=20, t=10, b=10),
        xaxis_title="Categorías",
        yaxis_title="% Respuestas / Leídos"
    )
    st.plotly_chart(fig_bar_cat, use_container_width=True)

st.write("---")

# ==============================================================================
# 6. BLOQUE DE COMPARACIÓN POR PLANTILLA Y TENDENCIA TEMPORAL (Opción A y Línea de Tiempo)
# ==============================================================================
col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    st.subheader("Clics vs. Respuestas por Plantilla")
    
    # Ordenamos el DataFrame por Respuestas (ascendente para que el mayor quede arriba en barras horizontales)
    df_sorted = filtered_df.sort_values(by="Respuestas", ascending=True)
    
    # Construimos el gráfico de barras agrupadas horizontales usando Plotly Graph Objects
    fig_grouped_bar = go.Figure()
    
    # Agregamos la barra para Clics (Azul Eléctrico)
    fig_grouped_bar.add_trace(go.Bar(
        y=df_sorted["Plantilla"],
        x=df_sorted["Clicks"],
        name="Clics",
        orientation="h",
        marker_color="#0760f7"
    ))
    
    # Agregamos la barra para Respuestas (Amarillo de marca)
    fig_grouped_bar.add_trace(go.Bar(
        y=df_sorted["Plantilla"],
        x=df_sorted["Respuestas"],
        name="Respuestas",
        orientation="h",
        marker_color="#FBBA00"
    ))
    
    fig_grouped_bar.update_layout(
        barmode="group", # Agrupadas juntas
        height=350,
        margin=dict(l=20, r=20, t=10, b=10),
        xaxis_title="Cantidad de Interacciones",
        yaxis_title="Plantillas",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_grouped_bar, use_container_width=True)

with col_graf4:
    st.subheader("Evolución Temporal del Rendimiento")
    df_timeline = filtered_df.sort_values(by="Fecha")
    
    fig_line = px.line(
        df_timeline, 
        x="Fecha", 
        y=["Leidos", "Clicks", "Respuestas"],
        color_discrete_map={
            "Leidos": "#024099",      # Azul Oscuro
            "Clicks": "#0760f7",      # Azul Eléctrico
            "Respuestas": "#FBBA00"   # Amarillo
        }
    )
    fig_line.update_layout(
        height=350, 
        margin=dict(l=20, r=20, t=10, b=10),
        xaxis_title="Línea de Tiempo",
        yaxis_title="Cantidad de Eventos"
    )
    st.plotly_chart(fig_line, use_container_width=True)
