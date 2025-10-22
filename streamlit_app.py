# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd
from datetime import datetime

# Título y descripción
st.title("🧾 Formato para reporte de Recuperaciones")


# Obtener sesión activa de Snowflake
session = get_active_session()

 # === Selección de tienda ===
#tiendas = session.table("ikea_col.tiendas.tiendas").select(col("TIENDA"), col("ID"))
#pd_tiendas = tiendas.to_pandas()

lista_tiendas = st.selectbox(
    "Elige una de las tiendas",
    #pd_tiendas["TIENDA"].to_list(),
    ["IKEA NQS", "IKEA MALLPLAZA CALI", "IKEA ENVIGADO"],
    placeholder="Selecciona una tienda",
    index=None
)

if not lista_tiendas:
    st.warning("👉 Para comenzar, selecciona una de las tiendas del listado")
else:
    # Obtener ID de tienda
    #id_tienda = int(pd_tiendas.loc[pd_tiendas["TIENDA"] == lista_tiendas, "ID"].iloc[0])
    match lista_tiendas:
        case "IKEA NQS":
            id_tienda = 1
        case "IKEA MALLPLAZA CALI":
            id_tienda = 2
        case "IKEA ENVIGADO":
            id_tienda = 3
  
    # === Campos de fecha y hora ===
    fecha = st.date_input("📅 Ingresa la fecha de la recuperación:", value=None)
    hora = st.time_input("🕒 Ingresa la hora de la recuperación:", value=None)
    
    # === Calcular información extra desde la fecha y la hora ===

    if not fecha and hora:
        
    else: 
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
    
    # === Vigilantes ===
    vigilantes_df = (
        session.table("ikea_col.cctv.vigilantes")
        .filter(col("ID_TIENDA") == id_tienda)
        .select(col("NOMBRE_VIGILANTE"))
        .to_pandas()
    )

    lista_vigilantes = st.selectbox(
        "👮 Indica el nombre del guarda",
        vigilantes_df["NOMBRE_VIGILANTE"].to_list(),
        placeholder="Selecciona un guarda",
        index=None
    )
    
    vigilante_id = session.table("ikea_col.cctv.vigilantes").filter(col("NOMBRE_VIGILANTE") == lista_vigilantes).select(col("IDVIGILANTE")).to_pandas()
    vigilante = vigilante_id["IDVIGILANTE"].iloc[0]

    # === Piso, ubicación y tipología ===
    pisos = st.radio(
        "🏬 Elige el piso",
        ["Piso 1", "Piso 2", "Piso 3", "Pecera"],
        index=None
    )

    ubicacion = st.radio(
        "📍 Elige la ubicación",
        ["Antenas", "Autopago", "Cajas Asistidas", "Auditorías"],
        index=None
    )

    tipologia = st.radio(
        "🔍 Elige una tipología",
        ["Intención de hurto", "Producto no facturado", "Error de sistema", "Error de coworker"],
        index=None
    )

    # === Datos del coworker ===
    nombre_cw = st.text_input("👤 Ingresa el nombre del Coworker:")
    pos_cw = st.text_input("💻 Ingresa el número de POS:")

    # Validar que POS sea numérico
    try:
        pos_cw = int(pos_cw) if pos_cw else None
    except ValueError:
        st.warning("⚠️ Ingresa solo números en el campo POS")

    # === Producto ===
    sku_df = session.table("ikea_col.products.sku").select(col("SKU"), col("ITEM")).to_pandas()

    lista_sku = st.selectbox(
        "📦 Ingresa el SKU",
        sku_df["SKU"].to_list(),
        placeholder="Selecciona un producto",
        index=None
    )

    if lista_sku:
        producto = sku_df.loc[sku_df["SKU"] == lista_sku, "ITEM"].iloc[0]
        st.info(f"🛒 Producto seleccionado: **{producto}**")

        familia_df = session.table("ikea_col.products.desc_general_products").filter(col("SKU") == lista_sku).select(col("FAMILY")).to_pandas()
        familia = familia_df["FAMILY"].iloc[0]
    
    # === Valores económicos ===
    cantidad = st.number_input("📊 Ingresa la cantidad recuperada:", min_value=1, value=1)
    pvp_publico = st.number_input("💰 Ingresa el valor unitario del producto:", min_value=0.0, value=None)

    # Calcular total y mostrar tabla
    if cantidad and pvp_publico:
        pvp_total = cantidad * pvp_publico

        valor = pd.DataFrame(
            [{
                "Cantidad": int(cantidad),
                "PVP Público": float(pvp_publico),
                "PVP Total": float(pvp_total)
            }]
        )

        valor_formateado = valor.style.format({
            "PVP Público": "${:,.0f}",
            "PVP Total": "${:,.0f}"
        })

        st.table(valor_formateado)

    # === Descripción del caso ===
    descripcion_caso = st.text_area("📝 Ingresa una descripción del caso:") 

    st.write("La siguiente sera la información que será ingresada:")
    recuperacion = pd.DataFrame([{
        "Tienda": lista_tiendas
        , "Fecha": fecha
        , "Hora": hora
        , "Rango Horas": rango_horas
        , "Mes": mes
        , "Dia": dia
        , "ID Vigilante": str(vigilante)
        , "Nombre Vigilante" : lista_vigilantes
        , "Piso": pisos
        , "Ubicación": ubicacion
        , "Tipologia": tipologia
        , "Nombre CW": nombre_cw
        , "POS": pos_cw
        , "SKU": lista_sku
        , "Familia": familia
        , "Producto": producto
        , "Cantidad": cantidad
        , "PVP Público": pvp_publico
        , "PVP Total": pvp_total        
        }]).T
    recuperacion.columns = recuperacion.iloc[0]
    recuperacion = recuperacion[1:]
    st.table(recuperacion)

    
# === Botón de envío ===
    submitted = st.button("📤 Registrar")

    if submitted:
        if not lista_tiendas and not lista_sku and not cantidad:
            st.error("Debe seleccionar una tienda antes de registrar.")
        else:
            
            st.success("✅ Información registrada correctamente (pendiente guardar en base).")