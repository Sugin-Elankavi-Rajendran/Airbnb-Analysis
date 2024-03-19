from pymongo import MongoClient
from client import mongo
import pandas as pd
import streamlit as st
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from streamlit_folium import folium_static

############

client = MongoClient(mongo)

db = client["sample_airbnb"]

collection = db["listingsAndReviews"]

results = collection.find({})

############

df = pd.DataFrame(results)

# Remove missing values and duplicates
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# Display DataFrame columns and first few rows
st.write("DataFrame columns:", df.columns)
st.write("First few rows of the DataFrame:", df.head())

# Streamlit setup
st.set_page_config(layout="wide")
st.title('Airbnb Distribution Map')

# Create map
map_center = [41.1413, -8.61308]  # Coordinates for Porto, Portugal
m = folium.Map(location=map_center, zoom_start=10)

# Add markers for each listing
for idx, row in df.iterrows():
    folium.Marker(location=[row['location']['coordinates'][1], row['location']['coordinates'][0]], popup=row['address']['street']).add_to(m)

# Display map
folium_static(m)

# Heatmap visualization of availability by month
availability_by_month = df.groupby(df['availability']['availability_30']).size().reset_index(name='counts')
plt.figure(figsize=(10, 6))
sns.heatmap(availability_by_month.pivot('availability', 'availability_365', 'counts'), cmap='Blues')
plt.title('Availability Heatmap by Month')
plt.xlabel('Availability for 30 Days')
plt.ylabel('Availability for 365 Days')
st.pyplot()

# Export cleaned data to CSV
df.to_csv('cleaned_data.csv', index=False)