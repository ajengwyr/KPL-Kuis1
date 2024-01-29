import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pickle
import numpy as np

# Load model
model = pickle.load(open('model.sav', 'rb'))

# Function to predict stroke
def predict_stroke(features):
    features = np.array(features).reshape(1, -1)
    prediction = model.predict(features)
    probability = model.predict_proba(features)[0][1]
    return prediction, probability

# Load credentials from config.yml
with open('config.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Define main function
def main():
    # Authenticate user
    authenticator.login('Login', 'main')

    # Check authentication status
    if st.session_state["authentication_status"]:
        authenticator.logout('Logout', 'main', key='unique_key')
        st.write(f'Welcome *{st.session_state["name"]}*')
        

        # Display main content
        st.title('''
        :rainbow[Aplikasi Prediksi Penyakit Stroke]''')
        st.write(''':blue[Masukkan informasi yang dibutuhkan berikut ini:]''')

        age = st.slider('Age', 0, 130, 25)
        hypertension = st.selectbox("Hypertension", ("Yes", "No"))
        heart_disease = st.selectbox("Heart Disease", ("Yes", "No"))
        avg_glucose_level = st.number_input("Average Glucose Level", min_value=0.0, value=80.0)
        bmi = st.number_input("BMI", min_value=0.0, value=20.0)
        gender = st.selectbox("Gender", ("Male", "Female"))
        smoking_status = st.selectbox("Smoking Status", ("Unknown", "Formerly Smoked", "Never Smoked", "Smokes"))
        ever_married = st.selectbox("ever_married", ("Yes", "No"))
        work_type = st.selectbox("work_type Status", ("Private", "Self-employed", "children", "Govt_job","Never_worked"))
        Residence_type = st.selectbox("Residence_type", ("Urban", "Rural"))

        hypertension = 1 if hypertension == "Yes" else 0
        heart_disease = 1 if heart_disease == "Yes" else 0
        gender = 1 if gender == "Male" else 0
        ever_married = 1 if ever_married == "Yes" else 0
        Residence_type = 1 if gender == "Urban" else 0

        smoking_map = {
            "Unknown": 0,
            "Formerly Smoked": 1,
            "Never Smoked": 2,
            "Smokes": 3
        }
        smoking_status = smoking_map[smoking_status]

        work_type_map = {
            "Govt_job": 0,
            "Never_worked": 1,
            "Private": 2,
            "Self-employed": 3,
            "children": 4,
        }
        work_type = work_type_map[work_type]

        if st.button("Prediksi Stroke"):
            # Gather input features
            features = [age, hypertension, heart_disease, avg_glucose_level, bmi, gender, smoking_status, ever_married, work_type, Residence_type]

            # Predict stroke and probability
            prediction, probability = predict_stroke(features)

            # Display the prediction
            if prediction[0] == 0:
                st.write("Selamat! Kamu memiliki kemungkinan kecil penyakit stroke \
            :tulip:")
                st.write("Kemungkinan stroke:", probability)
            else:
                st.write("Hati-Hati!! Kamu memiliki risiko tinggi penyakit stroke.")
                st.write("Kemungkinan stroke:", probability)

# Run the main function
if __name__ == "__main__":
    main()
