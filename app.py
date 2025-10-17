import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime
import folium
from streamlit_folium import st_folium
import requests
from functools import lru_cache
from twilio.rest import Client
import geocoder

# Twilio credentials (replace with your actual credentials)
TWILIO_ACCOUNT_SID = 'ACa851305b330f02071ebd953a0c26319b'
TWILIO_AUTH_TOKEN = '0ce15705637e0be037524175fadbbcab'
TWILIO_PHONE_NUMBER = '+14065014871'

# Load the trained model
with open('safety_score_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Load the preprocessed dataset
data = pd.read_csv('preprocessed_dataset.csv')

# Create a mapping of pincodes to districts
pincode_district_mapping = {
    "Central": ["110001", "110002", "110003", "110005", "110006", "110055", "110004", "110008", "110010", "110012"],
    "East": ["110031", "110032", "110051", "110091", "110092", "110093", "110094", "110095", "110096", "110013", "110014"],
    "New Delhi": ["110001", "110011", "110021", "110023", "110029", "110049", "110057", "110060", "110066", "110069"],
    "North": ["110006", "110007", "110009", "110033", "110036", "110040", "110042", "110054", "110084", "110085", "110050", "110052", "110056"],
    "North East": ["110032", "110053", "110090", "110093", "110094"],
    "North West": ["110033", "110034", "110035", "110039", "110040", "110041", "110081", "110082", "110083", "110084", "110085", "110086", "110087", "110088", "110089", "110099"],
    "South": ["110003", "110016", "110017", "110019", "110020", "110024", "110025", "110029", "110030", "110044", "110047", "110048", "110049", "110062", "110065", "110068", "110070", "110074", "110079", "110097"],
    "South West": ["110037", "110038", "110043", "110045", "110046", "110047", "110061", "110064", "110067", "110071", "110072", "110073", "110075", "110076", "110077", "110078", "110080", "110022"],
    "West": ["110015", "110018", "110026", "110027", "110028", "110058", "110059", "110063", "110064", "110098"]
}

# Function to get district from pincode
def get_district_from_pincode(pincode):
    for district, pincodes in pincode_district_mapping.items():
        if pincode in pincodes:
            return district
    return None

# Google Maps API key
API_KEY = 'AIzaSyAhRJDZgwuA5MUbJba23Ln25XvzABvCiZE'

# Cache API responses for better performance
@lru_cache(maxsize=100)
def get_nearby_areas(query):
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={query}&location=28.6139,77.2090&radius=5000&key={API_KEY}"
    try:
        response = requests.get(url, timeout=5)  # Add timeout to avoid hanging
        result = response.json()
        if result['status'] == 'OK':
            return [item['description'] for item in result['predictions']]
        else:
            st.error(f"Google Places API Error: {result.get('error_message', 'Unknown error')}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch nearby areas: {e}")
        return []

# Function to get geolocation and postal code from address
def get_geolocation(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
    try:
        response = requests.get(url, timeout=5)  # Add timeout to avoid hanging
        result = response.json()
        if result['status'] == 'OK':
            location = result['results'][0]['geometry']['location']
            lat = location['lat']
            lng = location['lng']
            address_components = result['results'][0]['address_components']
            postal_code = next((component['long_name'] for component in address_components if 'postal_code' in component['types']), None)
            return lat, lng, postal_code
        else:
            st.error(f"Geocoding API Error: {result.get('error_message', 'Unknown error')}")
            return None, None, None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch geolocation: {e}")
        return None, None, None

# Function to send SMS
def send_sms(message, to_phone_number):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone_number
        )
        st.success(f"Emergency message sent to your Emergency contact Ekveer Sahoo at {to_phone_number}")
    except Exception as e:
        st.error(f"Failed to send emergency message: {str(e)}")

# Streamlit app
st.title("VIGIL-AI")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Select District", "Search Address", "Choose on Map", "SOS Call"])

with tab1:
    st.header("Select District")
    district = st.selectbox("Select District", sorted(data['District'].unique()))
    selected_date = st.date_input("Select Date")
    time_input = st.time_input("Select Time")

    if st.button("Predict Safety Score"):
        district_info = data[data['District'] == district]
        if not district_info.empty:
            district_info = district_info.iloc[0]

            # Prepare input data for the model
            input_data = {
                'DayOfWeek': selected_date.weekday(),
                'Month': selected_date.month,
                'Rape_Time': time_input.hour,
                'Kidnapping and Abduction_Time': time_input.hour,
                'Dowry Deaths_Time': time_input.hour,
                'Assault on women with intent to outrage her modesty_Time': time_input.hour,
                'Insult to modesty of Women_Time': time_input.hour,
                'Cruelty by Husband or his Relatives_Time': time_input.hour,
                'Importation of Girls_Time': time_input.hour,
                'Attempt to commit Rape_Time': time_input.hour,
                'Latitude': district_info.get('Latitude', 28.6139),  # Default latitude for New Delhi
                'Longitude': district_info.get('Longitude', 77.2090),  # Default longitude for New Delhi
                'Literacy_Rate': district_info['Literacy_Rate'],
                'Unemployment_Rate': district_info['Unemployment_Rate'],
                'Avg_Income': district_info['Avg_Income'],
                'Police_Stations': district_info['Police_Stations'],
                'Hospitals': district_info['Hospitals'],
                'Schools': district_info['Schools'],
                'Area': district_info['Area']
            }

            input_df = pd.DataFrame([input_data])

            # Ensure input features match model's expected features
            input_df = input_df[model.feature_names_in_]

            # Predict safety score
            safety_score = model.predict(input_df)[0]

            # Round and constrain safety score between 1 and 5
            safety_score = round(safety_score)
            safety_score = max(1, min(5, safety_score))

            # Display predicted safety score and advice
            st.write(f"Predicted Safety Score: {safety_score}")

            if safety_score >= 4:
                st.write("Safety Level: Very Safe")
                st.write("Advice: Enjoy your time, but always stay aware of your surroundings.")
            elif safety_score == 3:
                st.write("Safety Level: Moderately Safe")
                st.write("Advice: Take normal precautions and stay vigilant.")
            elif safety_score == 2:
                st.write("Safety Level: Exercise Caution")
                st.write("Advice: Be extra careful and consider traveling with a companion.")
            else:
                st.write("Safety Level: Use Extreme Caution")
                st.write("Advice: Avoid unnecessary travel and stay in well-lit, populated areas if you must go out.")
        else:
            st.error("District information not found in the dataset.")

with tab2:
    st.header("Search Address")

    # Initialize session state for address suggestions
    if "address_suggestions" not in st.session_state:
        st.session_state.address_suggestions = []

    # Real-time autocomplete
    address_query = st.text_input("Enter Address", key="address_query")

    # Update suggestions as the user types
    if address_query:
        st.session_state.address_suggestions = get_nearby_areas(address_query)

    # Display suggestions in a dropdown below the input field
    if st.session_state.address_suggestions:
        selected_address = st.selectbox("Select from suggestions", st.session_state.address_suggestions)
    else:
        selected_address = address_query

    selected_date = st.date_input("Select Date", key="date2")
    time_input = st.time_input("Select Time", key="time2")

    if st.button("Predict Safety Score", key="predict2"):
        if selected_address:
            latitude, longitude, postal_code = get_geolocation(selected_address)
            if latitude is not None and longitude is not None:
                district = get_district_from_pincode(postal_code)
                if district:
                    # Display pincode and district
                    st.write(f"**Pincode:** {postal_code}")
                    st.write(f"**District:** {district}")

                    district_info = data[data['District'] == district]
                    if not district_info.empty:
                        district_info = district_info.iloc[0]

                        # Prepare input data for the model
                        input_data = {
                            'DayOfWeek': selected_date.weekday(),
                            'Month': selected_date.month,
                            'Rape_Time': time_input.hour,
                            'Kidnapping and Abduction_Time': time_input.hour,
                            'Dowry Deaths_Time': time_input.hour,
                            'Assault on women with intent to outrage her modesty_Time': time_input.hour,
                            'Insult to modesty of Women_Time': time_input.hour,
                            'Cruelty by Husband or his Relatives_Time': time_input.hour,
                            'Importation of Girls_Time': time_input.hour,
                            'Attempt to commit Rape_Time': time_input.hour,
                            'Latitude': latitude,
                            'Longitude': longitude,
                            'Literacy_Rate': district_info['Literacy_Rate'],
                            'Unemployment_Rate': district_info['Unemployment_Rate'],
                            'Avg_Income': district_info['Avg_Income'],
                            'Police_Stations': district_info['Police_Stations'],
                            'Hospitals': district_info['Hospitals'],
                            'Schools': district_info['Schools'],
                            'Area': district_info['Area']
                        }

                        input_df = pd.DataFrame([input_data])

                        # Ensure input features match model's expected features
                        input_df = input_df[model.feature_names_in_]

                        # Predict safety score
                        safety_score = model.predict(input_df)[0]

                        # Round and constrain safety score between 1 and 5
                        safety_score = round(safety_score)
                        safety_score = max(1, min(5, safety_score))

                        # Display predicted safety score and advice
                        st.write(f"Predicted Safety Score: {safety_score}")

                        if safety_score >= 4:
                            st.write("Safety Level: Very Safe")
                            st.write("Advice: Enjoy your time, but always stay aware of your surroundings.")
                        elif safety_score == 3:
                            st.write("Safety Level: Moderately Safe")
                            st.write("Advice: Take normal precautions and stay vigilant.")
                        elif safety_score == 2:
                            st.write("Safety Level: Exercise Caution")
                            st.write("Advice: Be extra careful and consider traveling with a companion.")
                        else:
                            st.write("Safety Level: Use Extreme Caution")
                            st.write("Advice: Avoid unnecessary travel and stay in well-lit, populated areas if you must go out.")
                    else:
                        st.error("District information not found in the dataset.")
                else:
                    st.error("Could not determine district from pincode.")
            else:
                st.error("Please enter a valid address or select a nearby area.")
        else:
            st.error("Please enter an address.")

with tab3:
    st.header("Choose on Map")

    # Initialize session state for map data and marker location
    if "map_data" not in st.session_state:
        st.session_state.map_data = None
    if "marker_location" not in st.session_state:
        st.session_state.marker_location = [28.6139, 77.2090]  # Default location (New Delhi)
    if "zoom" not in st.session_state:
        st.session_state.zoom = 12  # Default zoom

    # Create the base map
    m = folium.Map(location=st.session_state.marker_location, zoom_start=st.session_state.zoom)

    # Add Google Maps tile layer
    google_maps_api_key = "AIzaSyAhRJDZgwuA5MUbJba23Ln25XvzABvCiZE"  # Replace with your actual Google Maps API key
    folium.TileLayer(
        tiles=f"https://mt1.google.com/vt/lyrs=m&x={{x}}&y={{y}}&z={{z}}&key={google_maps_api_key}",
        attr="Google Maps",
        name="Google Maps",
    ).add_to(m)

    # Add a red marker at the current location in session state
    folium.Marker(
        location=st.session_state.marker_location,
        draggable=False,
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    # Render the map and capture clicks
    map_data = st_folium(m, width=700, height=500, key="folium_map")

    # Update marker position immediately after each click
    if map_data.get("last_clicked"):
        latitude, longitude = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
        st.session_state.marker_location = [latitude, longitude]  # Update session state with new marker location
        st.session_state.zoom = map_data["zoom"]

        # Use Google Maps API to get the address of the clicked location
        url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={google_maps_api_key}"
        response = requests.get(url)
        result = response.json()

        if result["status"] == "OK":
            address = result["results"][0]["formatted_address"]
            address_components = result["results"][0]["address_components"]
            postal_code = next(
                (component["long_name"] for component in address_components if "postal_code" in component["types"]),
                None
            )
            district = get_district_from_pincode(postal_code) if postal_code else None

            st.session_state.map_data = {
                "latitude": latitude,
                "longitude": longitude,
                "address": address,
                "postal_code": postal_code,
                "district": district
            }
        else:
            st.error("Failed to retrieve address for the selected location.")

        # Redraw the map immediately with the new marker location
        m = folium.Map(location=st.session_state.marker_location, zoom_start=st.session_state.zoom)
        folium.TileLayer(
            tiles=f"https://mt1.google.com/vt/lyrs=m&x={{x}}&y={{y}}&z={{z}}&key={google_maps_api_key}",
            attr="Google Maps",
            name="Google Maps",
        ).add_to(m)
        folium.Marker(
            location=st.session_state.marker_location,
            draggable=False,
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
        st_folium(m, width=700, height=500, key="folium_map")

    # Display the selected location
    if st.session_state.map_data:
        st.write(f"**Selected Location:** {st.session_state.map_data['address']}")
        st.write(f"**Latitude:** {st.session_state.map_data['latitude']}")
        st.write(f"**Longitude:** {st.session_state.map_data['longitude']}")
        st.write(f"**Postal Code:** {st.session_state.map_data['postal_code']}")
        st.write(f"**District:** {st.session_state.map_data['district']}")

    selected_date = st.date_input("Select Date", key="date3")
    time_input = st.time_input("Select Time", key="time3")

    if st.button("Predict Safety Score", key="predict3"):
        if st.session_state.map_data:
            latitude = st.session_state.map_data["latitude"]
            longitude = st.session_state.map_data["longitude"]
            address = st.session_state.map_data["address"]
            postal_code = st.session_state.map_data["postal_code"]
            district = st.session_state.map_data["district"]

            if district:
                district_info = data[data['District'] == district]
                if not district_info.empty:
                    district_info = district_info.iloc[0]

                    # Prepare input data for the model
                    input_data = {
                        'DayOfWeek': selected_date.weekday(),
                        'Month': selected_date.month,
                        'Rape_Time': time_input.hour,
                        'Kidnapping and Abduction_Time': time_input.hour,
                        'Dowry Deaths_Time': time_input.hour,
                        'Assault on women with intent to outrage her modesty_Time': time_input.hour,
                        'Insult to modesty of Women_Time': time_input.hour,
                        'Cruelty by Husband or his Relatives_Time': time_input.hour,
                        'Importation of Girls_Time': time_input.hour,
                        'Attempt to commit Rape_Time': time_input.hour,
                        'Latitude': latitude,
                        'Longitude': longitude,
                        'Literacy_Rate': district_info['Literacy_Rate'],
                        'Unemployment_Rate': district_info['Unemployment_Rate'],
                        'Avg_Income': district_info['Avg_Income'],
                        'Police_Stations': district_info['Police_Stations'],
                        'Hospitals': district_info['Hospitals'],
                        'Schools': district_info['Schools'],
                        'Area': district_info['Area']
                    }

                    input_df = pd.DataFrame([input_data])

                    # Ensure input features match model's expected features
                    input_df = input_df[model.feature_names_in_]

                    # Predict safety score
                    safety_score = model.predict(input_df)[0]

                    # Round and constrain safety score between 1 and 5
                    safety_score = round(safety_score)
                    safety_score = max(1, min(5, safety_score))

                    # Display predicted safety score and advice
                    st.write(f"Predicted Safety Score: {safety_score}")

                    if safety_score >= 4:
                        st.write("Safety Level: Very Safe")
                        st.write("Advice: Enjoy your time, but always stay aware of your surroundings.")
                    elif safety_score == 3:
                        st.write("Safety Level: Moderately Safe")
                        st.write("Advice: Take normal precautions and stay vigilant.")
                    elif safety_score == 2:
                        st.write("Safety Level: Exercise Caution")
                        st.write("Advice: Be extra careful and consider traveling with a companion.")
                    else:
                        st.write("Safety Level: Use Extreme Caution")
                        st.write("Advice: Avoid unnecessary travel and stay in well-lit, populated areas if you must go out.")
                else:
                    st.error("District information not found in the dataset.")
            else:
                st.error("Could not determine district from pincode.")
        else:
            st.error("Please select a location on the map.")


with tab4:
    st.header("SOS Emergency Call")

    # Initialize session state for location data
    if "location_data" not in st.session_state:
        st.session_state.location_data = None

    # Fetch current location using geocoder
    myloc = geocoder.ip('me')
    if myloc.latlng:
        latitude, longitude = myloc.latlng
        st.session_state.location_data = {"latitude": latitude, "longitude": longitude}
    else:
        st.error("Failed to get current location. Please ensure location services are enabled and allow access.")

    # SOS Emergency Button
    if st.button("SOS Emergency"):
        if st.session_state.location_data:
            latitude = st.session_state.location_data["latitude"]
            longitude = st.session_state.location_data["longitude"]

            # Prepare message with location
            message = f"Emergency! I need help. My current location is: https://www.google.com/maps?q={latitude},{longitude}"
            st.session_state.location_data = {"latitude": latitude, "longitude": longitude}
            st.write(f"Your current location: Latitude = {latitude}, Longitude = {longitude}")
            st.write(f"Sending your current location to nearst emergency services.")
            st.write(f"Calling 112...")
            # Send SMS to loved one
            loved_one_number = "+919315852959"  # Replace with the actual number
            send_sms(message, loved_one_number)
        else:
            st.error("Failed to get current location. Please ensure location services are enabled and allow access.")
