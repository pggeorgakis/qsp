import warnings
import streamlit as st
import numpy as np
import pandas as pd
from qsp.core import read_data, filter_data, load_models, select_inputs, replace_zeros
from qsp.optimization import run_optimization
from qsp.plotting import combined_plot


warnings.filterwarnings("ignore", category=UserWarning)

st.set_page_config(page_title="Quality Target Optimization v0.5", 
                   page_icon=":dart:", 
                   layout="wide")

# Title
st.title("Quality Target Optimization")

# Read data and load models at the beginning
data = read_data()
models = load_models()

tab1, tab2, tab3, tab4 = st.tabs(['Analysis',
               'Control Room',
               'Recipe Management',
               'Help'])

with tab1:
    col1, col2 = st.columns([0.2, 1.4])
    col1.write("Settings")
    
    # FIXME: Check types
    source_options = {'FM3': 0, 'FM4': 1, 'FM6': 2}
    product_type_options = {'GU': 0, 'I/II': 1, 'CEM IL': 2, 'Masonry': 3, 'Stucco': 4}

    # Set default start and end dates to the first and last values of the data
    default_start_date = pd.to_datetime(data.index.min())
    default_end_date = pd.to_datetime(data.index.max())

    # Select Source and Product Type
    product_type = col1.selectbox("Recipe", list(product_type_options.keys()), index=2)
    source = col1.selectbox("Sample site", list(source_options.keys()), index=1)

    # Create a sidebar column layout for the date pickers
    date_col1, date_col2 = col1.columns(2)
    # Date Picker for time period with default values
    with date_col1:
        start_date = st.date_input("Start Date", default_start_date)
        start_date = pd.to_datetime(start_date)

    with date_col2:
        end_date = st.date_input("End Date", default_end_date)
        end_date = pd.to_datetime(end_date)
        
    # Filter data based on Source and Product Type
    source_code = source_options[source]
    product_type_code = product_type_options[product_type]

    data_filtered = filter_data(data, source_code, product_type_code)
    
    # Filter data by time period
    data_filtered = data_filtered[(data_filtered.index >= start_date) & (data_filtered.index <= end_date)]

    # data_filtered = data_filtered.iloc[0:3, :]
    # Select model inputs
    inputs = select_inputs(data_filtered, models['xrd'])
    
    # FIXME: Auto optimization tba
    # if st.sidebar.button("Run Optimization"):
    optimized_values, predicted_values = run_optimization(inputs, models, target_1_day_strength=2200)
    
    data_filtered['325 Mesh Pass Optimized'] = optimized_values
    data_filtered['1 Day Strength Pred.'] = predicted_values['1d']
    data_filtered['7 Day Strength Pred.'] = predicted_values['7d']
    data_filtered['28 Day Strength Pred.'] = predicted_values['28d']
    
    fig = combined_plot(data_filtered)
    col2.plotly_chart(fig)
    
    # Show data table
    st.write(inputs)
    csv = inputs.to_csv().encode('utf-8')

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='data.csv',
        mime='text/csv')


with tab2:
    st.header("Under construction...")
    
    
with tab3:
    col3, col4 = st.columns([0.2, 1.4])
    target_1_day_strength = col3.number_input("Target 1-Day Strength", value=2200)
    
    st.header("Under construction...")
    
with tab4:
    st.write("Under construction...")


