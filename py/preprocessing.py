import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load the dataset
data = pd.read_csv('../modified_dataset.csv')

# Convert 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')

# Extract additional temporal features
data['DayOfWeek'] = data['Date'].dt.dayofweek
data['Month'] = data['Date'].dt.month

# List of crime columns and their corresponding time columns
crime_columns = [
    'Rape', 'Kidnapping and Abduction', 'Dowry Deaths',
    'Assault on women with intent to outrage her modesty',
    'Insult to modesty of Women', 'Cruelty by Husband or his Relatives',
    'Importation of Girls', 'Attempt to commit Rape'
]

time_columns = [col + '_Time' for col in crime_columns]

# Convert time columns to hours (assuming they are in HH:MM format)
for col in time_columns:
    data[col] = pd.to_datetime(data[col], format='%H:%M', errors='coerce').dt.hour

# Fill missing values in time columns with the median
data[time_columns] = data[time_columns].fillna(data[time_columns].median())

# Calculate total crimes
data['TotalCrimes'] = data[crime_columns].sum(axis=1)

# Normalize total crimes
scaler = MinMaxScaler()
data['NormalizedCrimes'] = scaler.fit_transform(data[['TotalCrimes']])

# Create safety score (inverse of normalized crimes)
data['SafetyScore'] = 5 - (data['NormalizedCrimes'] * 4)

# Select relevant features for the model
features = ['Year', 'Month', 'DayOfWeek'] + time_columns + [
    'Literacy_Rate', 'Unemployment_Rate', 'Avg_Income',
    'Police_Stations', 'Hospitals', 'Schools', 'Area'
]

# Create the final preprocessed dataset
preprocessed_data = data[['Date', 'District'] + features + crime_columns + ['SafetyScore']]

# Save the preprocessed dataset
preprocessed_data.to_csv('preprocessed_dataset.csv', index=False)

print("Preprocessing completed. Data saved to 'preprocessed_dataset.csv'")
