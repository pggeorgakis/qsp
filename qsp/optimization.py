from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error
from scipy.optimize import differential_evolution

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
    for _, inputs in tqdm_notebook(data.iterrows(), total=len(data)):
        result = differential_evolution(objective_function, 
                                        bounds=bounds,
                                        args=(target_1_day_strength, inputs, model))
        optimized_325_mesh_pass = result.x[0]
        optimized_325_mesh_pass = round(optimized_325_mesh_pass, 1)
        optimized_values.append(optimized_325_mesh_pass)
    return optimized_values