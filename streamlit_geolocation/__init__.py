import streamlit.components.v1 as components

def geolocation():
    """Render the custom geolocation component."""
    return components.declare_component(
        "streamlit_geolocation",
        path="./streamlit_geolocation"
    )