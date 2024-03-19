from pymongo import MongoClient
from client import mongo
import pandas as pd
import streamlit as st
import folium

############

client = MongoClient(mongo)

db = client["airbnb"]

collection = db["listings"]

results = collection.find({"city": "New York City"})

############

df = pd.DataFrame(results)

df.dropna(inplace=True)

df.drop_duplicates(inplace=True)

df['price'] = df['price'].astype(float)

############

st.set_page_config(layout="wide")

st.title('Airbnb Distribution Map')

