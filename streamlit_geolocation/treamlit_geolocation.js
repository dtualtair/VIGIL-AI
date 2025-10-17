function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                // Send the location data back to Streamlit
                Streamlit.setComponentValue({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                });
            },
            function(error) {
                console.error("Error getting location:", error);
                // Send an error message back to Streamlit
                Streamlit.setComponentValue({
                    error: "Failed to retrieve location. Please ensure location services are enabled and allow access."
                });
            }
        );
    } else {
        // Send an error message if geolocation is not supported
        Streamlit.setComponentValue({
            error: "Geolocation is not supported by this browser."
        });
    }
}

// Run the geolocation function when the component is loaded
getLocation();