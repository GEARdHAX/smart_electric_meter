from flask import Flask, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)

# Load models
fan_model = joblib.load("./fan_model.pkl")
tv_model = joblib.load("./tv_model.pkl")
fridge_model = joblib.load("./fridge_model.pkl")

# Load scaler only for fridge if needed
try:
    fridge_scaler = joblib.load("./scaler.pkl")
    fridge_has_scaler = True
except:
    fridge_scaler = None
    fridge_has_scaler = False


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    appliance = data["appliance"]
    base_input = data["features"]  # [current, voltage, on_off]

    # Extend base input to full feature set
    if appliance == "fan":
        # Expected 8 features: hour, day, month, temp, status, rpm, voltage, current
        features = [12, 15, 4, 30.0, base_input[2],
                    1200, base_input[1], base_input[0]]
    elif appliance == "led_tv":
        # Expected 6 features: Hour, Day, Month, Current, Voltage, On/Off
        features = [12, 15, 4, base_input[0], base_input[1], base_input[2]]
    elif appliance == "fridge":
        # Expected 8 features: Hour, Day, Month, Current, Voltage, On/Off, Hour, DayOfWeek
        features = [12, 15, 4, base_input[0],
                    base_input[1], base_input[2], 12, 4]
    else:
        return jsonify({"error": "Invalid appliance"})

    features = np.array(features).reshape(1, -1)

    # Predict
    if appliance == "fan":
        pred = fan_model.predict(features)
    elif appliance == "led_tv":
        pred = tv_model.predict(features)
    elif appliance == "fridge":
        if fridge_has_scaler:
            features = fridge_scaler.transform(features)
        pred = fridge_model.predict(features)

    return jsonify({"prediction": float(pred[0])})


@app.route("/predict-month", methods=["POST"])
def predict_month():
    data = request.get_json()
    appliance = data["appliance"]
    base_input = data["features"]  # [current, voltage, on_off]

    future_inputs = []
    for i in range(720):  # simulate 720 hourly rows
        if appliance == "fan":
            row = [12, 15, 4, 30.0, base_input[2], 1200,
                   base_input[1], base_input[0]]  # 8 features
        elif appliance == "led_tv":
            row = [12, 15, 4, base_input[0],
                   base_input[1], base_input[2]]  # 6 features
        elif appliance == "fridge":
            row = [12, 15, 4, base_input[0], base_input[1],
                   base_input[2], 12, 4]  # 8 features
        else:
            return jsonify({"error": "Invalid appliance"})
        future_inputs.append(row)

    future_inputs = np.array(future_inputs)

    if appliance == "fan":
        preds = fan_model.predict(future_inputs)
    elif appliance == "led_tv":
        preds = tv_model.predict(future_inputs)
    elif appliance == "fridge":
        if fridge_has_scaler:
            future_inputs = fridge_scaler.transform(future_inputs)
        preds = fridge_model.predict(future_inputs)

    total_kwh = float(np.sum(preds))
    return jsonify({"predicted_monthly_kwh": total_kwh})


if __name__ == "__main__":
    app.run(debug=True)
