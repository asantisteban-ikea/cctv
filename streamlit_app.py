import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# === CONFIGURACIÓN GENERAL ===
st.set_page_config(page_title="Formato Recuperaciones", page_icon="🧾", layout="wide")
st.title("🧾 Formato para reporte de Recuperaciones")

# === CONEXIÓN A GOOGLE SHEETS ===
conn = st.connection("gsheets", type=GSheetsConnection)

spreadsheet = "1t_hRvnpf_UaIH9_ZXvItlrsHVf2UaLrxQSNcpZQoQVA"

# === LECTURA DE HOJAS ===
try:
    df_tiendas = conn.read(spreadsheet=spreadsheet, worksheet="TIENDAS", ttl=0)
    df_vigilantes = conn.read(spreadsheet=spreadsheet, worksheet="VIGILANTES", ttl=0)
    df_sku = conn.read(spreadsheet=spreadsheet, worksheet="HFB", ttl=0)
    df_opciones = conn.read(spreadsheet=spreadsheet, worksheet="OPCIONES DE SELECCION", ttl=0)
    df_recuperaciones = conn.read(spreadsheet=spreadsheet, worksheet="RECUPERACIONES", ttl=0)
except Exception as e:
    st.error(f"❌ Error al leer Google Sheets: {e}")
    st.stop()

# === SELECCIÓN DE TIENDA ===
lista_tiendas = st.selectbox(
    "🏬 Elige una de las tiendas",
    df_tiendas["TIENDA"].dropna().tolist(),
    placeholder="Selecciona una tienda",
    index=None
)

if not lista_tiendas:
    st.warning("👉 Para comenzar, selecciona una tienda del listado.")
    st.stop()

# === DATOS DE TIENDA Y FECHA ===
id_tienda = df_tiendas.loc[df_tiendas["TIENDA"] == lista_tiendas, "ID"].iloc[0]
fecha = st.date_input("📅 Fecha de recuperación:")
hora = st.time_input("🕒 Hora de recuperación:")

horas = hora.hour
rango_horas = f"{horas} - {horas+1}"
mes = fecha.strftime("%B").capitalize()
dia = fecha.strftime("%A").capitalize()

# === VIGILANTE ===
vigilantes_df = df_vigilantes[df_vigilantes["ID_TIENDA"] == id_tienda]
lista_vigilantes = st.selectbox(
    "👮 Nombre del guarda",
    vigilantes_df["NOMBRE_VIGILANTE"].dropna().tolist(),
    placeholder="Selecciona un guarda",
    index=None
)
vigilante = (
    vigilantes_df.loc[vigilantes_df["NOMBRE_VIGILANTE"] == lista_vigilantes, "IDVIGILANTE"].iloc[0]
    if lista_vigilantes
    else None
)

# === PISO, UBICACIÓN, ÁREA ===
pisos = st.radio("🏢 Piso", df_opciones["PISOS"].dropna().tolist(), index=None)
ubicacion = st.radio("📍 Ubicación", df_opciones["UBICACION"].dropna().tolist(), index=None)
area_solicitud = st.radio("🗂️ Área que solicita", df_opciones["AREA QUE SOLICITA"].dropna().tolist(), index=None)

# === COWORKER ===
nombre_cw = st.text_input("👤 Nombre del Coworker:")
pos_cw = st.text_input("💻 Número de POS:")
try:
    pos_cw = int(pos_cw) if pos_cw else None
except ValueError:
    st.warning("⚠️ Ingresa solo números en el campo POS")

# === PRODUCTO ===
lista_sku = st.selectbox(
    "📦 SKU del producto",
    df_sku["SKU"].dropna().tolist(),
    placeholder="Selecciona un SKU",
    index=None
)
if lista_sku:
    producto = df_sku.loc[df_sku["SKU"] == lista_sku, "ITEM"].iloc[0]
    familia_row = df_sku.loc[df_sku["SKU"] == lista_sku, "FAMILIA"]
    familia = familia_row.iloc[0] if not familia_row.empty else "No definida"
    st.info(f"🛒 Producto seleccionado: **{producto}**")
else:
    producto, familia = None, None

# === VALORES ECONÓMICOS ===
cantidad = st.number_input("📊 Cantidad recuperada:", min_value=1, value=1)
pvp_publico = st.number_input("💰 Valor unitario del producto:", min_value=0.0, value=0.0)
pvp_total = cantidad * pvp_publico

st.table(pd.DataFrame(
    [{"Cantidad": cantidad, "PVP Público": pvp_publico, "PVP Total": pvp_total}]
).style.format({"PVP Público": "${:,.0f}", "PVP Total": "${:,.0f}"}))

# === DESCRIPCIÓN ===
descripcion_caso = st.text_area("📝 Descripción del caso:")

# === PREVISUALIZACIÓN ===
recuperacion = pd.DataFrame([{
    "Tienda": lista_tiendas,
    "Fecha": fecha,
    "Hora": str(hora),
    "Rango Horas": rango_horas,
    "Mes": mes,
    "Día": dia,
    "ID Vigilante": vigilante,
    "Nombre Vigilante": lista_vigilantes,
    "Piso": pisos,
    "Ubicación": ubicacion,
    "Área Solicitud": area_solicitud,
    "Nombre CW": nombre_cw,
    "POS": pos_cw,
    "SKU": lista_sku,
    "Familia": familia,
    "Producto": producto,
    "Cantidad": cantidad,
    "PVP Público": pvp_publico,
    "PVP Total": pvp_total,
    "Descripción Caso": descripcion_caso,
    "Fecha Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}])

st.write("📋 Información que se registrará:")
st.table(recuperacion.T)

# === GUARDAR EN GOOGLE SHEETS ===
if st.button("📤 Registrar"):
    try:
        df_actualizado = pd.concat([df_recuperaciones, recuperacion], ignore_index=True)
        conn.update(worksheet="RECUPERACIONES", data=df_actualizado)
        st.success("✅ Información registrada correctamente.")
    except Exception as e:
        st.error(f"❌ Error al guardar los datos: {e}")
