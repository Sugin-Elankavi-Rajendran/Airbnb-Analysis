#import streamlit as st
from pymongo import MongoClient
from client import mongo

client = MongoClient(mongo)

db = client["airbnb"]

collection = db["listings"]

query = {
    "accommodates": {"$gte": 6},
    "price": {"$lte": 100}
}

results = collection.find(query)

for listing in results:
    print("Name:", listing["name"])
    print("Listing URL:", listing["listing_url"])
    print("Price:", listing["price"])
    print("Accommodates:", listing["accommodates"])
    print("--------------")

#st.set_page_config(layout="wide")

