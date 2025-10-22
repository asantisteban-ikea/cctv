import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Mostrar secrets para depuración (puedes eliminarlo luego)
st.write(st.secrets)

# === CONFIGURACIÓN ===
st.title("🧾 Formato para reporte de Recuperaciones")

# Crear conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
spreadsheet = "1t_hRvnpf_UaIH9_ZXvItlrsHVf2UaLrxQSNcpZQoQVA"
st.write(conn.client.spreadsheet.worksheets())

try:
    client = conn._instance._client  # acceso directo al cliente gspread
    sh = client.open_by_key(spreadsheet)
    worksheets = [ws.title for ws in sh.worksheets()]
    st.success("✅ Conexión exitosa con el archivo.")
    st.write("📄 Hojas disponibles:", worksheets)
except Exception as e:
    st.error(f"❌ Error al obtener las hojas: {e}")

# === Cargar datos desde Google Sheets ===
df_tiendas = conn.read(spreadsheet=spreadsheet, worksheet="TIENDA")
df_vigilantes = conn.read(spreadsheet=spreadsheet, worksheet="VIGILANTES")
df_sku = conn.read(spreadsheet=spreadsheet, worksheet="HFB")
df_familias = conn.read(spreadsheet=spreadsheet, worksheet="HFB")  # Usa misma hoja si familia está allí
df_opciones_seleccion = conn.read(spreadsheet=spreadsheet, worksheet="OPCIONES DE SELECCION")
df_recuperaciones = conn.read(spreadsheet=spreadsheet, worksheet="RECUPERACIONES")

# === Selección de tienda ===
lista_tiendas = st.selectbox(
    "Elige una de las tiendas",
    df_tiendas["TIENDA"].dropna().tolist(),
    placeholder="Selecciona una tienda",
    index=None
)

if not lista_tiendas:
    st.warning("👉 Para comenzar, selecciona una de las tiendas del listado")
else:
    # Obtener ID de tienda
    id_tienda = df_tiendas.loc[df_tiendas["TIENDA"] == lista_tiendas, "ID"].iloc[0]

    # === Fecha y hora ===
    fecha = st.date_input("📅 Ingresa la fecha de la recuperación:")
    hora = st.time_input("🕒 Ingresa la hora de la recuperación:")

    if fecha and hora:
        horas = hora.hour
        rango_horas = f"{horas} - {horas+1}"
        mes = fecha.strftime("%B").capitalize()
        dia = fecha.strftime("%A").capitalize()
    else:
        rango_horas, mes, dia = None, None, None

    # === Vigilantes ===
    vigilantes_df = df_vigilantes[df_vigilantes["ID_TIENDA"] == id_tienda]
    lista_vigilantes = st.selectbox(
        "👮 Indica el nombre del guarda",
        vigilantes_df["NOMBRE_VIGILANTE"].dropna().tolist(),
        placeholder="Selecciona un guarda",
        index=None
    )

    if lista_vigilantes:
        vigilante = vigilantes_df.loc[
            vigilantes_df["NOMBRE_VIGILANTE"] == lista_vigilantes, "IDVIGILANTE"
        ].iloc[0]
    else:
        vigilante = None

    # === Piso, ubicación y área ===
    pisos = st.radio("🏬 Elige el piso", df_opciones_seleccion["PISOS"].dropna().tolist(), index=None)
    ubicacion = st.radio("📍 Elige la ubicación", df_opciones_seleccion["UBICACION"].dropna().tolist(), index=None)
    area_solicitud = st.radio("🗂️ Elige el área que solicita", df_opciones_seleccion["AREA QUE SOLICITA"].dropna().tolist(), index=None)

    # === Coworker ===
    nombre_cw = st.text_input("👤 Ingresa el nombre del Coworker:")
    pos_cw = st.text_input("💻 Ingresa el número de POS:")

    try:
        pos_cw = int(pos_cw) if pos_cw else None
    except ValueError:
        st.warning("⚠️ Ingresa solo números en el campo POS")

    # === Producto ===
    lista_sku = st.selectbox(
        "📦 Ingresa el SKU",
        df_sku["SKU"].dropna().tolist(),
        placeholder="Selecciona un producto",
        index=None
    )

    if lista_sku:
        producto = df_sku.loc[df_sku["SKU"] == lista_sku, "ITEM"].iloc[0]
        familia_row = df_familias.loc[df_familias["SKU"] == lista_sku, "FAMILIA"]
        familia = familia_row.iloc[0] if not familia_row.empty else "No definida"
        st.info(f"🛒 Producto seleccionado: **{producto}**")
    else:
        producto, familia = None, None

    # === Valores económicos ===
    cantidad = st.number_input("📊 Ingresa la cantidad recuperada:", min_value=1, value=1)
    pvp_publico = st.number_input("💰 Ingresa el valor unitario del producto:", min_value=0.0, value=0.0)

    pvp_total = cantidad * pvp_publico if cantidad and pvp_publico else 0

    if cantidad and pvp_publico:
        valor = pd.DataFrame(
            [{"Cantidad": int(cantidad), "PVP Público": float(pvp_publico), "PVP Total": float(pvp_total)}]
        )
        st.table(valor.style.format({"PVP Público": "${:,.0f}", "PVP Total": "${:,.0f}"}))

    # === Descripción ===
    descripcion_caso = st.text_area("📝 Ingresa una descripción del caso:")

    # === Resumen ===
    st.write("La siguiente será la información que será ingresada:")
    recuperacion = pd.DataFrame([{
        "Tienda": lista_tiendas,
        "Fecha": fecha,
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
        "Descripción Caso": descripcion_caso,
        "Fecha Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])

    st.table(recuperacion.T)

    # === Enviar registro ===
    if st.button("📤 Registrar"):
        if not lista_tiendas or not lista_sku or not cantidad:
            st.error("⚠️ Debes completar los campos obligatorios antes de registrar.")
        else:
            df_recuperaciones = pd.concat([df_recuperaciones, recuperacion], ignore_index=True)
            conn.update(worksheet="RECUPERACIONES", data=df_recuperaciones)
            st.success("✅ Información registrada correctamente.")
