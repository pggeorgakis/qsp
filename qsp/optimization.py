import numpy as np
from scipy.optimize import differential_evolution
import streamlit as st


# Define your model function that takes inputs and returns the predicted 28 day strength
def predict_1_day_strength(mesh_pass, inputs, model):
    inputs['325 Mesh Pass'] = mesh_pass
    inputs = inputs.values.reshape(1, -1)
    pred = model.predict(inputs)[0]
    return pred[0] # 0 for 1 Day Strength


# Define the objective function to minimize (mean squared error between predicted and target strengths)
def objective_function(mesh_pass, target_strength, fixed_inputs, model):
    predicted_strength = predict_1_day_strength(mesh_pass, fixed_inputs, model)
    return (predicted_strength - target_strength)**2


def optimize(data, target_1_day_strength, bounds, model):
    optimized_values = []
    for _, inputs in data.iterrows():
        result = differential_evolution(objective_function, 
                                        bounds=bounds,
                                        args=(target_1_day_strength, inputs, model))
        optimized_325_mesh_pass = result.x[0]
        optimized_325_mesh_pass = round(optimized_325_mesh_pass, 1)
        optimized_values.append(optimized_325_mesh_pass)
    return optimized_values


def get_strength_predictions(optimized_values, inputs, model):
    predicted_values = []
    for i, mesh_pass in enumerate(optimized_values):
        prediction = predict_1_day_strength(mesh_pass=mesh_pass, 
                                            inputs=inputs.iloc[i], 
                                            model=model)
        
        prediction = round(prediction, 1)
        predicted_values.append(prediction)
    return predicted_values


def run_optimization(inputs, models, target_1_day_strength):

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
    predicted_values = {}
    predicted_values['1d'] = np.round(np.random.uniform(2000, 2400, size=len(inputs)), 1)
    predicted_values['7d'] = np.round(np.random.uniform(5000, 5500, size=len(inputs)), 1)
    predicted_values['28d'] = np.round(np.random.uniform(7000, 7500, size=len(inputs)), 1)
    return optimized_values, predicted_values
