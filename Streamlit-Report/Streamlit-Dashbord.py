from cmath import exp
from email.utils import collapse_rfc2231_value
from lib2to3.pgen2.pgen import DFAState
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import folium 
import geopandas
import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage



from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from datetime import datetime

st.set_page_config(layout='wide')

@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)


    return data



@st.cache(allow_output_mutation=True)
def convert_data(data):
    return data.to_csv()

# Create API client.
credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])

client = storage.Client(credentials= credentials)

@st.experimental_memo(ttl=600)
def read_file(bucket_name, file_path):
    bucket = client.bucket(bucket_name)
    content = bucket.blob(file_path).download_as_string().decode("utf-8")
    return content


# functions
def get_data(path):
    data = pd.read_csv(path)


    return data

def transform(data):
    # Data types
    data['date'] = pd.to_datetime(data['date'])
    # Cleaning
    data.loc[data['bedrooms']==33,'bedrooms'] = data['bedrooms'].median()
    data = data[(data['bedrooms']!=0) | (data['bathrooms'] != 0)]
    data = data.sort_values('date', ascending=False)
    data = data.drop_duplicates('id')

    # Set features
    data['month-day'] = data['date'].dt.strftime('%m-%d')
    data['season_year'] = data['month-day'].apply(lambda x: 'summer' if x >= '06-21' and x < '09-22' else     
                                                      'fall' if x >= '09-22' and x < '12-21' else 
                                                      'spring' if x >= '03-20' and x < '06-20' else
                                                      'winter')
    price_reg_grouped = data[['price','zipcode']].groupby('zipcode').median().reset_index()
    m1 = data.merge(price_reg_grouped, on=['zipcode'], validate='many_to_one', how='inner')                                       
    price_regssn_grouped = m1[['price_x','season_year', 'zipcode']].groupby(['zipcode','season_year']).median().reset_index()
    m2 = m1.merge(price_regssn_grouped, on=['zipcode','season_year'],validate= 'many_to_one', how='inner')
    m2.columns = ['id', 'date', 'price', 'bedrooms', 'bathrooms', 'sqft_living',
       'sqft_lot', 'floors', 'waterfront', 'view', 'condition', 'grade',
       'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated', 'zipcode',
       'lat', 'long', 'sqft_living15', 'sqft_lot15', 'month-day',
       'season_year', 'median_price', 'median_s_price']
    data = m2.copy()
    data['status'] = data.apply(lambda x: 'buy' if x['price'] < x['median_price'] and x['condition'] >= 3 else 'do not buy' ,axis = 1)
    data['sale_price'] = data.apply(lambda x: 1.3*x['price'] if x['price'] > x['median_s_price'] else 1.1*x['price'], axis=1)
    data['profit'] = data.apply(lambda x: x['sale_price'] - x['price'], axis=1)

    data['sqft_diff15_num'] = data.apply(lambda x: x['sqft_living'] - x['sqft_living15'], axis = 1)
    data['renovation_space'] = data.apply(lambda x: x['sqft_lot']-x['sqft_living'], axis=1)
    data['renovation'] = data.apply(lambda x: 'yes' if (x['sqft_diff15_num'] < 0)  & ((x['sqft_lot']-x['sqft_living']) > 0) else 'no', axis= 1 )
    data['renovation_area'] = data.apply(lambda x: x['sqft_diff15_num']*(-1) if (x['renovation'] == 'yes') and (x['sqft_diff15_num']*(-1) <= 0.25*x['sqft_living']) else
                                             0.25*x['sqft_living'] if (x['renovation'] == 'yes') and (x['sqft_diff15_num']*(-1) > 0.25*x['sqft_living']) else
                                             0, axis=1 )
    data['sqft_price'] = data.apply(lambda x: x['price']/x['sqft_living'], axis=1)
    data['price_increasing'] = data.apply(lambda x: x['sqft_price']*x['renovation_area'], axis=1)
    data['sale_price_renovated'] = data.apply(lambda x: x['sale_price'] + x['price_increasing'], axis=1)
    data['profit_renovated'] = data.apply(lambda x: x['sale_price_renovated']-x['price'], axis=1)

    return data
    

def filters(data):

    min_price = int(data['price'].min())
    max_price = int(data['price'].max())
    avg_price = int(data['price'].mean())

    st.sidebar.title('Filters')

    f_price = st.sidebar.number_input(label='Insert the max price you want to filter. Min: {} Max: {}'.format(min_price, max_price),min_value=min_price,max_value=max_price,value=avg_price)

    #f_price = st.sidebar.slider('Filter by Price', min_price, max_price, avg_price)
    
    f_zipcode = st.sidebar.multiselect('Enter zipcode', data['zipcode'].unique())
    
    f_bedrooms = st.sidebar.selectbox('Max number of bedrooms',
                                      sorted(set(data['bedrooms'].unique()),reverse=True))

    f_bathrooms = st.sidebar.selectbox('Max number of bathrooms',
                                       sorted(set(data['bathrooms'].unique()),reverse=True))    

    f_waterview = st.sidebar.checkbox('Only houses with water view')

    
    return f_price, f_zipcode, f_bedrooms, f_bathrooms, f_waterview



