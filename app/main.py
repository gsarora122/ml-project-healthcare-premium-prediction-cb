import streamlit as st
from prediction_helper import predict

st.title("Shield Insurance Prediction")

data_dict = {
    "gender": ['Male', 'Female'],
    "region": ['Northwest', 'Northeast', 'Southeast', 'Southwest'],
    "marital_status": ['Unmarried', 'Married'],
    "bmi_category": ['Normal', 'Overweight', 'Underweight', 'Obesity'],
    "smoking_status": ['No Smoking', 'Regular', 'Occasional'],
    "employment_status": ['Salaried', 'Self-Employed', 'Freelancer'],
    "medical_history": ['No Disease', 'High blood pressure', 'Diabetes & High blood pressure',
                        'Diabetes & Heart disease', 'Diabetes', 'Diabetes & Thyroid',
                        'Heart disease', 'Thyroid', 'High blood pressure & Heart disease'],
    
    "insurance_plan": ['Bronze', 'Silver', 'Gold']
}

row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

with row1[0]:
    age = st.number_input(label="Age", min_value=18, value=18, max_value=100, step=1)
with row1[1]:
    number_of_dependants = st.number_input(label="Number of Dependants", min_value=0, max_value=20, step=1)
with row1[2]:
    income_lakhs = st.number_input(label="Income in Lakhs", min_value=0, max_value=10000000, step=1)

with row2[0]:
    genetical_risk = st.number_input(label="Genetical Risk", min_value=0, max_value=5, step=1)
with row2[1]:
    insurance_plan = st.selectbox(label="Insurance Plan", options=data_dict["insurance_plan"])
with row2[2]:
    employment_status = st.selectbox(label="Employment Status", options=data_dict["employment_status"])

with row3[0]:
    gender = st.selectbox(label="Gender", options=data_dict["gender"])
with row3[1]:
    marital_status = st.selectbox(label="Marital Status", options=data_dict["marital_status"])
with row3[2]:
    bmi_category = st.selectbox(label="BMI Category", options=data_dict["bmi_category"])

with row4[0]:
    smoking_status = st.selectbox(label="Smoking Status", options=data_dict["smoking_status"])
with row4[1]:
    region = st.selectbox(label="Region", options=data_dict["region"])
with row4[2]:
    medical_history = st.selectbox(label="Medical History", options=data_dict["medical_history"])

if st.button(label="Get Analytics"):
    prediction = predict(age, number_of_dependants, income_lakhs, genetical_risk, insurance_plan,
                         employment_status, gender, marital_status, bmi_category, smoking_status, region,
                         medical_history)
    
    st.write(f"Health Insurance Cost: {prediction}")

