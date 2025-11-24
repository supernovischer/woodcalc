import streamlit as st
from detector import count_piles
from estimator import calculate_mass
from PIL import Image
import numpy as np

st.set_page_config(page_title="Holzpfahl Zähler", layout="wide")

st.title("🌲 Holzpfahl Zähler & Masseschätzer")
st.markdown("Laden Sie ein Bild der Holzpfähle hoch, um deren Anzahl und Masse zu schätzen.")

# Sidebar for parameters
st.sidebar.header("Einstellungen")

# Wood types and their densities (kg/m³)
wood_types = {
    "Benutzerdefiniert": 600.0,
    "Robinie": 740.0,
    "Kastanie": 590.0,
    "Fichte (unbehandelt)": 470.0,
    "Fichte (imprägniert - grün)": 600.0,
    "Fichte (imprägniert - braun)": 600.0
}

selected_wood = st.sidebar.selectbox("Holzart", list(wood_types.keys()))
default_density = wood_types[selected_wood]

wood_density = st.sidebar.number_input("Holzdichte (kg/m³)", min_value=100.0, max_value=1500.0, value=default_density, step=10.0)
pile_diameter = st.sidebar.number_input("Durchschnittlicher Durchmesser (cm)", min_value=1.0, max_value=100.0, value=15.0, step=0.5)
pile_length = st.sidebar.number_input("Durchschnittliche Länge (m)", min_value=0.1, max_value=20.0, value=2.0, step=0.1)

st.sidebar.divider()
st.sidebar.header("Erkennungseinstellungen (Erweitert)")
st.sidebar.info("Passen Sie diese Werte an, wenn die Erkennung ungenau ist.")

min_dist = st.sidebar.slider("Min. Abstand zwischen Pfählen (px)", 10, 100, 40, help="Vergrößern, wenn zu viele überlappende Kreise erkannt werden.")
param2 = st.sidebar.slider("Erkennungsempfindlichkeit (Threshold)", 10, 100, 50, help="Höherer Wert = Weniger (aber sicherere) Erkennungen. Niedriger Wert = Mehr Erkennungen.")
min_radius = st.sidebar.slider("Min. Radius (px)", 5, 100, 15)
max_radius = st.sidebar.slider("Max. Radius (px)", 20, 200, 80)
blur_kernel = st.sidebar.slider("Glättung (Blur)", 1, 21, 9, step=2, help="Höherer Wert entfernt mehr Rauschen (Pflastersteine).")


uploaded_file = st.file_uploader("Bild hochladen", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Display original image
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Originalbild")
        st.image(image, use_container_width=True)
        
    # Process image
    # Reset file pointer for opencv reading
    uploaded_file.seek(0)
    count, processed_image = count_piles(uploaded_file, blur_kernel, min_dist, 100, param2, min_radius, max_radius)
    
    with col2:
        st.subheader("Erkanntes Bild")
        if processed_image is not None:
            st.image(processed_image, use_container_width=True)
        else:
            st.error("Fehler bei der Bildverarbeitung.")

    # Results
    st.divider()
    st.header("Ergebnisse")
    
    mass = calculate_mass(count, pile_diameter, pile_length, wood_density)
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Anzahl Pfähle", f"{count}")
    metric_col2.metric("Geschätzte Masse", f"{mass:.2f} kg")
    metric_col3.metric("Gesamtvolumen", f"{(mass/wood_density):.2f} m³")
