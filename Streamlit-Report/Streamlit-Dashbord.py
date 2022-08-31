from cmath import exp
from email.utils import collapse_rfc2231_value
from lib2to3.pgen2.pgen import DFAState
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import folium 
import geopandas

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
    c4.metric(label='Recommended Renovations', value=data[data['renovation'] == 'yes'].shape[0])

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

    check_status = st.checkbox("Show only purchase recommendations")

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
    path = "data_transformed.csv"
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

    data = get_data(path)

    # Transformation
    
    f_price, f_zipcode, f_bedrooms, f_bathrooms, f_waterview = filters(data)

    # Load
    overview(data)
    business_report(data)



