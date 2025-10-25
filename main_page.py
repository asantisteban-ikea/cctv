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

### 🧭 **Cómo navegar**
Usa el menú lateral para acceder a los diferentes módulos:

- 📝 **Registro:** Diligencia los formatos de recuperaciones y casos detectectados.
- 🔍 **Consulta:** Visualiza los registros ya enviados y busca por SKU, fecha o responsable.
- 📊 **Reportes:** Analiza la información consolidada mediante indicadores.
- ⚙️ **Configuración:** Administra listas de SKU, usuarios o parámetros del sistema.

---

🕒 **Hora local:**  
{hora}
""".format(hora=datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

st.info("Selecciona una opción desde el panel lateral izquierdo para comenzar.")