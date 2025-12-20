import streamlit as st
import pandas as pd
import pickle

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Food Delivery Time Prediction", layout="wide")

st.title("🍔 Food Delivery Time Prediction App")
st.write("Predict delivery time using a trained ML model.")

# -------------------------------
# Load Model + Saved Columns
# -------------------------------
model = pickle.load(open("random_forest.pkl", "rb"))
saved_columns = pickle.load(open("columns.pkl", "rb"))

# -------------------------------
# User Inputs (Sidebar)
# -------------------------------
with st.sidebar:
    st.header("Delivery Parameters")
    Time_of_Day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening", "Night"])
    Traffic_Level = st.selectbox("Traffic Level", ["Low", "Medium", "High"])
    Vehicle_Type = st.selectbox("Vehicle Type", ["Bike", "Scooter", "Car"])
    Weather = st.selectbox("Weather", ["Clear", "Rainy", "Windy", "Cloudy", "Foggy"])
    Distance_KM = st.number_input("Distance (KM)", min_value=0.1, step=0.1)
    Preparation_Time_min = st.number_input("Preparation Time (min)", min_value=1, max_value=120)
    Courier_Experience_yrs = st.number_input("Courier Experience (yrs)", min_value=0, max_value=40)

# -------------------------------
# Create Input DataFrame
# -------------------------------
input_df = pd.DataFrame([{
    "Distance_km": Distance_KM,
    "Preparation_Time_min": Preparation_Time_min,
    "Courier_Experience_yrs": Courier_Experience_yrs,
    "Weather": Weather,
    "Time_of_Day": Time_of_Day,
    "Traffic_Level": Traffic_Level,
    "Vehicle_Type": Vehicle_Type,
}])

# -------------------------------
# Encoding Input (NO drop_first!)
# -------------------------------
input_encoded = pd.get_dummies(
    input_df[['Weather', 'Traffic_Level', 'Time_of_Day', 'Vehicle_Type']],
    drop_first=False,   # <-- FIXED
    dtype=int
)

# Keep numeric features
input_df = input_df[['Distance_km', 'Preparation_Time_min', 'Courier_Experience_yrs']]

# Final dataframe
final_df = pd.concat([input_df, input_encoded], axis=1)

# Align columns with model training
final_df = final_df.reindex(columns=saved_columns, fill_value=0)

# -------------------------------
# Prediction
# -------------------------------
if st.button("Predict Delivery Time"):
    try:
        prediction = model.predict(final_df)[0]

        if prediction < 20:
            status = "🚀 Fast delivery expected!"
        elif prediction < 40:
            status = "⏳ Moderate wait time."
        else:
            status = "😅 Long wait ahead."

        st.success(f"⏱ Estimated Delivery Time: **{prediction:.2f} minutes** 🛵💨\n{status}")

    except Exception as e:
        st.error(f"Prediction failed: {e}")
