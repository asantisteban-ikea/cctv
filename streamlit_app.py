import streamlit as st
import importlib

st.set_page_config(
    page_title="Sistema CCTV",
    page_icon="🎥",
    layout="centered"
)

# === SIDEBAR ===
st.sidebar.title("📂 Navegación")
page = st.sidebar.radio(
    "Selecciona un módulo:",
    ["🏠 Inicio", "📋 Registro", "🔍 Consulta", "📊 Reportes", "⚙️ Configuración"]
)

# === PÁGINA PRINCIPAL ===
if page == "🏠 Inicio":
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
elif page == "📋 Registro":
    st.title("📋 Registro de actividades")
    st.write("Selecciona el formulario que deseas abrir:")

    col1, col2, col3 = st.columns(3)

    if "subpage" not in st.session_state:
        st.session_state["subpage"] = None

    with col1:
        if st.button("🧾 Recuperaciones CCTV"):
            st.session_state["subpage"] = "pages.p1_recuperaciones_cctv"

    with col2:
        if st.button("📦 Auditoría Recibo"):
            st.session_state["subpage"] = "pages.p2_auditoria_recibo"

    with col3:
        if st.button("🏭 Auditoría Warehouse"):
            st.session_state["subpage"] = "pages.p3_auditoria_warehouse"

    # Si se seleccionó un submódulo, lo carga dinámicamente
    if st.session_state["subpage"]:
        try:
            module = importlib.import_module(st.session_state["subpage"])
            module.main()  # cada subpágina debe tener una función main()
        except Exception as e:
            st.error(f"No se pudo cargar el módulo: {st.session_state['subpage']}")
            st.exception(e)

# === CONSULTA ===
elif page == "🔍 Consulta":
    st.info("🔍 Módulo de consulta aún en desarrollo.")

# === REPORTES ===
elif page == "📊 Reportes":
    st.info("📊 Módulo de reportes aún en desarrollo.")

# === CONFIGURACIÓN ===
elif page == "⚙️ Configuración":
    st.info("⚙️ Módulo de configuración aún en desarrollo.")
