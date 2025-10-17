import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd

# Load and prepare the data
df = pd.read_csv("../modified_dataset.csv")

# Calculate total crimes for each district
crime_columns = ['Rape', 'Kidnapping and Abduction', 'Dowry Deaths',
                 'Assault on women with intent to outrage her modesty',
                 'Insult to modesty of Women', 'Cruelty by Husband or his Relatives',
                 'Importation of Girls', 'Attempt to commit Rape']

# Group by district and calculate means
district_data = df.groupby('District').agg({
    'Latitude': 'first',
    'Longitude': 'first',
    'TotalCrimes': 'sum'
}).reset_index()

# Extract coordinates and normalize crime values
latitudes = district_data['Latitude'].values
longitudes = district_data['Longitude'].values
crimes = district_data['TotalCrimes'].values
normalized_crimes = (crimes - crimes.min()) / (crimes.max() - crimes.min())

# Create finer grid for interpolation
padding = 0.01
min_lat, max_lat = latitudes.min() - padding, latitudes.max() + padding
min_lon, max_lon = longitudes.min() - padding, longitudes.max() + padding
grid_x, grid_y = np.mgrid[min_lon:max_lon:1000j, min_lat:max_lat:1000j]

# Interpolate with modified parameters
grid_z = griddata((longitudes, latitudes), normalized_crimes, (grid_x, grid_y),
                  method='cubic', fill_value=0.05)

# Apply smoothing
from scipy.ndimage import gaussian_filter
grid_z = gaussian_filter(grid_z, sigma=3)

# Create custom colormap with smooth transitions
colors = ['#FFFFD9', '#EDF8B1', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#B10026']
cmap = LinearSegmentedColormap.from_list('custom', colors, N=256)

# Plot with white background
plt.figure(figsize=(12, 8), facecolor='white')
ax = plt.gca()
ax.set_facecolor('white')

# Plot heatmap with adjusted alpha
plt.imshow(grid_z.T, extent=(min_lon, max_lon, min_lat, max_lat),
           origin='lower', cmap=cmap, aspect='auto', alpha=0.95)

# Add district markers and labels
for _, row in district_data.iterrows():
    plt.plot(row['Longitude'], row['Latitude'], 'k.', markersize=5)
    plt.annotate(row['District'], (row['Longitude'], row['Latitude']),
                 color='black', fontsize=8, ha='right')

plt.colorbar(label='Crime Intensity')
plt.title('Crime Heatmap of Delhi')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Add statistics box
stats_text = f"Total Crimes: {crimes.sum():,.0f}\n"
stats_text += f"Avg Crimes: {crimes.mean():,.0f}\n"
stats_text += f"Max Crimes: {crimes.max():,.0f}"
plt.text(min_lon, min_lat, stats_text,
         bbox=dict(facecolor='white', alpha=0.7),
         color='black', fontsize=8)

plt.tight_layout()
plt.show()
