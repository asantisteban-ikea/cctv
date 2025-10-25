import streamlit as st
from datetime import datetime

# Configuración inicial
st.set_page_config(
    page_title="Gestión y Reportes",
    page_icon="📹",
    layout="centered"
)

# Encabezado principal
st.title("📋 Sistema de Registro y Control")
st.markdown("""
Bienvenido al sistema de **gestión de reportes de seguridad**.

Este aplicativo permite registrar, consultar y analizar información 
relacionada con los casos de seguridad en tiendas.

---           
""")

# --- Estado del submenú ---
if "mostrar_registro" not in st.session_state:
    st.session_state.mostrar_registro = False

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
            st.switch_page("pages/1_recuperaciones_cctv.py")
    with col2:
        if st.button("📋 Auditoría Recibo", key="auditoria_recibo"):
            st.switch_page("pages/2_auditoria_recibo.py")
    with col3:
        if st.button("🏗️ Auditoría Warehouse", key="auditoria_warehouse"):
            st.switch_page("pages/3_auditoria_warehouse.py")

st.markdown("---")

# --- Otros módulos ---
st.subheader("📊 Reportes")
st.write("Analiza la información consolidada mediante indicadores.")
if st.button("📈 Ir a Reportes ➜", key="reportes"):
    st.switch_page("pages/3_auditoria_warehouse.py")

st.markdown("---")

st.subheader("⚙️ Configuración")
st.write("Administra listas de SKU, usuarios o parámetros del sistema.")
if st.button("⚙️ Ir a Configuración ➜", key="configuracion"):
    st.switch_page("pages/4_configuracion.py")
