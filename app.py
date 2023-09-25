from scipy.optimize import differential_evolution
from qsp.optimization import objective_function, predict_1_day_strength, optimize
import joblib


features = ['Source', 'Product Type', 'CO2', 'Belite Sum', 'Alite Sum', 'Quartz', 'Gypsum', 'MgO', '325 Mesh Pass', 'D50', 'HemiHydrate', 'CaO', 'D90', 'Fe2O3', 'SO3', 'Alite M1', 'Al2O3', 'Arcanite', 'Blaine', 'K2O', 'Na2O', 'Belite Beta', 'D10', 'Aphthitalite', 'Belite Alpha', 'Belite Gamma', 'Alum Cubic', 'Alum Ortho', 'Alum Sum', 'Alite M3', 'Ferrite', 'Calcite', 'Langbeinite', 'Lime', 'Periclase', 'Portlandite', 'Fraction M1', 'SiO2']
inputs = data[features].iloc[0, :]
model = joblib.load(r"C:\Users\p.georgakis\Downloads\Alcemy_ExtraTrees_(38 inputs)_v0.cls")
target_1_day_strength = 2200
bounds = [(97, 99)]
# Perform differential evolution optimization
result = differential_evolution(objective_function, 
                                bounds=bounds,
                                args=(target_1_day_strength, inputs, model))

# Extract the optimized value for "325 Mesh Pass"
optimized_325_mesh_pass = result.x[0]
optimized_325_mesh_pass = round(optimized_325_mesh_pass, 1)

print("Optimized 325 Mesh Pass value:", optimized_325_mesh_pass)

predicted_1_day_strength = predict_1_day_strength(mesh_pass=optimized_325_mesh_pass, inputs=inputs, model=model)
predicted_1_day_strength = round(predicted_1_day_strength, 1)

print("Predicted 1 Day Strength for Optimized 325 Mesh Pass:", predicted_1_day_strength, 'psi')

optimized_values = optimize(data=data[features][:5],
                            bounds=bounds, 
                            target_1_day_strength=target_1_day_strength, 
                            model=model)