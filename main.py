from art import tprint
import warnings
from qsp.core import read_data, filter_data, load_models, select_inputs, replace_zeros
from qsp.optimization import optimize, get_strength_predictions
from qsp.plotting import plot_mesh_pass, plot_strength


warnings.filterwarnings("ignore", category=UserWarning)

def main():
    # Initialize
    data = read_data()
    models = load_models()

    # Define Sample site
    source = 1
    # Define Product type
    product_type = 2
    # Filter data based on Sample site and Product type
    data_filtered = filter_data(data, source, product_type).iloc[0:3, :]

    # Select model inputs
    inputs = select_inputs(data_filtered, models['xrd'])

    # Define Day 1 Strength target
    target_1_day_strength = 2200
    # Define 325 Mesh Pass bounds
    bounds = [(97, 99)]

    # Run optimization using the model trained with XRD data
    model = models['xrd']
    optimized_values = optimize(data=inputs,
                                bounds=bounds, 
                                target_1_day_strength=target_1_day_strength, 
                                model=model)

    
    # Get the Strength 1-Day predictions using the optimized values of 325 Mesh Pass
    predicted_values = get_strength_predictions(optimized_values, inputs, model)
    data_filtered['1 Day Strength Pred.'] = predicted_values
    
    data_filtered['325 Mesh Pass Optimized'] = optimized_values
    data_filtered = replace_zeros(data_filtered)
    
    # Plot 325 Mesh Pass Optimized values
    plot_mesh_pass(data_filtered)
    plot_strength(data_filtered)
    
    
if __name__ == '__main__':
    tprint("QSP")
    main()
