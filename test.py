import streamlit as st
from twilio.rest import Client

# Twilio credentials (replace with your actual credentials)
TWILIO_ACCOUNT_SID = 'ACa851305b330f02071ebd953a0c26319b'
TWILIO_AUTH_TOKEN = 'f7513d7cf062fc823187fd567c8f24ef'
TWILIO_PHONE_NUMBER = '+14065014871'

# Function to send SMS
def send_sms(message, to_phone_number):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone_number
        )
        st.success(f"Emergency message sent to your loved one at {to_phone_number}")
    except Exception as e:
        st.error(f"Failed to send emergency message: {str(e)}")

# Streamlit app
st.title("Women Safety Score Predictor for New Delhi")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Select District", "Search Address", "Choose on Map", "SOS Call"])

with tab4:
    st.header("SOS Emergency Call")

    # Initialize session state for location data
    if "location_data" not in st.session_state:
        st.session_state.location_data = None

    # JavaScript to get the current location and update the URL
    get_location_js = """
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(position) {
                    // Update the URL with the latitude and longitude
                    const url = new URL(window.location);
                    url.searchParams.set("latitude", position.coords.latitude);
                    url.searchParams.set("longitude", position.coords.longitude);
                    window.history.pushState({}, "", url);
                    // Reload the page to send the data to Streamlit
                    window.location.reload();
                },
                function(error) {
                    console.error("Error getting location:", error);
                    alert("Failed to retrieve location. Please ensure location services are enabled and allow access.");
                }
            );
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }
    getLocation();
    </script>
    """

    # Display the JavaScript in the Streamlit app
    st.components.v1.html(get_location_js, height=0)

    # Get latitude and longitude from the URL
    latitude = st.experimental_get_query_params().get("latitude", [None])[0]
    longitude = st.experimental_get_query_params().get("longitude", [None])[0]

    # Check if location data is received
    if latitude and longitude:
        st.session_state.location_data = {"latitude": float(latitude), "longitude": float(longitude)}
        st.write(f"Your current location: Latitude = {latitude}, Longitude = {longitude}")
    else:
        st.error("Failed to get current location. Please ensure location services are enabled and allow access.")

    # SOS Emergency Button
    if st.button("SOS Emergency"):
        if st.session_state.location_data:
            latitude = st.session_state.location_data["latitude"]
            longitude = st.session_state.location_data["longitude"]

            # Prepare message with location
            message = f"Emergency! I need help. My current location is: https://www.google.com/maps?q={latitude},{longitude}"

            # Send SMS to loved one
            loved_one_number = "9315852959"  # Replace with the actual number
            send_sms(message, loved_one_number)
        else:
            st.error("Failed to get current location. Please ensure location services are enabled and allow access.")