import streamlit as st
import ee
import geemap.foliumap as geemap
import folium
import streamlit.components.v1 as components
import json


# Authenticate the Earth Engine
ee.Authenticate()




default_location = [36.03393423886839, 50.99986716703871]

# Initialize the Earth Engine
ee.Initialize(project="ee-chrcheel")







# Set up Streamlit
st.set_page_config(layout="wide", page_icon=":globe_with_meridians:", page_title="Light Pollution Map")

# Hide Streamlit default elements like the header, footer, and menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Sidebar for map controls
st.sidebar.title("Map Controls")

# Add input sliders for visualization parameters
min_value = st.sidebar.slider("Min Radiance Value", 0.0, 100.0, 0.0, step=1.0)
max_value = st.sidebar.slider("Max Radiance Value", 0.0, 100.0, 100.0, step=1.0)
opacity = st.sidebar.slider("Overlay Opacity", 0.0, 1.0, 0.7, step=0.1)



# Define the default location for the map
# Store the map center and zoom level in session state to persist between rerenders
if 'map_center' not in st.session_state:
    st.session_state.map_center = default_location  # Default to New York City
if 'map_zoom' not in st.session_state:
    st.session_state.map_zoom = 9


# Create the map object
Map = geemap.Map(center=st.session_state.map_center, zoom=st.session_state.map_zoom, draw_export=False)


Map.add_basemap("SATELLITE")
# Load the NOAA/VIIRS dataset
dataset = ee.ImageCollection("NOAA/VIIRS/001/VNP46A1").filterDate('2023-01-01', '2023-12-31')

# Select the latest image
latest_image = dataset.sort('system:time_start', False).first()

# Visualization parameters
vis_params = {
    'min': min_value,
    'max': max_value,
    'bands': ['DNB_At_Sensor_Radiance_500m'],
    'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']
}

# Add the layer to the map
Map.addLayer(latest_image, vis_params, "Light Pollution", opacity=opacity)

# Add Layer Control
Map.addLayerControl()

# Function to handle the user's changes
def update_map_state(map_center, map_zoom):
    st.session_state.map_center = map_center
    st.session_state.map_zoom = map_zoom

# Display the map in Streamlit
Map.to_streamlit(height=600)
