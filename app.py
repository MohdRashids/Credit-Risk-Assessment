import streamlit as st
import pandas as pd
import joblib

# ===========================
# LOAD MODEL
# ===========================

model = joblib.load("models/credit_risk_model.pkl")

# ===========================
# PAGE CONFIG
# ===========================

st.set_page_config(
    page_title="Credit Risk Assessment",
    page_icon="💳",
    layout="wide"
)

# ===========================
# SIDEBAR
# ===========================

st.sidebar.title("📊 Credit Risk Assessment")

st.sidebar.success("Random Forest Classifier")

st.sidebar.write("Accuracy : 77%")
st.sidebar.write("ROC-AUC : 0.80")
st.sidebar.write("Dataset : German Credit")

# ===========================
# TITLE
# ===========================

st.title("💳 Credit Risk Assessment")

st.write("Enter customer information to predict credit risk.")

# ===========================
# INPUTS
# ===========================

col1, col2 = st.columns(2)

with col1:

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=80,
        value=35
    )

    sex = st.selectbox(
        "Sex",
        ["Female", "Male"]
    )

    job = st.selectbox(
        "Job",
        [0,1,2,3]
    )

    housing = st.selectbox(
        "Housing",
        ["Free","Own","Rent"]
    )

    saving = st.selectbox(
        "Saving Account",
        [
            "Unknown",
            "Little",
            "Moderate",
            "Rich",
            "Quite Rich"
        ]
    )

with col2:

    checking = st.selectbox(
        "Checking Account",
        [
            "Unknown",
            "Little",
            "Moderate",
            "Rich"
        ]
    )

    credit = st.number_input(
        "Credit Amount",
        min_value=250,
        max_value=20000,
        value=4000
    )

    duration = st.number_input(
        "Duration (Months)",
        min_value=4,
        max_value=72,
        value=24
    )

    purpose = st.selectbox(
        "Purpose",
        [
            "car",
            "radio/TV",
            "education",
            "furniture/equipment",
            "business",
            "domestic appliances",
            "repairs",
            "vacation/others"
        ]
    )

# ===========================
# ENCODING
# ===========================

sex_map = {
    "Female":0,
    "Male":1
}

housing_map = {
    "Free":0,
    "Own":1,
    "Rent":2
}

saving_map = {
    "Unknown":0,
    "Little":1,
    "Moderate":2,
    "Rich":3,
    "Quite Rich":4
}

checking_map = {
    "Unknown":0,
    "Little":1,
    "Moderate":2,
    "Rich":3
}

purpose_map = {
    "car":1,
    "radio/TV":5,
    "education":3,
    "furniture/equipment":4,
    "business":0,
    "domestic appliances":2,
    "repairs":6,
    "vacation/others":7
}

# ===========================
# BUTTON
# ===========================

if st.button("Predict Risk"):

    customer = pd.DataFrame({

        "Age":[age],
        "Sex":[sex_map[sex]],
        "Job":[job],
        "Housing":[housing_map[housing]],
        "Saving accounts":[saving_map[saving]],
        "Checking account":[checking_map[checking]],
        "Credit amount":[credit],
        "Duration":[duration],
        "Purpose":[purpose_map[purpose]]

    })

    prediction = model.predict(customer)

    probability = model.predict_proba(customer)

    st.markdown("---")

    if prediction[0] == 0:

        st.success("✅ GOOD CREDIT RISK")

    else:

        st.error("❌ BAD CREDIT RISK")

    st.subheader("Prediction Confidence")

    if prediction[0] == 0:
        st.progress(float(probability[0][0]))
    else:
        st.progress(float(probability[0][1]))

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Good Risk",
            f"{probability[0][0]*100:.2f}%"
        )

    with col2:

        st.metric(
            "Bad Risk",
            f"{probability[0][1]*100:.2f}%"
        )

# ===========================
# FOOTER
# ===========================

st.markdown("---")

st.caption(
    "Developed by MOHD RASHID | Credit Risk Assessment using Machine Learning"
)