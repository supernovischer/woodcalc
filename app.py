import streamlit as st
from detector import count_piles, count_rectangles
from estimator import calculate_mass, calculate_mass_rectangular
from PIL import Image
import numpy as np

st.set_page_config(page_title="Holz Zähler", layout="wide")

st.title("🌲 Holz Zähler & Masseschätzer")
st.markdown("Laden Sie ein Bild hoch, um die Anzahl und Masse zu schätzen.")

# Sidebar for parameters
st.sidebar.header("Einstellungen")

# Mode Selection
mode = st.sidebar.radio("Modus", ["Runde Pfähle", "Eckige Bretter/Balken"])

# Wood types
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

# Dimensions based on mode
if mode == "Runde Pfähle":
    pile_diameter = st.sidebar.number_input("Durchschnittlicher Durchmesser (cm)", min_value=1.0, max_value=100.0, value=15.0, step=0.5)
else:
    col_w, col_h = st.sidebar.columns(2)
    rect_width = col_w.number_input("Breite (cm)", min_value=1.0, max_value=100.0, value=15.0, step=0.5)
    rect_height = col_h.number_input("Höhe/Dicke (cm)", min_value=1.0, max_value=100.0, value=5.0, step=0.5)

pile_length = st.sidebar.number_input("Durchschnittliche Länge (m)", min_value=0.1, max_value=20.0, value=2.0, step=0.1)

st.sidebar.divider()
st.sidebar.header("Erkennungseinstellungen (Erweitert)")

if mode == "Runde Pfähle":
    st.sidebar.info("Einstellungen für Kreiserkennung")
    min_dist = st.sidebar.slider("Min. Abstand (px)", 10, 100, 40)
    param2 = st.sidebar.slider("Sensitivität (Threshold)", 10, 100, 50)
    min_radius = st.sidebar.slider("Min. Radius (px)", 5, 100, 15)
    max_radius = st.sidebar.slider("Max. Radius (px)", 20, 200, 80)
    blur_kernel = st.sidebar.slider("Glättung (Blur)", 1, 21, 9, step=2)
else:
    st.sidebar.info("Einstellungen für Rechteckerkennung")
    thresh_block = st.sidebar.slider("Threshold Block Size", 3, 51, 11, step=2, help="Größerer Bereich = unempfindlicher gegen kleine Helligkeitsunterschiede.")
    min_area = st.sidebar.slider("Min. Fläche (px²)", 10, 2000, 100)
    max_area = st.sidebar.slider("Max. Fläche (px²)", 500, 20000, 5000)
    min_aspect = st.sidebar.slider("Min. Seitenverhältnis", 1.0, 10.0, 2.0, help="Verhältnis von Länge zu Breite. Höher = nur längliche Objekte.")


uploaded_file = st.file_uploader("Bild hochladen", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Originalbild")
        st.image(image, use_column_width=True)
        
    uploaded_file.seek(0)
    
    if mode == "Runde Pfähle":
        count, processed_image = count_piles(uploaded_file, blur_kernel, min_dist, 100, param2, min_radius, max_radius)
        mass = calculate_mass(count, pile_diameter, pile_length, wood_density)
    else:
        count, processed_image = count_rectangles(uploaded_file, thresh_block, min_area, max_area, min_aspect)
        mass = calculate_mass_rectangular(count, rect_width, rect_height, pile_length, wood_density)
    
    with col2:
        st.subheader("Erkanntes Bild")
        if processed_image is not None:
            st.image(processed_image, use_container_width=True)
        else:
            st.error("Fehler bei der Bildverarbeitung.")

    st.divider()
    st.header("Ergebnisse")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Anzahl", f"{count}")
    metric_col2.metric("Geschätzte Masse", f"{mass:.2f} kg")
    metric_col3.metric("Gesamtvolumen", f"{(mass/wood_density):.2f} m³")
