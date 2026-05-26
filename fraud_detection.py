import streamlit as st
import pandas as pd
import joblib


st.set_page_config(
    page_title="Fraud Detection App",   # Tab name
    page_icon="💳",                     # Emoji or icon
    layout="centered" )

# Load model once
model = joblib.load("fraud_detection_pipeline.pkl")
# App title and intro
st.title("Fraud Detection Prediction App")
st.markdown("Please enter the transaction details and click Predict")

st.divider()

# Use a form to prevent rerun duplication
with st.form(key="fraud_form"):
    transaction_type = st.selectbox(
        "Transaction Type",
        ["PAYMENT", "TRANSFER", "CASH_OUT", "DEPOSITE"],
        key="transaction_type_select"
    )

    amount = st.number_input("Amount", min_value=0.0, value=10000.0, key="amount_input")

    st.header("Sender Details")
    oldbalanceOrg = st.number_input("Old Balance (sender)", min_value=0.0, value=10000.0, key="oldbalanceOrg_input")
    newbalanceOrg = st.number_input("New Balance (sender)", min_value=0.0, value=9000.0, key="newbalanceOrg_input")

    st.header("Receiver Details")
    oldbalanceDest = st.number_input("Old Balance (receiver)", min_value=0.0, value=0.0, key="oldbalanceDest_input")
    newbalanceDest = st.number_input("New Balance (receiver)", min_value=0.0, value=0.0, key="newbalanceDest_input")

    # Submit button inside form
    submit_button = st.form_submit_button(label="Predict", key="predict_button")

# Prediction logic runs only when form is submitted
if submit_button:
    balanceDiffOrig = oldbalanceOrg - newbalanceOrg
    balanceDiffdest = newbalanceDest - oldbalanceDest

    input_data = pd.DataFrame([{
        "type": transaction_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrg,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
        "balanceDiffOrig": balanceDiffOrig,
        "balanceDiffdest": balanceDiffdest
    }])

    try:
        prediction = model.predict(input_data)[0]
        st.subheader(f"Prediction: {int(prediction)}")
        if prediction == 1:
            st.error("⚠️ This transaction can be fraud")
        else:
            st.success("✅ This transaction looks  it is not a fraud")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.write("Input data:", input_data)
