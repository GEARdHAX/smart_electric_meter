# 🔌 Smart Energy Consumption Predictor

A machine learning-powered web app that predicts the electricity usage (in kWh) of household appliances like a fan, fridge, or LED TV — either for the next hour or for the next month (720 hours).

Built using Python, Flask (for backend API), Streamlit (for frontend UI), and trained RandomForestRegressor models.

---

## 📦 Features

- 🌀 Predict power usage of: Fan, Fridge, LED TV
- ⏱️ Predict for: 1 hour or 30 days (720 hours)
- 🧠 Backend powered by pre-trained ML models
- 🎯 Requires only 3 inputs:
  - Current (A)
  - Voltage (V)
  - On/Off status
- 💸 Estimates electricity bill based on your cost per unit (₹/kWh)

---

## 🛠 Tech Stack

- 🐍 Python 3
- ⚡ Flask – for serving predictions via API
- 🎨 Streamlit – for interactive web interface
- 🧠 scikit-learn – trained RandomForest models
- 📊 pandas, numpy – for data handling
- 🗃️ joblib – to save and load models

---

## 📁 Folder Structure

smart-electric_meter/
├── app.py 
├── model_api.py 
├── fan_model.pkl 
├── fridge_model.pkl 
├── tv_model.pkl 
├── datasets/ 
│ └── fan_3month.csv
│ └── fridge_data.csv
│ └── LED_TV_Dataset_Extended.csv
├── README.md 
└── requirements.txt 

---

## 🚀 How to Run the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/GEARdHAX/smart_electric_meter.git
cd smart-electric_meter
```
