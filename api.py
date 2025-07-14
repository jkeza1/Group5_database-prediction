from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib
import json

# --- Load Model and Artifacts ---
model = joblib.load("addiction_model_regression.pkl")
scaler = joblib.load("scaler.pkl")
with open("feature_names.json", "r") as f:
    feature_names = json.load(f)

# --- Initialize FastAPI App ---
app = FastAPI(title="Teen Phone Addiction Predictor")

# --- Pydantic Input Schema ---
class AddictionInput(BaseModel):
    Age: int
    Gender: str
    School_Grade: str
    Daily_Usage_Hours: float
    Sleep_Hours: float
    Academic_Performance: float
    Social_Interactions: float
    Exercise_Hours: float
    Anxiety_Level: float
    Depression_Level: float
    Self_Esteem: float
    Parental_Control: bool
    Screen_Time_Before_Bed: float
    Phone_Checks_Per_Day: int
    Apps_Used_Daily: int
    Time_on_Social_Media: float
    Time_on_Gaming: float
    Time_on_Education: float
    Family_Communication: str
    Weekend_Usage_Hours: float
    Phone_Usage_Purpose: str

# --- Prediction Endpoint ---
@app.post("/predict")
def predict_addiction_level(data: AddictionInput):
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([data.dict()])

        # --- Preprocessing ---
        # Ordinal encoding
        grade_order = ['7th', '8th', '9th', '10th', '11th', '12th']
        input_df['School_Grade'] = pd.Categorical(input_df['School_Grade'], categories=grade_order, ordered=True).codes

        # Label encoding
        gender_map = {'Male': 1, 'Female': 0, 'Other': 2}
        fam_comm_map = {'Good': 1, 'Average': 0, 'Poor': 2}
        input_df['Gender'] = input_df['Gender'].map(gender_map)
        input_df['Family_Communication'] = input_df['Family_Communication'].map(fam_comm_map)

        # Boolean to int
        input_df['Parental_Control'] = input_df['Parental_Control'].astype(int)

        # One-hot encode Phone_Usage_Purpose
        input_df = pd.get_dummies(input_df, columns=["Phone_Usage_Purpose"], prefix="Phone_Usage_Purpose")

        # Feature engineering
        input_df['Is_Heavy_User'] = (input_df['Daily_Usage_Hours'] > 5).astype(int)

        # Align with training feature columns
        for col in feature_names:
            if col not in input_df.columns:
                input_df[col] = 0  # Add missing one-hot columns
        input_df = input_df[feature_names]  # Ensure correct order

        # Scale numeric columns (used during training)
        numeric_cols = [
            'Age', 'Daily_Usage_Hours', 'Sleep_Hours', 'Academic_Performance',
            'Social_Interactions', 'Exercise_Hours', 'Anxiety_Level',
            'Depression_Level', 'Self_Esteem', 'Screen_Time_Before_Bed',
            'Phone_Checks_Per_Day', 'Apps_Used_Daily', 'Time_on_Social_Media',
            'Time_on_Gaming', 'Time_on_Education', 'Weekend_Usage_Hours'
        ]
        input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])

        # --- Make Prediction ---
        prediction = model.predict(input_df)[0]
        return {"predicted_addiction_level": round(prediction, 2)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {str(e)}")
