import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
from datetime import datetime

# === CONFIGURACIÓN ===
st.title("🧾 Formato para reporte de Recuperaciones")

# === CREDENCIALES ===
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["connections"]["gsheets"]["credentials"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

gc = gspread.authorize(credentials)

# === CONEXIÓN AL ARCHIVO ===
spreadsheet_id = st.secrets["connections"]["gsheets"]["spreadsheet"]
sh = gc.open_by_key(spreadsheet_id)

# ⛓️ Cargar datos con cache
@st.cache_data(ttl=86400)  # 1 semana de cache
def load_data(sheet):
    return conn.read(spreadsheet=spreadsheet, worksheet=sheet)


# === CARGAR HOJAS ===
#tiendas_ws = sh.worksheet("TIENDAS")
vigilantes_ws = sh.worksheet("VIGILANTES")
sku_ws = sh.worksheet("HFB")
#opciones_ws = sh.worksheet("OPCIONES DE SELECCION")
recuperaciones_ws = sh.worksheet("RECUPERACIONES")

# Convertir a DataFrame
#df_tiendas = pd.DataFrame(tiendas_ws.get_all_records())
#df_vigilantes = pd.DataFrame(vigilantes_ws.get_all_records())
df_sku = pd.DataFrame(sku_ws.get_all_records())
#df_opciones = pd.DataFrame(opciones_ws.get_all_records())
df_recuperaciones = pd.DataFrame(recuperaciones_ws.get_all_records())

# === INTERFAZ ===
lista_tiendas = st.selectbox(
    "Elige una de las tiendas",
    ["IKEA NQS", "IKEA MALLPLAZA CALI", "IKEA ENVIGADO"],
    placeholder="Selecciona una tienda",
    value=None
)

if lista_tiendas:
    match lista_tiendas:
        case "IKEA NQS":
            id_tienda = 1
        case "IKEA MALLPLAZA CALI":
            id_tienda = 2
        case "IKEA ENVIGADO":
            id_tienda = 3

    fecha = st.date_input("📅 Fecha de la recuperación")
    hora = st.time_input("🕒 Hora de la recuperación")

    vigilantes_df = df_vigilantes[df_vigilantes["ID_TIENDA"] == id_tienda]
    lista_vigilantes = st.selectbox(
        "👮 Nombre del vigilante",
        vigilantes_df["NOMBRE_VIGILANTE"].dropna().tolist(),
    )

    pisos = st.radio(
        "🏬 Piso", 
        ["Piso 1", "Piso 2", "Piso 3", "Pecera"],
        placeholder= "Indica el piso",
        value=None
    )

    ubicacion = st.radio(
        "📍 Ubicación",
        ["Antenas", "Autopago", "Auditoria", "Cajas Asistidas", "Check Out", "Solicitud"],
        placeholder="Indica la ubicación",
        value=None
        )

    area = st.radio(
        "🗂️ Área que solicita", 
        ["CX", "Recovery", "Olvido Cliente", "Fulfillment", "BNO", "S&S", "Sales", "Duty Manager"],
        placeholder="Indica el área que solicita",
        value=None
        )

    nombre_cw = st.text_input("👤 Nombre del Coworker")
    pos_cw = st.text_input("💻 Número de POS")

    lista_sku = st.selectbox("📦 SKU", df_sku["SKU"].dropna().tolist())

    if lista_sku:
        producto = df_sku.loc[df_sku["SKU"] == lista_sku, "ITEM"].iloc[0]
        familia = df_sku.loc[df_sku["SKU"] == lista_sku, "FAMILIA"].iloc[0]
        st.info(f"🛒 Producto: **{producto}**, Familia: **{familia}**")

    cantidad = st.number_input("📊 Cantidad", min_value=1, value=1)
    pvp = st.number_input("💰 Valor unitario", min_value=0.0, value=0.0)
    total = cantidad * pvp

    st.write(f"**Total:** ${total:,.0f}")

    descripcion = st.text_area("📝 Descripción del caso")

    if st.button("📤 Registrar"):
        nueva_fila = [
            lista_tiendas, str(fecha), str(hora),
            lista_vigilantes, pisos, ubicacion, area,
            nombre_cw, pos_cw, lista_sku, producto,
            familia, cantidad, pvp, total, descripcion,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        recuperaciones_ws.append_row(nueva_fila)
        st.success("✅ Información registrada correctamente.")
