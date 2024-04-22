import streamlit as st
import pandas as pd
import ast
import datetime

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
        
        df['reviews_per_month'].fillna(df['reviews_per_month'].mean(), inplace=True)
        df['security_deposit'].fillna(df['security_deposit'].mean(), inplace=True)
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

        df['reviews'] = df['reviews'].str.strip('[]').str.split(',')
        for key in ['reviewer_name', 'comments']:
                df[key] = df['reviews'].apply(lambda reviews_list: [review.split(':')[1].strip().strip("'\"") if len(review.split(':')) > 1 else None for review in reviews_list if key in review])
                
        df.drop(columns=['reviews'], inplace=True)

        df['review_scores'] = df['review_scores'].apply(ast.literal_eval)
        df['review_scores_accuracy'] = df['review_scores'].apply(lambda x: x.get('review_scores_accuracy'))
        df['review_scores_cleanliness'] = df['review_scores'].apply(lambda x: x.get('review_scores_cleanliness'))
        df['review_scores_checkin'] = df['review_scores'].apply(lambda x: x.get('review_scores_checkin'))
        df['review_scores_communication'] = df['review_scores'].apply(lambda x: x.get('review_scores_communication'))
        df['review_scores_location'] = df['review_scores'].apply(lambda x: x.get('review_scores_location'))
        df['review_scores_value'] = df['review_scores'].apply(lambda x: x.get('review_scores_value'))
        df['review_scores_rating'] = df['review_scores'].apply(lambda x: x.get('review_scores_rating'))

        df.drop(columns=['review_scores'], inplace=True)
        df.dropna(subset=['review_scores_value'], inplace=True)
        df.dropna(subset=['review_scores_accuracy'], inplace=True)
        df.dropna(subset=['review_scores_cleanliness'], inplace=True)
        df.dropna(subset=['review_scores_checkin'], inplace=True)
        df.dropna(subset=['review_scores_rating'], inplace=True)

        df['availability'] = df['availability'].apply(ast.literal_eval)
        df['availability_30'] = df['availability'].apply(lambda x: x.get('availability_30'))
        df['availability_60'] = df['availability'].apply(lambda x: x.get('availability_60'))
        df['availability_90'] = df['availability'].apply(lambda x: x.get('availability_90'))
        df['availability_365'] = df['availability'].apply(lambda x: x.get('availability_365'))

        df.drop(columns=['availability'], inplace=True)

        df['address'] = df['address'].apply(ast.literal_eval)
        df['street'] = df['address'].apply(lambda x: x.get('street'))
        df['suburb'] = df['address'].apply(lambda x: x.get('suburb'))
        df['government_area'] = df['address'].apply(lambda x: x.get('government_area'))
        df['market'] = df['address'].apply(lambda x: x.get('market'))
        df['country'] = df['address'].apply(lambda x: x.get('country'))
        df['country_code'] = df['address'].apply(lambda x: x.get('country_code'))
        df['latitude'] = df['address'].apply(lambda x: x.get('location', {}).get('coordinates', [])[0] if x.get('location') else None)
        df['longitude'] = df['address'].apply(lambda x: x.get('location', {}).get('coordinates', [])[1] if x.get('location') else None)

        df.drop(columns=['address'], inplace=True)

        missing_values = df.isnull().sum()
        st.write("Missing values:\n", missing_values)
        st.write(df.head())
        df.to_csv("cleaned_airbnb_data.csv", index=False)

############


