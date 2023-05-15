#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import numpy as np
import pandas as pd
import pickle

model = pickle.load(open("pipe3.pkl", "rb"))
df = pd.read_csv("traineddata.csv")
    
weather_values = ['Clear, Few clouds, Partly cloudy, Partly cloudy',
                      "Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist",
                      "Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds",
                      "Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog"]
weekday_values = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
boolean_values = ["No", "Yes"]
year_values = ["2018", "2019"]
month_values = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
st.title("Bike Sharing Analysis & Prediction")
st.subheader("Enter the following information to predict the number of bike rentals:") 
col1, col2 = st.columns(2)

with col1:
        year = st.selectbox('Year', options=[0, 1], format_func=lambda x: year_values[x])
        month = st.selectbox('Month', options=range(1, 13), format_func=lambda x: month_values[x-1])
        holiday = st.selectbox('Holiday', options=[0, 1], format_func=lambda x: boolean_values[x])
        st.markdown('Weather-wise:') 
with col2:
        weekday = st.selectbox('Weekday', options=[0, 1, 2, 3, 4, 5, 6], format_func=lambda x: weekday_values[x])
        st.header('  ') 
           
        
with col1:
        weather = st.selectbox('Weather', options=[1, 2, 3, 4], format_func=lambda x: weather_values[x-1])
        conv_factor2 = 100.0
        humidity = st.slider('Humidity (%)', min_value=0, max_value=int(conv_factor2), step=1, value=int(0.5*conv_factor2), format='%d %%')
        humidity_normalized = humidity / conv_factor2

with col2:
        conv_factor = 41.0
        temp = st.slider('Temperature (°C)', min_value=0, max_value=int(conv_factor), step=1, value=int(0.5*conv_factor), format='%d °C')
        temp_normalized = temp / conv_factor
        conv_factor1 = 67.0
        windspeed = st.slider('Wind Speed (km/h)', min_value=0, max_value=int(conv_factor1), step=1, value=int(0.5*conv_factor1), format='%d km/h')
        windspeed_normalized = windspeed / conv_factor1

        
        
                
input_data = {
        'season': get_season(spring),get_season(fall)
        'yr': year,
        'mnth': month,
        'holiday': holiday,
        'weekday': weekday,
        'workingday': 1 - holiday,
        'weathersit': weather,
        'atemp': temp_normalized,
        'hum': humidity_normalized,
        'windspeed': windspeed_normalized,
        'day' : day,
        'comfortable_temp' : comf_temp(temp_normalized),
        'comfortable_humidity' : comf_hum(humidity_normalized)
}

input_df = pd.DataFrame([input_data])

prediction = model.predict(input_df)
    
rounded_prediction = round(prediction[0])
    
st.subheader('Predicted Number of Bike Rentals:')
st.markdown(f"<p style='font-size:30px; color:green'>{rounded_prediction}</p>", unsafe_allow_html=True)
bike_emoji = '<span style="font-size:30px"> 🚲 </span>'
st.write(bike_emoji * rounded_prediction, unsafe_allow_html=True)
    
    


# In[ ]:




