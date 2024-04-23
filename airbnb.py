import streamlit as st
import pandas as pd
import ast
import datetime
import plotly.express as px

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
        #df.to_csv("cleaned_airbnb_data.csv", index=False)

############

st.write("Geospatial Visualization")
def create_geospatial_viz(df):
            fig = px.scatter_geo(df, lat='latitude', lon='longitude', color='price', hover_name='name',
                                 size='price', projection='natural earth')
            
            # Customize layout and appearance
            fig.update_geos(
                showland=True,
                landcolor='rgb(243, 243, 243)',
                countrycolor='white'
            )
            fig.update_layout(
                title='Airbnb Listings Worldwide',
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    projection_type='natural earth'
                )
            )
            
            st.plotly_chart(fig)

create_geospatial_viz(df)

############

def create_price_analysis(df):
            fig = px.histogram(df, x="price", color="country", marginal="box", title="Price Distribution Across Different Countries")
            st.plotly_chart(fig)

            fig = px.box(df, x="property_type", y="price", title="Price Variation Across Property Types")
            st.plotly_chart(fig)

            df['first_review'] = pd.to_datetime(df['first_review'])
            df['month'] = df['first_review'].dt.month
            fig = px.box(df, x='month', y='price', title='Price Trends Over Months')
            st.plotly_chart(fig)

create_price_analysis(df)

############

def create_availability_analysis(df, availability_duration):
    # Create dynamic plots and charts to analyze availability variations
    # Example: Availability trends over time (seasonal analysis)
    df['first_review'] = pd.to_datetime(df['first_review'])
    df['year'] = df['first_review'].dt.year
    if availability_duration == '30':
        title = 'Availability Histogram for 30 Days'
        availability_col = 'availability_30'
    elif availability_duration == '60':
        title = 'Availability Histogram for 60 Days'
        availability_col = 'availability_60'
    elif availability_duration == '90':
        title = 'Availability Histogram for 90 Days'
        availability_col = 'availability_90'
    else:  # availability_duration == '365'
        title = 'Availability Histogram for 1 Year'
        availability_col = 'availability_365'
        
    fig = px.histogram(df, x='year', y=availability_col, title=title)
    st.plotly_chart(fig)

    # Heatmap visualization for availability by year
    heatmap_data = df.groupby(['country', 'year'])[availability_col].mean().reset_index()
    heatmap_fig = px.imshow(heatmap_data.pivot(index='country', columns='year', values=availability_col),
                            labels=dict(x="Year", y="Country", color="Availability"),
                            title=f'Availability Heatmap for {availability_duration} Days by Year',
                            color_continuous_scale='Viridis')
    st.plotly_chart(heatmap_fig)

availability_duration = st.selectbox("Select Availability Duration", ['30', '60', '90', '365'])

create_availability_analysis(df, availability_duration)

############

regions = df['host_location'].unique()
selected_region = st.selectbox("Select Region or Neighborhood", regions, index=0)

region_data = df[df['host_location'] == selected_region]

fig = px.histogram(region_data, x="price", title=f"Price Distribution in {selected_region}")
st.plotly_chart(fig)

############

selected_region = st.selectbox("Select Region or Neighborhood", ["All"] + list(df['host_location'].unique()))
selected_property_type = st.selectbox("Select Property Type", ["All"] + list(df['property_type'].unique()))

filtered_df = df.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df['host_location'] == selected_region]
if selected_property_type != "All":
    filtered_df = filtered_df[filtered_df['property_type'] == selected_property_type]

fig = px.histogram(filtered_df, x="price", title="Price Distribution")
st.plotly_chart(fig)