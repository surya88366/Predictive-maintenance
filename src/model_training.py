# src/model_training.py
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

np.random.seed(42)

appliances = {
    'fan': {'normal_vib': (40, 5), 'fault_vib': (70, 10), 'normal_temp': (35, 2), 'fault_temp': (50, 5), 'normal_curr': (1.2, 0.2), 'fault_curr': (2.5, 0.3)},
    'ac': {'normal_vib': (30, 3), 'fault_vib': (60, 8), 'normal_temp': (22, 1.5), 'fault_temp': (35, 4), 'normal_curr': (3.5, 0.5), 'fault_curr': (5.0, 0.7)},
    'washing_machine': {'normal_vib': (60, 10), 'fault_vib': (90, 15), 'normal_temp': (40, 3), 'fault_temp': (55, 5), 'normal_curr': (2.0, 0.4), 'fault_curr': (3.5, 0.6)}
}

rows = []
total_data_points = 5000

for appliance, ranges in appliances.items():
    vibration_val = ranges['normal_vib'][0]
    temperature_val = ranges['normal_temp'][0]
    current_val = ranges['normal_curr'][0]

    for i in range(total_data_points):
        needs_service = 0
        
        if i > 4500:
            needs_service = 1
            
        vibration_change = np.random.normal(0, 0.1)
        temperature_change = np.random.normal(0, 0.05)
        current_change = np.random.normal(0, 0.02)
        
        vibration_val += vibration_change
        temperature_val += temperature_change
        current_val += current_change
        
        if needs_service:
            vibration_val = np.random.normal(ranges['fault_vib'][0], ranges['fault_vib'][1])
            temperature_val = np.random.normal(ranges['fault_temp'][0], ranges['fault_temp'][1])
            current_val = np.random.normal(ranges['fault_curr'][0], ranges['fault_curr'][1])
        else:
            vibration_val = np.random.normal(ranges['normal_vib'][0], ranges['normal_vib'][1])
            temperature_val = np.random.normal(ranges['normal_temp'][0], ranges['normal_temp'][1])
            current_val = np.random.normal(ranges['normal_curr'][0], ranges['normal_curr'][1])
            
        vibration_val = max(0, vibration_val)
        temperature_val = max(0, temperature_val)
        current_val = max(0, current_val)
        
        rows.append([appliance, vibration_val, temperature_val, current_val, needs_service])

df = pd.DataFrame(rows, columns=['appliance', 'vibration', 'temperature', 'current', 'needs_service'])
os.makedirs('data', exist_ok=True)
df.to_csv('data/synthetic_data.csv', index=False)
le = LabelEncoder()
df['appliance_encoded'] = le.fit_transform(df['appliance'])
X = df[['vibration', 'temperature', 'current', 'appliance_encoded']]
y = df['needs_service']
model = RandomForestClassifier()
model.fit(X, y)
os.makedirs('src', exist_ok=True)
with open('src/model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("✅ Synthetic data generated and model trained successfully.")