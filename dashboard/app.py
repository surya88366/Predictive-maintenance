import streamlit as st
import requests
import time

st.title("Appliance Health Monitor (Live Feed)")

# Function to get all latest data from the API
def get_all_appliance_data():
    try:
        response = requests.get("http://127.0.0.1:5000/latest_prediction")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        st.error("Request failed. Ensure the Flask API is running.")
        return {}

# Health Calculation Logic
def calculate_health(vibration, temperature, current, appliance_name):
    health = 100
    if appliance_name == 'fan':
        if vibration > 60: health -= (vibration - 60) * 1.5
        if temperature > 45: health -= (temperature - 45) * 2
        if current > 2.0: health -= (current - 2.0) * 15
    elif appliance_name == 'ac':
        if vibration > 50: health -= (vibration - 50) * 1.2
        if temperature > 30: health -= (temperature - 30) * 2.5
        if current > 4.5: health -= (current - 4.5) * 10
    elif appliance_name == 'washing_machine':
        if vibration > 80: health -= (vibration - 80) * 0.8
        if temperature > 50: health -= (temperature - 50) * 1.8
        if current > 3.0: health -= (current - 3.0) * 12
    return max(0, min(100, health))

# Fault Detection and Solution Logic
def get_fault_and_solution(vibration, temperature, current, appliance_name):
    fault_details = []
    solution_ideas = []
    if appliance_name == 'fan':
        if vibration > 60:
            fault_details.append("High vibration detected in the motor or blades.")
            solution_ideas.append("Check for unbalanced blades or loose motor mounts.")
        if temperature > 45:
            fault_details.append("High temperature detected, possibly due to motor friction.")
            solution_ideas.append("Clean air vents and ensure adequate airflow to the motor.")
        if current > 2.0:
            fault_details.append("High current draw, indicating a potential electrical fault.")
            solution_ideas.append("Inspect wiring for shorts and verify the motor's health.")
    elif appliance_name == 'ac':
        if vibration > 50:
            fault_details.append("Unusual vibration in the compressor or fan unit.")
            solution_ideas.append("Inspect the compressor mounts and clean the fan blades.")
        if temperature > 30:
            fault_details.append("High operating temperature, indicating a cooling issue.")
            solution_ideas.append("Check refrigerant levels and clean the condenser coils.")
        if current > 4.5:
            fault_details.append("High current draw, possibly due to a failing compressor.")
            solution_ideas.append("Service the compressor and check for electrical shorts.")
    elif appliance_name == 'washing_machine':
        if vibration > 80:
            fault_details.append("Excessive vibration during spin cycle.")
            solution_ideas.append("Check for an unbalanced load or worn-out suspension springs.")
        if temperature > 50:
            fault_details.append("High water temperature or motor overheating.")
            solution_ideas.append("Verify the heating element is working correctly and inspect motor bearings.")
        if current > 3.0:
            fault_details.append("High current draw, suggesting a motor problem or jammed drum.")
            solution_ideas.append("Inspect the motor and check for obstructions in the drum.")
    return fault_details, solution_ideas

# Main dashboard logic with tabs
tab_names = ["Fan", "AC", "Washing Machine"]
tabs = st.tabs(tab_names)
placeholders = {name: tab.empty() for name, tab in zip(tab_names, tabs)}

while True:
    all_data = get_all_appliance_data()
    
    for appliance_name, placeholder in placeholders.items():
        data = all_data.get(appliance_name.lower().replace(" ", "_"))
        
        with placeholder.container():
            if data:
                vibration = data['vibration']
                temperature = data['temperature']
                current = data['current']
                needs_service = data['needs_service']
                
                # Display Health Bar
                health_score = calculate_health(vibration, temperature, current, appliance_name.lower().replace(" ", "_"))
                st.subheader(f"{appliance_name} Health")
                st.progress(int(health_score / 100 * 100))
                st.write(f"**Health Score:** {health_score:.2f}%")
                
                # Display Sensor Readings
                st.write(f"**Current Readings:**")
                st.write(f"Vibration: {vibration:.2f} | Temperature: {temperature:.2f} | Current: {current:.2f}")

                # Fault Detection
                st.subheader("Fault Diagnosis")
                faults, solutions = get_fault_and_solution(vibration, temperature, current, appliance_name.lower().replace(" ", "_"))
                
                if faults:
                    for fault in faults:
                        st.error(f"**Fault:** {fault}")
                    st.write("**Recommended Solution:**")
                    for solution in solutions: 
                        st.info(f"**-** {solution}")
                else:
                    st.success("No significant faults detected.")

                if needs_service:
                    st.warning("⚠️ **Prediction:** This appliance needs service based on the ML model.")
                else:
                    st.success("✅ **Prediction:** This appliance is operating normally.")
            else:
                st.info(f"Waiting for data from the {appliance_name} simulator.")
    
    time.sleep(2)