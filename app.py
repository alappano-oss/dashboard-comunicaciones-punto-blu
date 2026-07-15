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
# 2. CARGA, LIMPIEZA Y CLASIFICACIÓN DE DATOS (BD COMPLETA 2026)
# ==============================================================================
@st.cache_data  
def load_data():  
    data = {  
        "Fecha": [
            # ABRIL
            "01-04-2026", "01-04-2026", "08-04-2026", "06-04-2026", "06-04-2026", 
            "14-04-2026", "16-04-2026", "22-04-2026", "20-04-2026", "21-04-2026", 
            "27-04-2026", "27-04-2026",
            # MAYO
            "04-05-2026", "07-05-2026", "19-05-2026",
            # JUNIO
            "02-06-2026", "02-06-2026", "09-06-2026", "09-06-2026", "16-06-2026", 
            "16-06-2026", "17-06-2026", "17-06-2026", "22-06-2026", "23-06-2026", 
            "23-06-2026", "24-06-2026", "24-06-2026",
            # JULIO
            "01-07-2026", "02-07-2026", "03-07-2026", "06-07-2026", "07-07-2026", 
            "08-07-2026", "10-07-2026"
        ],  
        "Plantilla": [
            # ABRIL
            "lineablanca_b", "lineablanca_a", "televisoresb12si", "lineablanca_b2", "televisores_12si", 
            "electro_cocina", "celulares_12si", "sommiers24si", "accion_paracocina260420", "accion_9si260421", 
            "linea_hogar260427", "teles_celus260427",
            # MAYO
            "tv_mayo260504", "calefa_260507", "sucus_260519",
            # JUNIO
            "dia_del_padre_disp_bajo_260602", "generico_disp_alto_260602", "dia_del_padre_disp_bajo_260609", 
            "generico_disp_alto_megaclub_260609", "blu_generico_disp_alto_megaclub_260616", "blu_generico_disp_bajo_megaclub_260616", 
            "blu_generico_disp_alto_megaclub_260617", "blu_generico_disp_bajo_megaclub_260617", "blu_generico_disponible_alto_diferido_260622", 
            "blu_generico_disp_bajo_diferido_260623", "blu_generico_disponible_alto_diferido_260623", "blu_generico_disponible_alto_diferido_260624", 
            "blu_generico_disp_bajo_diferido_260624",
            # JULIO
            "blu_generico_disponible_alto_sommiers_260701", "blu_generico_disponible_alto_herramientas_260702", 
            "minicuotas_celulares_260703", "flash_tromen_260706", "linea_blanca_260707", 
            "faustina_260708", "Flash Smart 260710"
        ],  
        "Enviados": [
            # ABRIL
            935, 533, 874, 1100, 645, 747, 228, 378, 378, 1700, 1600, 1300,
            # MAYO
            1800, 935, 839,
            # JUNIO
            751, 261, 516, 267, 121, 123, 377, 379, 157, 234, 36, 1980, 1890,
            # JULIO
            791, 775, 797, 796, 795, 797, 792
        ],  
        "Entregados": [
            # ABRIL
            908, 526, 847, 1100, 629, 734, 214, 363, 364, 1700, 1500, 1200,
            # MAYO
            1700, 912, 809,
            # JUNIO
            738, 252, 506, 258, 110, 114, 327, 330, 139, 209, 32, 1750, 1700,
            # JULIO
            716, 708, 732, 730, 731, 701, 714
        ],  
        "Leidos": [
            # ABRIL
            752, 430, 691, 903, 518, 625, 157, 279, 298, 1400, 1200, 974,
            # MAYO
            1300, 742, 641,
            # JUNIO
            588, 210, 399, 213, 93, 105, 267, 294, 119, 182, 24, 1470, 1380,
            # JULIO
            603, 555, 620, 611, 596, 589, 571
        ],  
        "Respuestas": [
            # ABRIL
            112, 119, 120, 139, 93, 114, 22, 26, 27, 146, 104, 120,
            # MAYO
            126, 88, 13,
            # JUNIO
            165, 42, 88, 58, 12, 18, 56, 98, 13, 36, 5, 181, 267,
            # JULIO
            98, 87, 212, 141, 93, 116, 78
        ],  
        "Clicks": [
            # ABRIL
            108, 128, 110, 143, 98, 123, 17, 10, 22, 114, 81, 102,
            # MAYO
            88, 82, 0,
            # JUNIO
            187, 46, 97, 52, 0, 0, 56, 98, 13, 36, 5, 181, 267,
            # JULIO
            98, 86, 212, 141, 93, 114, 78
        ],
        "Conversión %": [
            # ABRIL
            "2.0%", "1.1%", "0.1%", "1.5%", "0.6%", "1.2%", "0.0%", "0.3%", "0.8%", "0.9%", "0.2%", "1.2%",
            # MAYO
            "0.7%", "0.5%", "0.0%",
            # JUNIO
            "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-",
            # JULIO
            "-", "-", "-", "-", "-", "-", "-"
        ]
    }  
    df = pd.DataFrame(data)  
    df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d-%m-%Y", errors="coerce")  
    
    # Limpieza de conversión
    df["Conversión %"] = df["Conversión %"].replace("-", None)
    df["Conversión %"] = df["Conversión %"].str.rstrip('%').astype('float') / 100.0
    
    # Agregamos columnas auxiliares para filtrar por Año, Mes y Nombre del Mes
    df["Año"] = df["Fecha"].dt.year
    df["Mes_Num"] = df["Fecha"].dt.month
    
    # Diccionario en español para traducir nombres de meses
    meses_es = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    df["Mes"] = df["Mes_Num"].map(meses_es)
    
    # Clasificación por Categorías
    def clasificar_categoria(nombre):
        nombre_lower = str(nombre).lower()
        if "tele" in nombre_lower or "tv" in nombre_lower or "smart" in nombre_lower:
            return "TV y Pantallas"
        elif "lineablanca" in nombre_lower or "cocina" in nombre_lower or "hogar" in nombre_lower or "tromen" in nombre_lower:
            return "Línea Blanca / Hogar"
        elif "celu" in nombre_lower:
            return "Celulares"
        elif "sommier" in nombre_lower:
            return "Sommiers"
        elif "calefa" in nombre_lower:
            return "Climatización"
        elif "padre" in nombre_lower:
            return "Día del Padre"
        elif "herramientas" in nombre_lower:
            return "Herramientas"
        else:
            return "Otros / Genéricos"
            
    df["Categoría"] = df["Plantilla"].apply(clasificar_categoria)
    return df  
  
