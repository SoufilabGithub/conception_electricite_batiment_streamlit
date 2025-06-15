import streamlit as st
import importlib

st.set_page_config(page_title="Conception Électrique", layout="wide")
st.title("⚡ Conception Électrique du Bâtiment")

st.sidebar.markdown("## 📁 Sections disponibles")
choix = st.sidebar.radio("Choisir une section :", [
    "I. Simulation de l'Énergie",
    "II. Dimensionnement des Conduits",
    "III. Protection contre les Chocs Électriques"
])

mapping_modules = {
    "I. Simulation de l'Énergie": "section1_simulation_streamlit_full",
    "II. Dimensionnement des Conduits": "section2_conduits_streamlit",
    "III. Protection contre les Chocs Électriques": "section3_protection_streamlit"
}

module_name = mapping_modules[choix]
module = importlib.import_module(module_name)

if hasattr(module, "main"):
    module.main()
else:
    st.error(f"⚠️ La fonction `main()` est manquante dans `{module_name}.py`")
