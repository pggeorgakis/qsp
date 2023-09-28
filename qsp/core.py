import numpy as np
import pandas as pd
import joblib
import streamlit as st


@st.cache_data
def read_data():
    data = pd.read_excel('asset/data/data.xlsx')
    data.index = pd.to_datetime(data['Sample recorded at'])
    
    variables = pd.read_csv('asset/variables.csv')

    # Replace column names based on variables.csv
    column_rename_dict = dict(zip(variables['Old name'], variables['New name']))
    data = data.rename(columns=column_rename_dict)
    
    # Map data columns "Source", "Product Type"
    data = map_data(data)
    return data
    

def map_data(data):
    mapping = {
    'Source': {'FM3': 0, 
               'FM4': 1, 
               'FM6': 2},
    'Product Type': {'GU': 0, 
                     'I/II': 1, 
                     'CEM IL': 2, 
                     'Masonry': 3, 
                     'Stucco': 4}
    }
    data['Source'] = data['Source'].replace(mapping['Source'])
    data['Product Type'] = data['Product Type'].replace(mapping['Product Type'])

    # Fill NA with zeros
    data = data.fillna(0)
    return data


def filter_data(data, source, product_type):
    data = data[(data['Source']==source) & 
                (data['Product Type']==product_type) &
                (data['325 Mesh Pass Target'] !=0)]
    data = data[[c for c in data.columns if 'Pred' not in c]]
    data['1 Day'] = data['1 Day']*1000
    data['7 Day'] = data['7 Day']*1000
    data['28 Day'] = data['28 Day']*1000
    return data


@st.cache_resource
def load_models():
    models = {}
    
    # Load model trained with XRD data
    model = joblib.load("asset/models/xrd/model_xrd.cls")
    models['xrd'] = model
    # Load model trained without XRD data
    model = joblib.load("asset/models/no_xrd/model_no_xrd.cls")
    models['no_xrd'] = model
    return models


def load_config():
    # 
    pass


def select_inputs(data, model):
    features = list(model.feature_names_in_)
    inputs = data[features]
    return inputs


def replace_zeros(inputs):
    inputs['325 Mesh Pass'] = inputs['325 Mesh Pass'].replace(0, np.nan)
    return inputs