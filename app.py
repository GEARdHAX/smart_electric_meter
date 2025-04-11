import streamlit as st
import requests

st.set_page_config(page_title="Power Predictor", page_icon="⚡")
st.title("🔌 Power Consumption Predictor")

appliance = st.selectbox("Select Appliance", ["fan", "led_tv", "fridge"])

st.subheader("Enter Input Features:")
current = st.number_input("Current (A)", value=0.6, min_value=0.0, step=0.01)
voltage = st.number_input("Voltage (V)", value=220.0,
                          min_value=100.0, step=1.0)
on_off = st.selectbox("Device ON?", [1, 0])

features = [current, voltage, on_off]

predict_type = st.radio("What do you want to predict?", [
                        "1-hour Power Usage", "Next 30 Days (kWh)"])

unit_price = st.number_input("Unit Price (₹/kWh)", value=6.5)

if st.button("🔍 Predict"):
    try:
        if predict_type == "1-hour Power Usage":
            res = requests.post("http://localhost:5000/predict", json={
                "appliance": appliance,
                "features": features
            })
            if res.status_code == 200:
                value = res.json()["prediction"]
                st.success(f"Predicted Power Usage: {value:.4f} kWh")
                st.info(f"Estimated Cost: ₹{value * unit_price:.2f}")
            else:
                st.error("Prediction failed.")

        else:  # Monthly prediction
            res = requests.post("http://localhost:5000/predict-month", json={
                "appliance": appliance,
                "features": features
            })
            if res.status_code == 200:
                value = res.json()["predicted_monthly_kwh"]
                st.success(f"Predicted Monthly Usage: {value:.2f} kWh")
                st.info(f"Estimated Monthly Bill: ₹{value * unit_price:.2f}")
            else:
                st.error("Prediction failed.")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
