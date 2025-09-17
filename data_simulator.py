# data_simulator.py
import requests
import time
import random
import numpy as np

APPLIANCES = {
    "fan": {"vibration": 40, "temperature": 35, "current": 1.2},
    "ac": {"vibration": 30, "temperature": 22, "current": 3.5},
    "washing_machine": {"vibration": 60, "temperature": 40, "current": 2.0},
}

def simulate_stream():
    while True:
        appliance = random.choice(list(APPLIANCES.keys()))
        baseline = APPLIANCES[appliance]
        fault = np.random.rand() < 0.1
        
        if fault:
            vibration = np.random.normal(baseline['vibration'] * 1.5, 10)
            temperature = np.random.normal(baseline['temperature'] * 1.5, 5)
            current = np.random.normal(baseline['current'] * 1.5, 1)
        else:
            vibration = np.random.normal(baseline['vibration'], 5)
            temperature = np.random.normal(baseline['temperature'], 2)
            current = np.random.normal(baseline['current'], 0.2)
        
        payload = {
            "appliance": appliance,
            "vibration": max(0, vibration),
            "temperature": max(0, temperature),
            "current": max(0, current),
        }
        
        try:
            response = requests.post("http://127.0.0.1:5000/predict", json=payload)
            response.raise_for_status()
            result = response.json()
            print(f"Sent {payload} | Prediction: {result}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        
        time.sleep(2)

if __name__ == '__main__':
    simulate_stream()