df = load_data()  
  
# ==============================================================================
# 3. FILTROS LATERALES TEMPORALES Y DE PLANTILLAS (Sidebar)
# ==============================================================================
st.sidebar.header("Filtros Temporales")

# Filtro 1: Año (Multiselección)
años_disponibles = sorted(df["Año"].dropna().unique())
selected_years = st.sidebar.multiselect(
    "Seleccionar Año", 
    options=años_disponibles, 
    default=años_disponibles
)

# Filtro 2: Mes (Multiselección - Sensible al Año seleccionado)
df_filtered_temp = df[df["Año"].isin(selected_years)]
meses_disponibles = df_filtered_temp.sort_values("Mes_Num")["Mes"].unique()

selected_months = st.sidebar.multiselect(
    "Seleccionar Mes", 
    options=meses_disponibles, 
    default=meses_disponibles
)

# Filtro 3: Rango de Fecha exacto (Date Input)
if not df_filtered_temp.empty:
    min_date = df_filtered_temp["Fecha"].min().to_pydatetime()
    max_date = df_filtered_temp["Fecha"].max().to_pydatetime()
    
    selected_dates = st.sidebar.date_input(
        "Rango de Fechas Específico",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
else:
    selected_dates = []

# --- APLICACIÓN DE FILTROS TEMPORALES AL DATAFRAME BASE ---
filtered_df = df[df["Año"].isin(selected_years)]
if len(selected_months) > 0:
    filtered_df = filtered_df[filtered_df["Mes"].isin(selected_months)]

if len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered_df = filtered_df[
        (filtered_df["Fecha"].dt.date >= start_date) & 
        (filtered_df["Fecha"].dt.date <= end_date)
    ]

# --- FILTROS DE PLANTILLAS Y CONVERSIÓN ---
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filtros de Campaña")  

plantillas_disponibles = sorted(filtered_df["Plantilla"].unique())
selected_template = st.sidebar.multiselect(
    "Seleccionar Plantilla", 
    options=plantillas_disponibles, 
    default=plantillas_disponibles
)  

# Aplicamos filtro de plantillas seleccionadas
filtered_df = filtered_df[filtered_df["Plantilla"].isin(selected_template)]  

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
# Verificación si quedan datos tras aplicar todos los filtros cruzados
if not filtered_df.empty:
    col1, col2, col3, col4 = st.columns(4)  

    campanas_con_conversion = filtered_df[filtered_df["Conversión %"].notna()]

    if len(campanas_con_conversion) > 0:
        conversion_promedio = campanas_con_conversion["Conversión %"].mean() * 100
        label_conversion = "Conversión Promedio"
    else:
        conversion_promedio = 0.0
        label_conversion = "Conversión (Sin datos)"

    total_entregados = filtered_df['Entregados'].sum()
    tasa_lectura = (filtered_df['Leidos'].sum() / total_entregados * 100) if total_entregados > 0 else 0.0

    col1.metric("Total Enviados", f"{filtered_df['Enviados'].sum():,}")  
    col2.metric("Total Entregados", f"{total_entregados:,}")  
    col3.metric("Tasa de Lectura", f"{tasa_lectura:.1f}%")  
    col4.metric(label_conversion, f"{conversion_promedio:.1f}%")  
else:
    st.warning("No hay datos que coincidan con la combinación de filtros seleccionados en el sidebar.")
    st.stop() # Frena la ejecución visual si no hay datos disponibles

st.write("---")

# ==============================================================================
# 5. BLOQUE DE GRÁFICOS PRINCIPALES (Embudo y Categorías)
# ==============================================================================
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Embudo de Conversión")  
    etapas = ["Enviados", "Entregados", "Leídos", "Clicks", "Respuestas"]
    valores = [
        filtered_df["Enviados"].sum(), 
        filtered_df["Entregados"].sum(), 
        filtered_df["Leidos"].sum(), 
        filtered_df["Clicks"].sum(), 
        filtered_df["Respuestas"].sum()
    ]  

    if len(campanas_con_conversion) > 0:
        ventas_reales = (campanas_con_conversion["Enviados"] * campanas_con_conversion["Conversión %"]).sum()
        etapas.append("Conversión (Venta)")
        valores.append(int(ventas_reales))

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
    df_cat = filtered_df.groupby("Categoría").agg({
        "Leidos": "sum",
        "Respuestas": "sum"
    }).reset_index()
    
    df_cat["Tasa Respuesta %"] = df_cat.apply(
        lambda r: (r["Respuestas"] / r["Leidos"] * 100) if r["Leidos"] > 0 else 0, axis=1
    )
    
    fig_bar_cat = px.bar(
        df_cat, 
        x="Categoría", 
        y="Tasa Respuesta %", 
        text_auto='.1f',
        color_discrete_sequence=["#0760f7"]
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
# 6. BLOQUE DE COMPARACIÓN POR PLANTILLA Y TENDENCIA TEMPORAL
# ==============================================================================
col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    st.subheader("Clics vs. Respuestas por Plantilla")
    
    df_sorted = filtered_df.sort_values(by="Respuestas", ascending=True)
    
    fig_grouped_bar = go.Figure()
    
    fig_grouped_bar.add_trace(go.Bar(
        y=df_sorted["Plantilla"],
        x=df_sorted["Clicks"],
        name="Clics",
        orientation="h",
        marker_color="#0760f7"
    ))
    
    fig_grouped_bar.add_trace(go.Bar(
        y=df_sorted["Plantilla"],
        x=df_sorted["Respuestas"],
        name="Respuestas",
        orientation="h",
        marker_color="#FBBA00"
    ))
    
    # Ajustamos la altura dinámicamente según la cantidad de campañas para que no se amontonen
    altura_dinamica = max(350, len(df_sorted) * 20)
    
    fig_grouped_bar.update_layout(
        barmode="group",
        height=altura_dinamica,
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
            "Leidos": "#024099",
            "Clicks": "#0760f7",
            "Respuestas": "#FBBA00"
        }
    )
    fig_line.update_layout(
        height=500, 
        margin=dict(l=20, r=20, t=10, b=10),
        xaxis_title="Línea de Tiempo",
        yaxis_title="Cantidad de Eventos"
    )
    st.plotly_chart(fig_line, use_container_width=True)
