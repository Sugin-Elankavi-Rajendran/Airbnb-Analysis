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

st.set_page_config(layout="wide")
st.title('Airbnb Analysis')


