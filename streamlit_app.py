import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# === CONFIGURACIÓN ===
st.title("🧾 Formato para reporte de Recuperaciones")

# === CARGAR CREDENCIALES ===
creds_dict = st.secrets["connections"]["gsheets"]["credentials"]
spreadsheet_id = st.secrets["connections"]["gsheets"]["spreadsheet"]

# Crear credenciales y cliente gspread
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
gc = gspread.authorize(creds)
sh = gc.open_by_key(spreadsheet_id)



# === CARGAR HOJAS ===
df_tiendas = pd.DataFrame(sh.worksheet("TIENDAS").get_all_records())
df_vigilantes = pd.DataFrame(sh.worksheet("VIGILANTES").get_all_records())
df_sku = pd.DataFrame(sh.worksheet("HFB").get_all_records())
df_opciones_seleccion = pd.DataFrame(sh.worksheet("OPCIONES DE SELECCION").get_all_records())
df_recuperaciones = pd.DataFrame(sh.worksheet("RECUPERACIONES").get_all_records())

# === SELECCIÓN DE TIENDA ===
lista_tiendas = st.selectbox(
    "Elige una de las tiendas",
    df_tiendas["TIENDA"].dropna().tolist(),
    placeholder="Selecciona una tienda",
    index=None
)

if not lista_tiendas:
    st.warning("👉 Para comenzar, selecciona una de las tiendas del listado")
else:
    id_tienda = df_tiendas.loc[df_tiendas["TIENDA"] == lista_tiendas, "ID"].iloc[0]

    fecha = st.date_input("📅 Ingresa la fecha de la recuperación:")
    hora = st.time_input("🕒 Ingresa la hora de la recuperación:")
    if fecha and hora:
        horas = hora.hour
        rango_horas = f"{horas} - {horas+1}"
        mes = fecha.strftime("%B").capitalize()
        dia = fecha.strftime("%A").capitalize()
    else:
        rango_horas, mes, dia = None, None, None

    vigilantes_df = df_vigilantes[df_vigilantes["ID_TIENDA"] == id_tienda]
    lista_vigilantes = st.selectbox(
        "👮 Indica el nombre del guarda",
        vigilantes_df["NOMBRE_VIGILANTE"].dropna().tolist(),
        placeholder="Selecciona un guarda",
        index=None
    )
    vigilante = None
    if lista_vigilantes:
        vigilante = vigilantes_df.loc[
            vigilantes_df["NOMBRE_VIGILANTE"] == lista_vigilantes, "IDVIGILANTE"
        ].iloc[0]

    pisos = st.radio("🏬 Elige el piso", df_opciones_seleccion["PISOS"].dropna().tolist(), index=None)
    ubicacion = st.radio("📍 Elige la ubicación", df_opciones_seleccion["UBICACION"].dropna().tolist(), index=None)
    area_solicitud = st.radio("🗂️ Elige el área que solicita", df_opciones_seleccion["AREA QUE SOLICITA"].dropna().tolist(), index=None)

    nombre_cw = st.text_input("👤 Ingresa el nombre del Coworker:")
    pos_cw = st.text_input("💻 Ingresa el número de POS:")
    try:
        pos_cw = int(pos_cw) if pos_cw else None
    except ValueError:
        st.warning("⚠️ Ingresa solo números en el campo POS")

    lista_sku = st.selectbox(
        "📦 Ingresa el SKU",
        df_sku["SKU"].dropna().tolist(),
        placeholder="Selecciona un producto",
        index=None
    )
    producto, familia = None, None
    if lista_sku:
        producto = df_sku.loc[df_sku["SKU"] == lista_sku, "ITEM"].iloc[0]
        familia = df_sku.loc[df_sku["SKU"] == lista_sku, "FAMILIA"].iloc[0]
        st.info(f"🛒 Producto seleccionado: **{producto}**")

    cantidad = st.number_input("📊 Ingresa la cantidad recuperada:", min_value=1, value=1)
    pvp_publico = st.number_input("💰 Ingresa el valor unitario del producto:", min_value=0.0, value=0.0)
    pvp_total = cantidad * pvp_publico

    st.write("### Resumen del registro")
    recuperacion = pd.DataFrame([{
        "Tienda": lista_tiendas,
        "Fecha": fecha.strftime("%Y-%m-%d"),
        "Hora": str(hora),
        "Rango Horas": rango_horas,
        "Mes": mes,
        "Dia": dia,
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
        "Fecha Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    st.dataframe(recuperacion)

    if st.button("📤 Registrar"):
        try:
            worksheet = sh.worksheet("RECUPERACIONES")
            existing = pd.DataFrame(worksheet.get_all_records())
            updated = pd.concat([existing, recuperacion], ignore_index=True)
            worksheet.update([updated.columns.values.tolist()] + updated.values.tolist())
            st.success("✅ Registro guardado correctamente en Google Sheets.")
        except Exception as e:
            st.error(f"❌ Error al guardar: {e}")
