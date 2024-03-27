from pymongo import MongoClient
from client import mongo
import pandas as pd

############

client = MongoClient(mongo)
db = client["sample_airbnb"]
collection = db["listingsAndReviews"]

cursor = collection.find({})
df = pd.DataFrame(list(cursor))

csv_file_path = "listingsAndReviews.csv"
df.to_csv(csv_file_path, index=False)

print("CSV file has been saved successfully.")