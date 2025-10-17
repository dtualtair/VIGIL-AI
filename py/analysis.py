import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# Load the preprocessed data
df = pd.read_csv("../preprocessed_delhi_crime_data.csv")

# Convert Date to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Feature Engineering
df['DayOfWeek'] = df['Date'].dt.dayofweek
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year
df['IsWeekend'] = df['DayOfWeek'].isin([5, 6]).astype(int)

# Create a total crime column
crime_columns = ['Rape', 'Kidnapping and Abduction', 'Dowry Deaths',
                 'Assault on women with intent to outrage her modesty',
                 'Insult to modesty of Women', 'Cruelty by Husband or his Relatives',
                 'Importation of Girls', 'Attempt to commit Rape']
df['TotalCrimes'] = df[crime_columns].sum(axis=1)

# Exploratory Data Analysis

# Time series plot of total crimes
plt.figure(figsize=(12, 6))
df.groupby('Date')['TotalCrimes'].sum().plot()
plt.title('Total Crimes Over Time')
plt.xlabel('Date')
plt.ylabel('Total Crimes')
plt.savefig('total_crimes_over_time.png')
plt.close()

# Correlation heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(df[crime_columns + ['Literacy_Rate', 'Unemployment_Rate', 'Avg_Income']].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap of Crime Types and Socioeconomic Factors')
plt.savefig('correlation_heatmap.png')
plt.close()

# Crime distribution by district
plt.figure(figsize=(12, 6))
df.groupby('District')['TotalCrimes'].sum().sort_values(ascending=False).plot(kind='bar')
plt.title('Total Crimes by District')
plt.xlabel('District')
plt.ylabel('Total Crimes')
plt.xticks(rotation=45)
plt.savefig('crimes_by_district.png')
plt.close()

# Crime distribution by day of week
plt.figure(figsize=(10, 6))
df.groupby('DayOfWeek')['TotalCrimes'].mean().plot(kind='bar')
plt.title('Average Crimes by Day of Week')
plt.xlabel('Day of Week (0 = Monday, 6 = Sunday)')
plt.ylabel('Average Crimes')
plt.savefig('crimes_by_day_of_week.png')
plt.close()

# Crime distribution by month
plt.figure(figsize=(10, 6))
df.groupby('Month')['TotalCrimes'].mean().plot(kind='bar')
plt.title('Average Crimes by Month')
plt.xlabel('Month')
plt.ylabel('Average Crimes')
plt.savefig('crimes_by_month.png')
plt.close()

# Relationship between literacy rate and total crimes
plt.figure(figsize=(10, 6))
plt.scatter(df['Literacy_Rate'], df['TotalCrimes'])
plt.title('Literacy Rate vs Total Crimes')
plt.xlabel('Literacy Rate')
plt.ylabel('Total Crimes')
plt.savefig('literacy_vs_crimes.png')
plt.close()

# Print summary statistics
print(df[crime_columns + ['TotalCrimes', 'Literacy_Rate', 'Unemployment_Rate', 'Avg_Income']].describe())

# Save the updated dataframe
df.to_csv('delhi_crime_data_with_features.csv', index=False)

print("Exploratory Data Analysis completed. Check the generated PNG files for visualizations.")

# Load preprocessed data for visualization
df = pd.read_csv("../preprocessed_delhi_crime_data.csv")

# 1. Total Crimes Over Time (Line Plot)
plt.figure(figsize=(12, 6))
df.groupby('Date')['TotalCrimes'].sum().plot()
plt.title('Total Crimes Over Time')
plt.xlabel('Date')
plt.ylabel('Total Crimes')
plt.savefig('total_crimes_over_time.png')
plt.close()

# 2. Total Crimes by District (Bar Plot)
plt.figure(figsize=(12, 6))
df.groupby('District')['TotalCrimes'].sum().sort_values(ascending=False).plot(kind='bar', color='skyblue')
plt.title('Total Crimes by District')
plt.xlabel('District')
plt.ylabel('Total Crimes')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('total_crimes_by_district.png')
plt.close()

# 3. Total Crimes by Day of Week (Bar Plot)
plt.figure(figsize=(10, 6))
df.groupby('DayOfWeek')['TotalCrimes'].mean().plot(kind='bar', color='orange')
plt.title('Average Crimes by Day of Week')
plt.xlabel('Day of Week (0=Monday, 6=Sunday)')
plt.ylabel('Average Crimes')
plt.savefig('crimes_by_day_of_week.png')
plt.close()

# 4. Total Crimes by Month (Bar Plot)
plt.figure(figsize=(10, 6))
df.groupby('Month')['TotalCrimes'].mean().plot(kind='bar', color='green')
plt.title('Average Crimes by Month')
plt.xlabel('Month')
plt.ylabel('Average Crimes')
plt.savefig('crimes_by_month.png')
plt.close()

# 5. Correlation Heatmap (Heatmap)
plt.figure(figsize=(12, 10))
sns.heatmap(df[crime_columns + ['Literacy_Rate', 'Unemployment_Rate', 'Avg_Income']].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap of Crime Types and Socioeconomic Factors')
plt.savefig('correlation_heatmap.png')
plt.close()

# 6. Literacy Rate vs Total Crimes (Scatter Plot)
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Literacy_Rate', y='TotalCrimes', data=df, color='purple')
plt.title('Literacy Rate vs Total Crimes')
plt.xlabel('Literacy Rate (%)')
plt.ylabel('Total Crimes')
plt.savefig('literacy_vs_crimes.png')
plt.close()

# 7. Unemployment Rate vs Total Crimes (Scatter Plot)
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Unemployment_Rate', y='TotalCrimes', data=df, color='red')
plt.title('Unemployment Rate vs Total Crimes')
plt.xlabel('Unemployment Rate (%)')
plt.ylabel('Total Crimes')
plt.savefig('unemployment_vs_crimes.png')
plt.close()

# 8. Average Income vs Total Crimes (Scatter Plot)
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Avg_Income', y='TotalCrimes', data=df, color='blue')
plt.title('Average Income vs Total Crimes')
plt.xlabel('Average Income (INR)')
plt.ylabel('Total Crimes')
plt.savefig('income_vs_crimes.png')
plt.close()

# 9. Crime Distribution by Latitude and Longitude (Scatter Plot)
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Longitude', y='Latitude', size='TotalCrimes', sizes=(20, 200), hue='TotalCrimes', palette="viridis", data=df)
plt.title("Crime Distribution by Geographic Location")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend(title="Crime Count", loc="upper left")
plt.savefig("crime_distribution_geography.png")
plt.close()

# 10. Police Stations vs Total Crimes (Scatter Plot)
plt.figure(figsize=(10, 6))
sns.scatterplot(x="Police_Stations", y="TotalCrimes", data=df, color="brown")
plt.title("Police Stations vs Total Crimes")
plt.xlabel("Number of Police Stations")
plt.ylabel("Total Crimes")
plt.savefig("police_stations_vs_crimes.png")
