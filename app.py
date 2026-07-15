import streamlit as st  
import pandas as pd  
import plotly.express as px  
import plotly.graph_objects as go  
  
st.set_page_config(page_title="Dashboard Punto Blu", layout="wide")  
st.title("Tablero de Rendimiento de Campañas - Punto Blu")  
  
# 1. CARGA Y LIMPIEZA DE DATOS (Actualizado para procesar Conversiones)
@st.cache_data  
def load_data():  
    # Tus datos consolidados (incluyendo las filas con y sin conversiones)
    data = {  
        "Fecha": ["01-04-2026", "06-04-2026", "06-04-2026", "08-04-2026", "08-04-2026", "14-04-2026", "16-04-2026", "20-04-2026", "21-04-2026", "22-04-2026", "27-04-2026", "27-04-2026", "04-05-2026", "07-05-2026", "19-05-2026", "01-07-2026", "02-07-2026", "03-07-2026", "06-07-2026", "07-07-2026", "08-07-2026", "10-07-2026"],  
        "Plantilla": ["lineablanca b", "Lineablanca_b2", "televisores 12si", "lineablanca a", "televisoresb12si", "electro_cocina", "celulares 12si", "accion_paracocina260420", "accion 9si260421", "sommiers24si", "linea hogar260427", "teles_celus260427", "tv mayo260504", "calefa 260507", "sucus 260519", "alto_sommiers", "alto_herramientas", "minicuotas_celulares", "flash_tromen", "Linea_blanca", "faustina", "Flash Smart"],  
        "Enviados": [935, 1100, 645, 533, 874, 747, 228, 378, 1700, 378, 1600, 1300, 1800, 935, 839, 791, 775, 797, 796, 795, 797, 792],  
        "Entregados": [908, 1100, 629, 526, 847, 734, 214, 364, 1700, 363, 1500, 1200, 1700, 912, 809, 716, 708, 732, 730, 731, 701, 714],  
        "Leidos": [752, 903, 518, 430, 691, 625, 157, 298, 1400, 279, 1200, 974, 1300, 742, 641, 603, 555, 620, 611, 596, 589, 571],  
        "Respuestas": [112, 139, 93, 119, 120, 114, 22, 27, 146, 26, 104, 120, 126, 88, 13, 98, 87, 212, 141, 93, 116, 78],  
        "Clicks": [108, 143, 98, 128, 110, 123, 17, 22, 114, 10, 81, 102, 88, 82, 0, 98, 86, 212, 141, 93, 114, 78], # Reemplazado "-" por 0 en clics para consistencia
        "Conversión %": ["2.0%", "1.5%", "0.6%", "1.1%", "0.2%", "1.2%", "0.0%", "0.8%", "0.9%", "0.3%", "0.2%", "1.3%", "0.7%", "0.5%", "0.0%", "-", "-", "-", "-", "-", "-", "-"]
    }  
    df = pd.DataFrame(data)  
    df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d-%m-%Y", errors="coerce")  
    
    # Limpieza de la columna de Conversión para cálculos matemáticos
    df["Conversión %"] = df["Conversión %"].replace("-", None)
    df["Conversión %"] = df["Conversión %"].str.rstrip('%').astype('float') / 100.0
    
    return df  
  
df = load_data()  
  
# 2. FILTROS LATERALES
st.sidebar.header("Filtros de Campaña")  
selected_template = st.sidebar.multiselect("Seleccionar Plantilla", options=df["Plantilla"].unique(), default=df["Plantilla"].unique())  
filtered_df = df[df["Plantilla"].isin(selected_template)]  

st.sidebar.markdown("---")
st.sidebar.header("Filtros de Conversión")
# Checkbox para aislar rápidamente las campañas que sí tienen datos de ventas
filtrar_conversiones = st.sidebar.checkbox("Mostrar solo campañas con datos de Conversión", value=False)

if filtrar_conversiones:
    filtered_df = filtered_df[filtered_df["Conversión %"].notna()]
  
# 3. CÁLCULO DE KPIs DINÁMICOS
col1, col2, col3, col4 = st.columns(4)  

# Identificar cuáles de las campañas seleccionadas tienen registro de conversiones
campanas_con_conversion = filtered_df[filtered_df["Conversión %"].notna()]

if len(campanas_con_conversion) > 0:
    # Si hay campañas con datos, calculamos el promedio ponderado real
    conversion_promedio = campanas_con_conversion["Conversión %"].mean() * 100
    label_conversion = "Conversión Promedio"
else:
    # Si no hay datos en la selección, evitamos errores mostrando 0%
    conversion_promedio = 0.0
    label_conversion = "Conversión (Sin datos registrados)"

col1.metric("Total Enviados", f"{filtered_df['Enviados'].sum():,}")  
col2.metric("Total Entregados", f"{filtered_df['Entregados'].sum():,}")  
col3.metric("Tasa de Lectura Promedio", f"{(filtered_df['Leidos'].sum() / filtered_df['Entregados'].sum() * 100):.1f}%")  
col4.metric(label_conversion, f"{conversion_promedio:.1f}%")  
  
# 4. GRÁFICO DE EMBUDO (FUNNEL) DINÁMICO
st.subheader("Embudo de Conversión Consolidado")  

# Etapas que siempre tienen datos cargados
etapas = ["Enviados", "Entregados", "Leídos", "Clicks", "Respuestas"]
valores = [
    filtered_df["Enviados"].sum(), 
    filtered_df["Entregados"].sum(), 
    filtered_df["Leidos"].sum(), 
    filtered_df["Clicks"].sum(), 
    filtered_df["Respuestas"].sum()
]  

# Si hay campañas con conversiones en la selección actual, sumamos el paso final al gráfico
if len(campanas_con_conversion) > 0:
    # Calculamos el estimado de ventas (Enviados * % de Conversión de cada campaña)
    ventas_reales = (campanas_con_conversion["Enviados"] * campanas_con_conversion["Conversión %"]).sum()
    etapas.append("Conversión (Ventas)")
    valores.append(int(ventas_reales))

fig_funnel = go.Figure(go.Funnel(  
    y=etapas,  
    x=valores  
))  
st.plotly_chart(fig_funnel, use_container_width=True)
