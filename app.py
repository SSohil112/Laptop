import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the model and dataset
pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))

st.title("💻 Laptop Price Predictor")

# Brand
company = st.selectbox('Brand', df['Company'].unique())

# Type
type = st.selectbox('Type', df['TypeName'].unique())

# RAM
ram = st.selectbox('RAM (in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])

# Weight
weight = st.number_input('Weight of the Laptop')

# Touchscreen
touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])

# IPS
ips = st.selectbox('IPS Panel', ['No', 'Yes'])

# Screen size
screen_size = st.slider('Screen Size (in inches)', 10.0, 18.0, 13.0)

# Resolution
resolution = st.selectbox('Screen Resolution', [
    '1920x1080', '1366x768', '1600x900', '3840x2160',
    '3200x1800', '2880x1800', '2560x1600', '2560x1440', '2304x1440'
])

# CPU
cpu = st.selectbox('CPU', df['brand_name'].unique())

# HDD
hdd = st.selectbox('HDD (in GB)', [0, 128, 256, 512, 1024, 2048])

# SSD
ssd = st.selectbox('SSD (in GB)', [0, 8, 128, 256, 512, 1024])

# GPU
gpu = st.selectbox('GPU', df['Gpu_barnd'].unique())

# OS
os = st.selectbox('Operating System', df['os'].unique())

# Predict Button
if st.button('Predict Price 💰'):
    # Convert categorical Yes/No to binary
    touchscreen = 1 if touchscreen == 'Yes' else 0
    ips = 1 if ips == 'Yes' else 0

    # Calculate PPI
    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])
    ppi = ((X_res ** 2) + (Y_res ** 2)) ** 0.5 / screen_size

    # Create input DataFrame
    query = pd.DataFrame([{
        'Company': company,
        'TypeName': type,
        'Ram': ram,
        'Weight': weight,
        'Touchscreen': touchscreen,
        'IPS': ips,             # FIXED: was 'Ips'
        'ppi': ppi,             # FIXED: was 'PPI'
        'brand_name': cpu,
        'HDD': hdd,
        'SSD': ssd,
        'Gpu_barnd': gpu,
        'os': os
    }])


    # Predict price
    predicted_log_price = pipe.predict(query)[0]
    predicted_price = int(np.exp(predicted_log_price))

    st.success(f"💰 The predicted price of this configuration is: ₹ {predicted_price}")

