import streamlit as st
import pandas as pd

############

st.set_page_config(layout="wide")
st.title('Airbnb Analysis')

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
        st.write("File uploaded successfully!")
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.write(df.head())

############


