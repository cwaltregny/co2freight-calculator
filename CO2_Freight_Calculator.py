from openai import OpenAI
import streamlit as st
import pandas as pd
import numpy as np
import time
from io import StringIO
from utils.logo import add_logo

def inject_css():
    css = """
    <style>
        /* General body styling */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #F0F2F5;
        }
        
        /* Custom banner style */
        .custom-banner {
            background-color: white; 
            padding: 10px 0;
            color: black;
            text-align: left;
            margin-bottom: 10px;
            font-size: 40px;
        }

        .custom-banner img {
            height: 50px; /* Adjust based on your logo's size */
            margin: 0 20px;
            vertical-align: middle;
        }

        .stButton>button {
            border: 2px solid #4CAF50;
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            cursor: pointer;
            border-radius: 4px;
        }

        .stButton>button:hover {
            background-color: #45a049;
        }

        .stFileUploader {
            border: 2px dashed #4CAF50;
            border-radius: 5px;
            background-color: #ffffff;
        }

        h1 {
            color: #333;
        }

        /* Add more custom styles as needed */
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


st.set_page_config(page_title="CO2 Freight Calculator", page_icon="https://co2freight-calculator.com/wp-content/uploads/2024/02/EcoFreightCalculator_logo-Charlotte-Waltregny.png")
# CSS Styling
inject_css()

# Welcome Banner and App Description
st.markdown("""
<div class="custom-banner">
    <h1>Welcome to CO2 Freight Calculator</h1>
</div>

## 🌱 What is this app about?

This app is designed to help businesses and individuals calculate the carbon footprint of their freight activities. By uploading data related to your shipping activities, you can get an estimate of the CO2 emissions associated with your freight operations.

## 📊 How to use the app?

1. **Prepare your data:** Ensure you have a CSV file with details of your freight activities. Your file should include columns for origin, destination, mode of transport, and weight.

2. **Upload your file:** Use the file uploader to submit your CSV. The app will then calculate the emissions based on standardized emission factors.

3. **Review the results:** Once the calculation is complete, you can review the emissions associated with each shipment. The app also provides options to download the results for further analysis.

""", unsafe_allow_html=True)

#st.image("freightmap.png")
    
    # Example of generating a map (assuming you have lat/long data)
    # df = pd.DataFrame({
    #     'lat': [34.0522, 40.7128],
    #     'lon': [-118.2437, -74.0060]
    # })
    # st.map(df)
