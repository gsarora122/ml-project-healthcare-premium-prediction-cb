import pandas as pd
from joblib import load

# Load models and scalers
model_young = load(r"app/artifacts/model_young.joblib")
scaler_young = load(r"app/artifacts/scaler_young.joblib")

model_old = load(r"app/artifacts/model_old.joblib")
scaler_old = load(r"app/artifacts/scaler_old.joblib")

def calculate_normalized_risk(medical_history):
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }
    diseases = medical_history.lower().replace(" & ", "&").split("&")
    total_risk_score = sum(risk_scores.get(d.strip(), 0) for d in diseases)
    min_score = 0
    max_score = 14
    normalized_risk_score = (total_risk_score - min_score) / (max_score - min_score)
    return normalized_risk_score

def preprocessing_data(age, number_of_dependants, income_lakhs, genetical_risk, insurance_plan,
                       employment_status, gender, marital_status, bmi_category, smoking_status, region,
                       medical_history, model):

    # Manual encoding for insurance plan
    insurance_plan_encoded = {"Bronze": 1, "Silver": 2, "Gold": 3}

    input_dict = {
        "age": age,
        "number_of_dependants": number_of_dependants,
        "income_lakhs": income_lakhs,
        "genetical_risk": genetical_risk,
        "insurance_plan": insurance_plan_encoded.get(insurance_plan, 0),
        "employment_status_Salaried": 1 if employment_status == "Salaried" else 0,
        "employment_status_Self-Employed": 1 if employment_status == "Self-Employed" else 0,
        "employment_status_Freelancer": 1 if employment_status == "Freelancer" else 0,
        "gender_Male": 1 if gender == "Male" else 0,
        "marital_status_Unmarried": 1 if marital_status == "Unmarried" else 0,
        "bmi_category_Obesity": 1 if bmi_category == "Obesity" else 0,
        "bmi_category_Overweight": 1 if bmi_category == "Overweight" else 0,
        "bmi_category_Underweight": 1 if bmi_category == "Underweight" else 0,
        "smoking_status_Occasional": 1 if smoking_status == "Occasional" else 0,
        "smoking_status_Regular": 1 if smoking_status == "Regular" else 0,
        "region_Northwest": 1 if region == "Northwest" else 0,
        "region_Southeast": 1 if region == "Southeast" else 0,
        "region_Southwest": 1 if region == "Southwest" else 0,

        "income_level": 1  # Dummy used for scaling (gets dropped later)
    }

    # Convert to DataFrame
    df = pd.DataFrame([input_dict])

    # Add normalized risk
    df["normalized_risk_score"] = calculate_normalized_risk(medical_history)

    # Apply appropriate scaling
    df = handling_scaling(df, age)

    # Match training column structure
    expected_features = model.feature_names_in_
    df = df.reindex(columns=expected_features, fill_value=0)

    return df

def handling_scaling(df, age):
    scaler_object = scaler_young if age <= 25 else scaler_old
    scaler = scaler_object["scaler"]
    cols_to_scale = scaler_object["cols_to_scale"]
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])
    df.drop(columns=["income_level"], inplace=True, errors="ignore")
    return df

def predict(age, number_of_dependants, income_lakhs, genetical_risk, insurance_plan,
            employment_status, gender, marital_status, bmi_category, smoking_status, region,
            medical_history):

    # Select model based on age
    model = model_young if age <= 25 else model_old

    # Preprocess input data
    input_df = preprocessing_data(age, number_of_dependants, income_lakhs, genetical_risk,
                                  insurance_plan, employment_status, gender, marital_status,
                                  bmi_category, smoking_status, region, medical_history, model)

    prediction = model.predict(input_df)
    return int(prediction[0])
