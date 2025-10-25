import streamlit as st
import importlib

st.set_page_config(
    page_title="Sistema CCTV",
    page_icon="🎥",
    layout="centered"
)

# === SIDEBAR ===
st.sidebar.title("📂 Navegación")
main_page = st.sidebar.radio(
    "Selecciona un módulo:",
    ["🏠 Inicio", "📋 Registro", "🔍 Consulta", "📊 Reportes", "⚙️ Configuración"]
)

# === FUNCIÓN PARA CARGAR SUBPÁGINAS ===
def cargar_pagina(nombre_modulo):
    try:
        modulo = importlib.import_module(nombre_modulo)
        if hasattr(modulo, "run"):
            modulo.run()  # ejecuta función run() del módulo
        else:
            st.warning(f"⚠️ El módulo `{nombre_modulo}` no tiene una función run().")
    except ModuleNotFoundError:
        st.error(f"❌ No se encontró el módulo `{nombre_modulo}`.")
    except Exception as e:
        st.error(f"⚠️ Error al cargar la página: {e}")

# === INICIO ===
if main_page == "🏠 Inicio":
    st.title("🎥 Sistema de Control CCTV")
    st.markdown("---")
    st.header("🧭 Cómo navegar")
    st.markdown("""
    Usa el menú lateral para acceder a los diferentes módulos:
    - 📝 **Registro:** Diligencia los formatos de recuperaciones y casos detectados.
    - 🔍 **Consulta:** Visualiza los registros ya enviados y busca por SKU, fecha o responsable.
    - 📊 **Reportes:** Analiza la información consolidada mediante indicadores.
    - ⚙️ **Configuración:** Administra listas de SKU, usuarios o parámetros del sistema.
    """)

# === REGISTRO ===
elif main_page == "📋 Registro":
    st.title("📋 Registro de actividades")

    # Inicializamos el estado de la subpágina si no existe
    if "subpage" not in st.session_state:
        st.session_state["subpage"] = None

    # Si no hay subpágina seleccionada, mostramos los botones
    if st.session_state["subpage"] is None:
        st.write("Selecciona el formulario que deseas abrir:")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🧾 Recuperaciones CCTV"):
                st.session_state["subpage"] = "pages.1_recuperaciones_cctv"

        with col2:
            if st.button("📦 Auditoría Recibo"):
                st.session_state["subpage"] = "pages.2_auditoria_recibo"

        with col3:
            if st.button("🏭 Auditoría Warehouse"):
                st.session_state["subpage"] = "pages.3_auditoria_warehouse"

    # Si ya hay una subpágina seleccionada, la mostramos
    else:
        import importlib

        module = importlib.import_module(st.session_state["subpage"])
        module.run()

        # Botón para volver al menú principal
        st.markdown("---")
        if st.button("⬅️ Volver al menú de registro"):
            st.session_state["subpage"] = None
