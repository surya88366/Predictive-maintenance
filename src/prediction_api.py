from flask import Flask, request, jsonify
import pickle
import numpy as np
import time

app = Flask(__name__)

try:
    model = pickle.load(open('src/model.pkl', 'rb'))
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

appliance_map = {'fan': 0, 'ac': 1, 'washing_machine': 2}
latest_predictions = {}  # Global dictionary to store the latest prediction for each appliance

@app.route('/predict', methods=['POST'])
def predict():
    global latest_predictions
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    try:
        data = request.get_json()
        appliance = data.get("appliance")
        vibration = float(data.get("vibration"))
        temperature = float(data.get("temperature"))
        current = float(data.get("current"))
        
        if appliance not in appliance_map:
            return jsonify({"error": "Invalid appliance type"}), 400
        
        features = np.array([[vibration, temperature, current, appliance_map[appliance]]])
        prediction = model.predict(features)[0]
        result = {"needs_service": bool(prediction)}
        
        # Store the latest prediction and data for the specific appliance
        latest_predictions[appliance] = {
            "appliance": appliance,
            "vibration": vibration,
            "temperature": temperature,
            "current": current,
            "needs_service": bool(prediction),
            "timestamp": time.time()
        }
        return jsonify(result)
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return jsonify({"error": "Server error"}), 500

@app.route('/latest_prediction', methods=['GET'])
def get_latest_prediction():
    return jsonify(latest_predictions)

if __name__ == '__main__':
    app.run(debug=True)