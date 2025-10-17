import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import pickle

# Load the preprocessed dataset
data = pd.read_csv('../preprocessed_dataset.csv')

# Calculate total crimes
crime_columns = [
    'Rape', 'Kidnapping and Abduction', 'Dowry Deaths',
    'Assault on women with intent to outrage her modesty',
    'Insult to modesty of Women', 'Cruelty by Husband or his Relatives',
    'Importation of Girls', 'Attempt to commit Rape'
]
data['TotalCrimes'] = data[crime_columns].sum(axis=1)

# Normalize total crimes
scaler = MinMaxScaler()
data['NormalizedCrimes'] = scaler.fit_transform(data[['TotalCrimes']])

# Create safety score (inverse of normalized crimes)
data['SafetyScore'] = 5 - (data['NormalizedCrimes'] * 4)

# Define features and target variable
features = [
    'DayOfWeek', 'Month', 'Rape_Time', 'Kidnapping and Abduction_Time', 'Dowry Deaths_Time',
    'Assault on women with intent to outrage her modesty_Time', 'Insult to modesty of Women_Time',
    'Cruelty by Husband or his Relatives_Time', 'Importation of Girls_Time', 'Attempt to commit Rape_Time',
    'Literacy_Rate', 'Unemployment_Rate', 'Avg_Income', 'Police_Stations', 'Hospitals', 'Schools', 'Area'
]
X = data[features]
y = data['SafetyScore']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

# Save the model
with open('../safety_score_model.pkl', 'wb') as file:
    pickle.dump(model, file)

# Print evaluation metrics
print(f"R-squared: {r2:.4f}")
print(f"Mean Squared Error: {mse:.4f}")
print(f"Root Mean Squared Error: {rmse:.4f}")
