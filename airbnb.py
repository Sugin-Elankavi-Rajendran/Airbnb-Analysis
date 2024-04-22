import streamlit as st
import pandas as pd
import ast

############

st.set_page_config(layout="wide")
st.title('Airbnb Analysis')

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
        st.write("File uploaded successfully!")
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.write(df.head())

        missing_values = df.isnull().sum()
        st.write("Missing values:\n", missing_values)
        df.drop(['summary','space','description','neighborhood_overview',
                 'notes','transit','access','interaction','house_rules',
                 'cancellation_policy','last_scraped','calendar_last_scraped',
                 'weekly_price','monthly_price','cleaning_fee','images','listing_url'], axis=1, inplace=True)
        df.dropna(subset=['name'], inplace=True)
        df.dropna(subset=['first_review'], inplace=True)
        df.dropna(subset=['reviews_per_month'], inplace=True)
        df.dropna(subset=['security_deposit'], inplace=True)
        df['bedrooms'].fillna(df['bedrooms'].mean(), inplace=True)
        df['beds'].fillna(df['beds'].mean(), inplace=True)
        df['bathrooms'].fillna(df['bathrooms'].mean(), inplace=True)

        df['host'] = df['host'].apply(lambda x: ast.literal_eval(x))
        df['host_id'] = df['host'].apply(lambda x: x.get('host_id'))
        df['host_name'] = df['host'].apply(lambda x: x.get('host_name'))
        df['host_location'] = df['host'].apply(lambda x: x.get('host_location'))
        df['host_neighbourhood'] = df['host'].apply(lambda x: x.get('host_neighbourhood'))
        df['host_listings_count'] = df['host'].apply(lambda x: x.get('host_listings_count'))
        df['host_total_listings_count'] = df['host'].apply(lambda x: x.get('host_total_listings_count'))

        df.drop(columns=['host'], inplace=True)

        missing_values = df.isnull().sum()
        st.write("Missing values:\n", missing_values)
        st.write(df.head())
        df.to_csv("cleaned_airbnb_data.csv", index=False)

############


