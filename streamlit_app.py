import streamlit as st
import pandas as pd
import gspread
from google.oauth2 import service_account
from datetime import datetime
from zoneinfo import ZoneInfo

# === CONFIGURACIÓN ===
st.title("🧾 Formato para reporte de Recuperaciones")

# === CREDENCIALES ===
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["connections"]["gsheets"]["credentials"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

gc = gspread.authorize(credentials)
spreadsheet_id = st.secrets["connections"]["gsheets"]["spreadsheet"]
sh = gc.open_by_key(spreadsheet_id)

# === CARGA DE DATOS CON CACHE (TTL = 7 días) ===
@st.cache_data(ttl=7*24*60*60)  # 7 días en segundos
def load_worksheet_data(sheet_name):
    ws = sh.worksheet(sheet_name)
    return pd.DataFrame(ws.get_all_records())

# === CARGA DE HOJAS ===
df_vigilantes = load_worksheet_data("VIGILANTES")
df_sku = load_worksheet_data("HFB")
df_sku["SKU"] = df_sku["SKU"].astype(str).str.zfill(8)
recuperaciones_ws = sh.worksheet("RECUPERACIONES")

# === INTERFAZ ===
lista_tiendas = st.selectbox(
    "Elige una de las tiendas",
    ["IKEA NQS", "IKEA MALLPLAZA CALI", "IKEA ENVIGADO"],
    placeholder="Selecciona una tienda",
    index=None
)

if lista_tiendas:
    match lista_tiendas:
        case "IKEA NQS":
            id_tienda = 1
        case "IKEA MALLPLAZA CALI":
            id_tienda = 2
        case "IKEA ENVIGADO":
            id_tienda = 3

    fecha = st.date_input("📅 Fecha de la recuperación", value=None)
    hora = st.time_input("🕒 Hora de la recuperación", value=None)

    if fecha and hora:
        horas = hora.hour
        rango_horas = f"{horas} - {horas+1}"
        mes = fecha.month
        dia = fecha.weekday()
        
        match mes:
            case 1:
                mes = "Enero"
            case 2:
                mes = "Febrero"
            case 3:
                mes = "Marzo"
            case 4:
                mes = "Abril"
            case 5:
                mes = "Mayo"
            case 6:
                mes = "Junio"
            case 7:
                mes = "Julio"
            case 8:
                mes = "Agosto"
            case 9:
                mes = "Septiembre"
            case 10:
                mes = "Octubre"
            case 11:
                mes = "Noviembre"
            case 12:
                mes = "Diciembre"
                     
        match dia:
            case 0:
                dia = "Lunes"
            case 1:
                dia = "Martes"
            case 2:
                dia = "Miercoles"
            case 3:
                dia = "Jueves"
            case 4:
                dia = "Viernes"
            case 5:
                dia = "Sabado"
            case 6:
                dia = "Domingo"

    vigilantes_df = df_vigilantes[df_vigilantes["ID_TIENDA"] == id_tienda]
    lista_vigilantes = st.selectbox(
        "👮 Nombre del vigilante",
        vigilantes_df["NOMBRE VIGILANTE"].dropna().tolist(),
        index=None
    )

    pisos = st.radio(
        "🏬 Piso", 
        ["Piso 1", "Piso 2", "Piso 3", "Pecera"],
        horizontal=True,
        index=None
    )

    ubicacion = st.radio(
        "📍 Ubicación",
        ["Antenas", "Autopago", "Auditoria", "Cajas Asistidas", "Check Out", "Solicitud"],
        horizontal=True,
        index=None
    )

    area = st.radio(
        "🗂️ Área que solicita", 
        ["CX", "Recovery", "Olvido Cliente", "Fulfillment", "BNO", "S&S", "Sales", "Duty Manager"],
        horizontal=True,
        index=None
    )

    nombre_cw = st.text_input("👤 Nombre del Coworker")
    pos_cw = st.text_input("💻 Número de POS")
    if pos_cw:
        try:
            pos_cw = int(pos_cw)
        except Exception as e:
            st.warning(f"⚠️ Solo debes ingresar el número de la POS")   

    # === SELECCIÓN DE SKU CON BÚSQUEDA FILTRADA ===
    st.markdown("### 📦 Búsqueda de producto por SKU")

    # Campo de texto para escribir el SKU
    busqueda_sku = st.text_input(
        "🔎 Escribe el SKU del producto:",
        placeholder="Ejemplo: 001234 o 1234"
    )

    sku_seleccionado = None

    if busqueda_sku:
        # Buscar coincidencias parciales en el DataFrame
        filtro = df_sku[df_sku["SKU"].astype(str).str.contains(busqueda_sku, case=False, na=False)]

        # Mostrar sugerencias directamente bajo el campo
        if not filtro.empty:
            sugerencias = filtro.head(5)  # Muestra máximo 5 sugerencias

            st.markdown("**Coincidencias encontradas:**")
            for _, row in sugerencias.iterrows():
                st.write(f"🔹 `{row['SKU']}` — {row['ITEM']} ({row['FAMILIA']})")

            # Si hay coincidencia exacta
            match = filtro[filtro["SKU"] == busqueda_sku]
            if not match.empty:
                producto = match.iloc[0]["ITEM"]
                familia = match.iloc[0]["FAMILIA"]
                st.success(f"🛒 Producto: **{producto}**, Familia: **{familia}**")
                sku_seleccionado = busqueda_sku
        else:
            st.warning("⚠️ No se encontraron coincidencias.")

    cantidad = st.number_input("📊 Cantidad", min_value=1, value=1)
    pvp = st.number_input("💰 Valor unitario", min_value=0, value=0)
    total = cantidad * pvp
    st.write(f"**Total:** ${total:,.0f}")

    descripcion = st.text_area("📝 Descripción del caso")

    fecha_registro = datetime.now(ZoneInfo("America/Bogota")).strftime("%Y-%m-%d %H:%M:%S")


    if st.button("📤 Registrar"):
        try:
            nueva_fila = [
                fecha_registro,
                lista_tiendas, str(fecha), str(hora),
                lista_vigilantes, pisos, ubicacion, area,
                nombre_cw, pos_cw, lista_sku, producto,
                familia, cantidad, pvp, total, descripcion,
                dia, mes, rango_horas,
            ]
            recuperaciones_ws.append_row(nueva_fila)
            st.success("✅ Información registrada correctamente.")
        except Exception as e:
            st.error(f"⚠️ Error al registrar los datos: {e}")
