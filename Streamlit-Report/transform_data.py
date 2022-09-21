import pandas as pd

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

def load_data(data):
    data.to_csv('Streamlit-Report/data_transformed.csv') # saving data into Streamlit-Report folder



# ETL
# Data Extraction
path = "kc_house_data.csv"
data = get_data(path)

 # Transformation
data = transform(data)

# Load
load_data(data)    

