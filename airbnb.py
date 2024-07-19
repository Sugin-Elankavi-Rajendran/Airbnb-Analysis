import streamlit as st
import pandas as pd
import ast
import plotly.express as px

# Set page layout
st.set_page_config(layout="wide")
st.title('🌍 Airbnb Analysis Dashboard')

# Custom CSS for background, styles, and dark text input titles
st.markdown(
    """
    <style>
    /* Apply styles to the body to set the background image */
    body {
        background-image: url('https://hello.pricelabs.co/wp-content/uploads/2022/03/15-Airbnb-Hosting-Tips-To-Make-Your-Listing-Successful-1-1.png');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        margin: 0;
        padding: 0;
        height: 100vh;
    }
    /* Style the main container to make sure content is visible above the background */
    .stApp {
        background-color: rgba(255, 255, 255, 0.8); /* Adds a slight white background to text for better readability */
        border-radius: 15px;
        padding: 20px;
        margin: auto;
        width: 80%;
        max-width: 1200px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .title {
        color: #009999;
        font-family: 'Arial', sans-serif;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #009999;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stTextInput input {
        font-size: 18px;
        padding: 10px;
        border: 1px solid #009999;
        border-radius: 5px;
    }
    .stNumberInput input {
        font-size: 18px;
        padding: 10px;
        border: 1px solid #009999;
        border-radius: 5px;
    }
    .stTextInput>label, .stNumberInput>label {
        color: #000000;
        font-size: 20px;
        font-weight: bold;
    }
    .stSelectbox {
        font-size: 18px;
    }
    .form-label {
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True
)


# File uploader
uploaded_file = st.file_uploader("Upload your CSV file 📁", type=["csv"])

# Function to clean and preprocess the data
def clean_data(uploaded_file):
    try:
        # Try reading the CSV file with different encodings
        encodings = ['utf-8', 'latin1', 'iso-8859-1']
        for encoding in encodings:
            try:
                df = pd.read_csv(uploaded_file, encoding=encoding)
                break
            except Exception as e:
                last_exception = e
        else:
            st.error(f"Error processing the file: {last_exception}")
            return pd.DataFrame()

        # Drop columns if they exist in the dataframe
        columns_to_drop = ['summary', 'space', 'description', 'neighborhood_overview', 'notes', 'transit',
                           'access', 'interaction', 'house_rules', 'cancellation_policy', 'last_scraped',
                           'calendar_last_scraped', 'weekly_price', 'monthly_price', 'cleaning_fee', 'images',
                           'listing_url']
        df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

        # Drop rows with missing 'name' or 'first_review'
        df.dropna(subset=['name', 'first_review'], inplace=True)

        # Fill missing values
        df['reviews_per_month'].fillna(df['reviews_per_month'].mean(), inplace=True)
        df['security_deposit'].fillna(df['security_deposit'].mean(), inplace=True)
        df['bedrooms'].fillna(df['bedrooms'].mean(), inplace=True)
        df['beds'].fillna(df['beds'].mean(), inplace=True)
        df['bathrooms'].fillna(df['bathrooms'].mean(), inplace=True)

        # Parse 'host' column
        if 'host' in df.columns:
            df['host'] = df['host'].apply(lambda x: ast.literal_eval(x))
            df['host_id'] = df['host'].apply(lambda x: x.get('host_id'))
            df['host_name'] = df['host'].apply(lambda x: x.get('host_name'))
            df['host_location'] = df['host'].apply(lambda x: x.get('host_location'))
            df['host_neighbourhood'] = df['host'].apply(lambda x: x.get('host_neighbourhood'))
            df['host_listings_count'] = df['host'].apply(lambda x: x.get('host_listings_count'))
            df['host_total_listings_count'] = df['host'].apply(lambda x: x.get('host_total_listings_count'))
            df.drop(columns=['host'], inplace=True)

        # Parse 'reviews' column
        if 'reviews' in df.columns:
            df['reviews'] = df['reviews'].str.strip('[]').str.split(',')
            for key in ['reviewer_name', 'comments']:
                df[key] = df['reviews'].apply(lambda reviews_list: [review.split(':')[1].strip().strip("'\"") if len(review.split(':')) > 1 else None for review in reviews_list if key in review])
            df.drop(columns=['reviews'], inplace=True)

        # Parse 'review_scores' column
        if 'review_scores' in df.columns:
            df['review_scores'] = df['review_scores'].apply(ast.literal_eval)
            df['review_scores_accuracy'] = df['review_scores'].apply(lambda x: x.get('review_scores_accuracy'))
            df['review_scores_cleanliness'] = df['review_scores'].apply(lambda x: x.get('review_scores_cleanliness'))
            df['review_scores_checkin'] = df['review_scores'].apply(lambda x: x.get('review_scores_checkin'))
            df['review_scores_communication'] = df['review_scores'].apply(lambda x: x.get('review_scores_communication'))
            df['review_scores_location'] = df['review_scores'].apply(lambda x: x.get('review_scores_location'))
            df['review_scores_value'] = df['review_scores'].apply(lambda x: x.get('review_scores_value'))
            df['review_scores_rating'] = df['review_scores'].apply(lambda x: x.get('review_scores_rating'))
            df.drop(columns=['review_scores'], inplace=True)
            # Drop rows with missing review scores
            review_score_columns = ['review_scores_value', 'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_checkin', 'review_scores_rating']
            df.dropna(subset=review_score_columns, inplace=True)

        # Parse 'availability' column
        if 'availability' in df.columns:
            df['availability'] = df['availability'].apply(ast.literal_eval)
            df['availability_30'] = df['availability'].apply(lambda x: x.get('availability_30'))
            df['availability_60'] = df['availability'].apply(lambda x: x.get('availability_60'))
            df['availability_90'] = df['availability'].apply(lambda x: x.get('availability_90'))
            df['availability_365'] = df['availability'].apply(lambda x: x.get('availability_365'))
            df.drop(columns=['availability'], inplace=True)

        # Parse 'address' column
        if 'address' in df.columns:
            df['address'] = df['address'].apply(ast.literal_eval)
            df['street'] = df['address'].apply(lambda x: x.get('street'))
            df['suburb'] = df['address'].apply(lambda x: x.get('suburb'))
            df['government_area'] = df['address'].apply(lambda x: x.get('government_area'))
            df['market'] = df['address'].apply(lambda x: x.get('market'))
            df['country'] = df['address'].apply(lambda x: x.get('country'))
            df['country_code'] = df['address'].apply(lambda x: x.get('country_code'))
            df['latitude'] = df['address'].apply(lambda x: x.get('location', {}).get('coordinates', [None, None])[0])
            df['longitude'] = df['address'].apply(lambda x: x.get('location', {}).get('coordinates', [None, None])[1])
            df.drop(columns=['address'], inplace=True)

        return df
    except Exception as e:
        st.error(f"Error processing the file: {e}")
        return pd.DataFrame()

# Function to create geospatial visualization
def create_geospatial_viz(df):
    fig = px.scatter_geo(df, lat='latitude', lon='longitude', color='price', hover_name='name',
                         size='price', projection='natural earth')
    fig.update_geos(showland=True, landcolor='rgb(243, 243, 243)', countrycolor='white')
    fig.update_layout(title='🌍 Airbnb Listings Worldwide',
                      geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
                      margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)

# Function to create price analysis visualization
def create_price_analysis(df):
    st.header("Price Analysis")
    
    fig = px.histogram(df, x="price", color="country", marginal="box", title="Price Distribution Across Different Countries")
    fig.update_layout(title_font_size=20, xaxis_title='Price', yaxis_title='Count')
    st.plotly_chart(fig, use_container_width=True)
    
    fig = px.box(df, x="property_type", y="price", title="Price Variation Across Property Types")
    fig.update_layout(title_font_size=20, xaxis_title='Property Type', yaxis_title='Price')
    st.plotly_chart(fig, use_container_width=True)
    
    df['first_review'] = pd.to_datetime(df['first_review'], errors='coerce')
    df['month'] = df['first_review'].dt.month
    fig = px.box(df, x='month', y='price', title='Price Trends Over Months')
    fig.update_layout(title_font_size=20, xaxis_title='Month', yaxis_title='Price')
    st.plotly_chart(fig, use_container_width=True)

# Function to create availability analysis visualization
def create_availability_analysis(df, availability_duration):
    st.header("Availability Analysis")
    
    df['first_review'] = pd.to_datetime(df['first_review'], errors='coerce')
    df['year'] = df['first_review'].dt.year
    
    availability_col = {
        '30': 'availability_30',
        '60': 'availability_60',
        '90': 'availability_90',
        '365': 'availability_365'
    }.get(availability_duration, 'availability_365')
    
    title = f'Availability Histogram for {availability_duration} Days'
    fig = px.histogram(df, x='year', y=availability_col, title=title)
    fig.update_layout(title_font_size=20, xaxis_title='Year', yaxis_title='Availability')
    st.plotly_chart(fig, use_container_width=True)
    
    heatmap_data = df.groupby(['country', 'year'])[availability_col].mean().reset_index()
    heatmap_fig = px.imshow(heatmap_data.pivot(index='country', columns='year', values=availability_col),
                            labels=dict(x="Year", y="Country", color="Availability"),
                            title=f'Availability Heatmap for {availability_duration} Days by Year',
                            color_continuous_scale='Viridis')
    heatmap_fig.update_layout(title_font_size=20)
    st.plotly_chart(heatmap_fig, use_container_width=True)

# Function to create region-based price distribution visualization
def create_region_price_distribution(df):
    st.header("Region-Based Price Distribution")
    
    regions = df['host_location'].unique()
    selected_region = st.selectbox("Select Region or Neighborhood", regions, index=0)
    
    region_data = df[df['host_location'] == selected_region]
    
    fig = px.histogram(region_data, x="price", title=f"Price Distribution in {selected_region}")
    fig.update_layout(title_font_size=20, xaxis_title='Price', yaxis_title='Count')
    st.plotly_chart(fig, use_container_width=True)

# Function to create filtered analysis visualization
def create_filtered_analysis(df):
    st.header("Filtered Analysis")
    
    selected_region = st.selectbox("Select Region or Neighborhood", ["All"] + list(df['host_location'].unique()))
    selected_property_type = st.selectbox("Select Property Type", ["All"] + list(df['property_type'].unique()))
    
    filtered_df = df.copy()
    if selected_region != "All":
        filtered_df = filtered_df[filtered_df['host_location'] == selected_region]
    if selected_property_type != "All":
        filtered_df = filtered_df[filtered_df['property_type'] == selected_property_type]
    
    fig = px.histogram(filtered_df, x="price", title="Price Distribution")
    fig.update_layout(title_font_size=20, xaxis_title='Price', yaxis_title='Count')
    st.plotly_chart(fig, use_container_width=True)

# Main app logic
if uploaded_file is not None:
    st.write("File uploaded successfully! 🎉")
    df = clean_data(uploaded_file)
    
    if not df.empty:
        st.write("## Explore the Data")
        st.write("### Geospatial Visualization")
        create_geospatial_viz(df)
        
        st.write("### Price Analysis")
        create_price_analysis(df)
        
        st.write("### Availability Analysis")
        availability_duration = st.selectbox("Select Availability Duration", ['30', '60', '90', '365'])
        create_availability_analysis(df, availability_duration)
        
        st.write("### Region-Based Price Distribution")
        create_region_price_distribution(df)
        
        st.write("### Filtered Analysis")
        create_filtered_analysis(df)
    else:
        st.write("The data could not be processed. Please check the file format and try again.")
else:
    st.write("Please upload a CSV file to proceed. 📂")
