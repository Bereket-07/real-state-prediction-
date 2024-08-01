import streamlit as st
import requests
import json 
import pickle
import numpy as np

def load_saved_artifacts():
    print("loading saved artifacts ...... start")
    global __data_columns
    global __locations
    global __models

    with open('./artifacts/columns.json','r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]
    with open('./artifacts/banglore_home_prices_model.pickle','rb') as f:
        __models  = pickle.load(f)
    
    print("loading saved articles ....... done")




# Function to fetch locations
def fetch_locations():
    load_saved_artifacts()
    return __locations

# Function to predict price
def predict_price(data):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    x[0]=data['sqft']
    x[1]=data['bath']
    x[2]=data['bhk']
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__models.predict([x])[0],2)

st.title('Price Prediction Form')

# Add custom CSS to change border colors based on input validity
st.markdown("""
    <style>
        .stNumberInput input[type=number]:valid {
            border: 2px solid green;
        }
        .stNumberInput input[type=number]:invalid {
            border: 2px solid red;
        }
    </style>
""", unsafe_allow_html=True)

# Fetch locations
locations = fetch_locations()

if locations:
    with st.form(key='predict_form'):
        # First input: Accepting a number, default 1000
        number1 = st.number_input('Enter a square feet', min_value=0, value=1000, step=1, key="sqft")

        # Second input: Incrementing number
        number2 = st.number_input('Enter the number of bed rooms', min_value=0, value=0, step=1, key="bedrooms")

        # Third input: Incrementing number
        number3 = st.number_input('Enter the number of bath rooms', min_value=0, value=0, step=1, key="bathrooms")

        # Fourth input: String with dropdown menu
        location = st.selectbox('Select a location', locations)

        # Submit button
        submit_button = st.form_submit_button(label='Predict Price')

    if submit_button:
        # Prepare data for prediction
        data = {
            'sqft': number1,
            'bhk': number2,
            'bath': number3,
            'location': location
        }
        
        # Get prediction result
        result = predict_price(data)
        
        if result:
            st.markdown("<h2 style='text-align: center; color: green;'>Prediction Result</h2>", unsafe_allow_html=True)
            st.metric(label="Predicted Price", value=f"${result:,.2f}")