def overview(data):
    st.title("House Rocket's Dashboard")

    st.markdown("# Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(label="Number of Properties", value=data.shape[0])
    c2.metric(label='Average Price', value=round(data['price'].mean(),1))
    c3.metric(label='Purchase Recomendations', value=data[data['status'] == 'buy'].shape[0])
    c4.metric(label='Recommended Renovations', value=data[(data['status'] == 'buy') & (data['renovation'] == 'yes')].shape[0])

    data = data.copy()
    # Filtering
    if f_waterview == True:
        data = data[data['waterfront'] == 1]
        if (f_zipcode != []):
            data = data[(data['price'] <= f_price) & (data['bedrooms'] <= f_bedrooms) & 
                    (data['bathrooms'] <= f_bathrooms) & (data['zipcode'].isin(f_zipcode))]
        else:
            data = data[(data['price'] <= f_price) & (data['bedrooms'] <= f_bedrooms) & 
                    (data['bathrooms'] <= f_bathrooms)]
    else:
        data = data.copy()
        if (f_zipcode != []):
            data = data[(data['price'] <= f_price) & (data['bedrooms'] <= f_bedrooms) & 
                    (data['bathrooms'] <= f_bathrooms) & (data['zipcode'].isin(f_zipcode))]
        else:
            data = data[(data['price'] <= f_price) & (data['bedrooms'] <= f_bedrooms) & 
                    (data['bathrooms'] <= f_bathrooms)]
    

    #c1, c2= st.columns(2)

    fig = px.scatter_mapbox(data,
                            lat='lat',
                            lon='long',
                            hover_name='id',
    #                       size='sqft_price',
                            color='price',
                            color_continuous_scale= px.colors.cyclical.IceFire,
                            size_max=20,
                            zoom=10)
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(height=600,margin={'r':0,'t':0,'b':0,'l':0})

    st.markdown("### House Rocket's Portfolio")
    st.write("The Overview Map below allows you to see all the properties and the price distribution by regions")
    st.plotly_chart(fig)

# ==============================================================================================================
# TAB 1
# ==============================================================================================================

def business_report(data):
    # Density Maps

    st.markdown("# Business Report")

    tab1, tab2 = st.tabs(['Map Report','🗃 Data Reports'])

    tab1.subheader('Portfolio Density')

    tab1.write("Here you can visualize the properties in the region. If it's a purchase recomendation, it will be indicated in the popup.")
    tab1.write('Or else you can filter it below')

    check_status = tab1.checkbox("Show only purchase recommendations")

    if check_status == True:
        data = data[data['status'] == 'buy']
    else:
        data = data.copy()

    # Base Map - Folium
    
    density_map = folium.Map(location=[data['lat'].mean(),
                                    data['long'].mean()],
                            default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in data.iterrows():
        folium.Marker([row['lat'], row['long']],
                    popup ='Sale Price R${0} on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, status: {5}'.format(row['price'],
                                                                                                                        row['season_year'],
                                                                                                                        row['sqft_living'],
                                                                                                                        row['bedrooms'],
                                                                                                                        row['bathrooms'],
                                                                                                                        row['status'])).add_to(marker_cluster)
    
    with tab1:
        folium_static(density_map)
    
    return data
# ==============================================================================================================
# TAB 2
# ==============================================================================================================

    tab2.subheader("Purchase Recommendations")
    tab2.write('The table below contains the properties, as well as their purchase suggestion')

    report1 = data[['id','zipcode','price','status']]

    csv = convert_data(report1)
    tab2.download_button(label="Download.csv",
            data=csv,
            file_name='recommendation_report.csv',
            mime='text/csv')

    tab2.dataframe(data=report1, width=800)
# ==============================================================================================================
    tab2.subheader("Sale Prices Recommendations")
    tab2.write('The table below contains the properties recommended, their sale prices and the season of sale')

    report2 = data[['id','zipcode','price','season_year','sale_price','profit']]

    csv = convert_data(report2)
    tab2.download_button(label="Download.csv",
            data=csv,
            file_name='sales_price_report.csv',
            mime='text/csv')

    tab2.dataframe(data=report2, width=800)
# ==============================================================================================================
    tab2.subheader("Renovation Recommendations")
    tab2.write('The table below contains the properties and renovations recommended. It also shows the new sale price in case of home renovations.')

    report3 = data[['id','zipcode','price','renovation','sale_price_renovated','profit_renovated']]

    csv = convert_data(report3)
    tab2.download_button(label="Download.csv",
            data=csv,
            file_name='renovation_report.csv',
            mime='text/csv')

    tab2.dataframe(data=report3, width=800)
# ==============================================================================================================

if __name__ == '__main__':
    # ETL
    # Data Extraction
    path = "gs://house-apps-sales/kc_house_data.csv"
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

    bucket_name = "house-apps-sales"
    file_path = "kc_house_data.csv"
    
    data = read_file(bucket_name, file_path)

    # Transformation

    data = transform(data)
    
    f_price, f_zipcode, f_bedrooms, f_bathrooms, f_waterview = filters(data)

    # Load
    data = overview(data)
    business_report(data)



