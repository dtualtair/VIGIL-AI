import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler


# Create time-based features from existing data
def get_time_weight(hour):
    if 0 <= hour < 6:  # Late night
        return 1.0
    elif 6 <= hour < 12:  # Morning
        return 0.4
    elif 12 <= hour < 18:  # Afternoon
        return 0.6
    else:  # Evening/Night
        return 0.8


# Calculate safety score components
def calculate_safety_score(district_data):
    # Crime density score (30% weight)
    crime_density = district_data['TotalCrimes'] / district_data['Area']
    crime_score = 5 - (crime_density / crime_density.max() * 4)

    # Infrastructure score (40% weight)
    infra_features = ['Police_Stations', 'Hospitals', 'Schools']
    infra_score = district_data[infra_features].mean(axis=1) / district_data[infra_features].max().mean() * 5

    # Socioeconomic score (30% weight)
    socio_features = ['Literacy_Rate', 'Avg_Income']
    socio_score = district_data[socio_features].mean(axis=1) / district_data[socio_features].max().mean() * 5

    # Combined weighted score
    safety_score = (0.3 * crime_score +
                    0.4 * infra_score +
                    0.3 * socio_score)

    return safety_score


# Train model
def train_safety_model(data):
    features = ['Latitude', 'Longitude', 'Area', 'Literacy_Rate',
                'Police_Stations', 'Hospitals', 'Schools', 'Avg_Income']

    X = data[features]
    y = calculate_safety_score(data)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    return model


# Function to predict safety score
def predict_safety(model, district_data, hour):
    base_score = model.predict(district_data[['Latitude', 'Longitude', 'Area', 'Literacy_Rate',
                                              'Police_Stations', 'Hospitals', 'Schools', 'Avg_Income']])
    time_weight = get_time_weight(hour)
    return base_score * time_weight
