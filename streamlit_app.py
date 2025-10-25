import streamlit as st

st.set_page_config(
    page_title="Sistema CCTV",
    page_icon="👁️",
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
    st.title("👁️ Sistema de Control CCTV")
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

    # botones de navegación interna
    with col1:
        if st.button("🧾 Recuperaciones CCTV"):
            st.session_state["page"] = "Recuperaciones"
            st.markdown("[Abrir Recuperaciones CCTV](./1_recuperaciones_cctv)")

    with col2:
        if st.button("📦 Auditoría Recibo"):
            st.session_state["page"] = "Recibo"
            st.markdown("[Abrir Auditoría Recibo](./2_auditoria_recibo)")

    with col3:
        if st.button("🏭 Auditoría Warehouse"):
            st.session_state["page"] = "Warehouse"
            st.markdown("[Abrir Auditoría Warehouse](./3_auditoria_warehouse)")

# === CONSULTA ===
elif page == "🔍 Consulta":
    st.info("🔍 Módulo de consulta aún en desarrollo.")

# === REPORTES ===
elif page == "📊 Reportes":
    st.info("📊 Módulo de reportes aún en desarrollo.")

# === CONFIGURACIÓN ===
elif page == "⚙️ Configuración":
    st.info("⚙️ Módulo de configuración aún en desarrollo.")
