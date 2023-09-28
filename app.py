import warnings
import streamlit as st
import numpy as np
import pandas as pd
from qsp.core import read_data, filter_data, load_models, select_inputs, replace_zeros
from qsp.optimization import optimize, get_strength_predictions
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

# Define Source and Product Type options
# FIXME: Check types
source_options = {'FM3': 0, 'FM4': 1, 'FM6': 2}
product_type_options = {'GU': 0, 'I/II': 1, 'CEM IL': 2, 'Masonry': 3, 'Stucco': 4}

# Set default start and end dates to the first and last values of the data
default_start_date = pd.to_datetime(data.index.min())
default_end_date = pd.to_datetime(data.index.max())

st.sidebar.header("Select Options")

# Select Source and Product Type
product_type = st.sidebar.selectbox("Recipe", list(product_type_options.keys()), index=2)
source = st.sidebar.selectbox("Sample site", list(source_options.keys()), index=1)

# Input for setting the target 1-day strength
target_1_day_strength = st.sidebar.number_input("Target 1-Day Strength", value=2200)

# Create a sidebar column layout for the date pickers
date_col1, date_col2 = st.sidebar.columns(2)
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

# Streamlit UI
def main():
    data_filtered = filter_data(data, source_code, product_type_code)
    
    # Filter data by time period
    data_filtered = data_filtered[(data_filtered.index >= start_date) & (data_filtered.index <= end_date)]

    # data_filtered = data_filtered.iloc[0:3, :]
    # Select model inputs
    inputs = select_inputs(data_filtered, models['xrd'])
    
    # FIXME: Auto optimization tba
    # if st.sidebar.button("Run Optimization"):
    optimized_values, predicted_values = run_optimization(inputs, target_1_day_strength)

    data_filtered['1 Day Strength Pred.'] = predicted_values
    data_filtered['325 Mesh Pass Optimized'] = optimized_values
    data_filtered = replace_zeros(data_filtered)
    
    fig = combined_plot(data_filtered)
    st.plotly_chart(fig)
    
    # Show data table
    st.write(inputs)
    csv = inputs.to_csv().encode('utf-8')

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='data.csv',
        mime='text/csv')
    
    
def run_optimization(inputs, target_1_day_strength):

    # Define 325 Mesh Pass bounds
    bounds = [(97, 99)]

    # Run optimization using the model trained with XRD data
    model = models['xrd']
    
    # FIXME: optimization temp disabled
    # optimized_values = optimize(data=inputs,
    #                             bounds=bounds, 
    #                             target_1_day_strength=target_1_day_strength, 
    #                             model=model)

    optimized_values = np.round(np.random.uniform(97, 100, size=len(inputs)), 1)
    
    # Get the Strength 1-Day predictions using the optimized values of 325 Mesh Pass
    # FIXME: predictions temp disabled
    # predicted_values = get_strength_predictions(optimized_values, inputs, model)
    predicted_values = np.round(np.random.uniform(2000, 2400, size=len(inputs)), 1)
    return optimized_values, predicted_values


if __name__ == '__main__':
    main()
