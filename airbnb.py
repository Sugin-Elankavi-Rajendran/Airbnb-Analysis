from pymongo import MongoClient
from client import mongo
import pandas as pd
import streamlit as st

############

client = MongoClient(mongo)
db = client["sample_airbnb"]
collection = db["listingsAndReviews"]

cursor = collection.find({})
df = pd.DataFrame(list(cursor))

csv_file_path = "listingsAndReviews.csv"
df.to_csv(csv_file_path, index=False)

print("CSV file has been saved successfully.")

############

st.set_page_config(layout="wide")
st.title('Airbnb Analysis')

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
        st.write("File uploaded successfully!")
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.write(df.head())

