import streamlit as st
from datetime import datetime

# Configuración inicial
st.set_page_config(
    page_title="Gestión y Reportes",
    page_icon="📹",
    layout="centered"
)

# === SIDEBAR ===
with st.sidebar:
    st.header("🧭 Navegación")

    pagina = st.radio(
        "Selecciona un módulo:",
        [
            "🏠 Inicio",
            "📦 Registro",
            "🔎 Consulta",
            "📊 Reportes",
            "⚙️ Configuración"
        ]
    )

# === CONTENIDO PRINCIPAL ===
if pagina == "🏠 Inicio":
    st.title("🎥 Sistema de Recuperaciones y Auditorías CCTV")

    st.markdown("""
    ---
    ### 🧭 Cómo navegar
    Usa el menú lateral para acceder a los diferentes módulos:
    - 📝 **Registro:** Diligencia los formatos de recuperaciones y casos detectados.
    - 🔎 **Consulta:** Visualiza los registros ya enviados y busca por SKU, fecha o responsable.
    - 📊 **Reportes:** Analiza la información consolidada mediante indicadores.
    - ⚙️ **Configuración:** Administra listas de SKU, usuarios o parámetros del sistema.
    ---
    """)

elif pagina == "📦 Registro":
    st.header("📦 Registro de recuperaciones")
    st.info("Selecciona un submódulo de registro:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🧾 Recuperaciones CCTV"):
            st.switch_page("1_recuperaciones_cctv")
    with col2:
        if st.button("📋 Auditoría Recibo"):
            st.switch_page("2_auditoria_recibo")
    with col3:
        if st.button("🏗️ Auditoría Warehouse"):
            st.switch_page("3_auditoria_warehouse")


# --- Botón principal: Registro ---
st.subheader("📝 Registro")
st.write("Diligencia los formatos de recuperaciones y casos detectados.")
if st.button("➡️ Ir al módulo de Registro", key="registro_main"):
    # Alternar visualización del submenú
    st.session_state.mostrar_registro = not st.session_state.mostrar_registro


# --- Submenú dinámico (solo aparece si se activa) ---
if st.session_state.mostrar_registro:
    st.markdown("#### 🔽 Selecciona el tipo de registro:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📦 Recuperaciones", key="recuperaciones"):
            st.switch_page("1_recuperaciones_cctv")
    with col2:
        if st.button("📋 Auditoría Recibo", key="auditoria_recibo"):
            st.switch_page("2_auditoria_recibo")
    with col3:
        if st.button("🏗️ Auditoría Warehouse", key="auditoria_warehouse"):
            st.switch_page("3_auditoria_warehouse")

st.markdown("---")

# --- Otros módulos ---
st.subheader("📊 Reportes")
st.write("Analiza la información consolidada mediante indicadores.")
if st.button("📈 Ir a Reportes ➜", key="reportes"):
    st.switch_page("3_auditoria_warehouse")

st.markdown("---")

st.subheader("⚙️ Configuración")
st.write("Administra listas de SKU, usuarios o parámetros del sistema.")
if st.button("⚙️ Ir a Configuración ➜", key="configuracion"):
    st.switch_page("4_configuracion")