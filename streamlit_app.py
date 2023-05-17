import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pickle
from PIL import Image
import time

# create page navigation
def page_navigation():
    pages = {
        "Introduction": page_summary,
        "Exploratory Data Analysis": page_eda,
        "Prediction Result": page_model,
    }
    st.sidebar.title("Bike Sharing Analysis & Prediction")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page()                  

# the first page is summary
def page_summary():
    st.title("Bike Sharing Analysis & Prediction")
    st.image('https://wips.plug.it/cips/tecnologia/cms/2021/03/bike-sharing.jpg')
    
#the second page is our plots
def page_eda():
    st.title("Bike Sharing Analysis & Prediction")
    st.header("Exploratory Data Analysis")
    st.subheader("Information of the dataset")
    col1, col2, col3 = st.columns(3)
    col1.metric("Columns", "16")
    col2.metric("Rows", "730")
    col3.metric("Null Values", "0")
    st.subheader("First 5 rows of the dataset:")
    df = pd.read_csv('day.csv')
    st.dataframe(df.head(), use_container_width=True)
    st.subheader("Analysis of the Bike Sharing Service")
    st.markdown("Overview:")
    tab1 = st.tabs(["📕 Distribution by User"])
    # 1. Distribution of Rental Counts by type of user
    df = pd.read_csv('day.csv')
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(y=["Registered", "Casual"], x=[df["registered"].sum(), df["casual"].sum()], orientation='h'))
    fig1.update_traces(opacity=0.75)
    fig1.update_layout(title="Distribution of rental counts by type of user", yaxis_title="User type", xaxis_title="Count")
    tab1[0].plotly_chart(fig1, use_container_width=True)
    
    st.markdown("By Season:")
    df = pd.read_csv('day.csv')
    tab2, tab3, tab4, tab5, tab6 = st.tabs(["📗 by Season", "📘 by Month", "📙 by Day", "📓 by Weekday/Weekend", "🎉 by Holiday"])
    # 2. Rental Counts by Season
    grouped_season = df.groupby("season").sum()["cnt"]
    fig2 = px.bar(grouped_season, title="Rental Counts by Season")
    fig2.update_layout(xaxis_title="Season", yaxis_title="Rental counts",
                      xaxis=dict(tickmode='array', tickvals=[1, 2, 3, 4],
                                 ticktext=['Winter', 'Spring', 'Summer', 'Fall']))
    # 3. Rental Counts by Month of the year
    grouped_month = df.groupby("mnth").sum()["cnt"]
    fig3 = px.bar(grouped_month, title="Rental Counts by Month")
    fig3.update_layout(xaxis_title="Month", yaxis_title="Rental counts",
                      xaxis=dict(tickmode='array', tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                 ticktext=['January', 'February', 'March', 'April', 'May', 'June', 
                                           'July', 'August', 'September', 'October', 'November', 'December']))

    # 4. Rental Counts by Day of the week
    fig4 = px.bar(df, x="weekday", y=["casual", "registered"], title="Rental Counts by Day of the week", barmode="stack")
    fig4.update_layout(xaxis_title="Day of the week", yaxis_title="Rental counts",
                  xaxis=dict(tickmode='array', tickvals=[0, 1, 2, 3, 4, 5, 6], 
                             ticktext=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']))

    # 5. Rental Counts by weekday or weekend
    grouped_weekday = df.groupby("workingday").sum()["cnt"]

    fig5 = px.bar(grouped_weekday, title="Rental Counts if the Day is a weekday or weekend")
    fig5.update_layout(xaxis_title="Weekday or Weekend?", yaxis_title="Rental counts",
                      xaxis=dict(tickmode='array', tickvals=[0, 1],
                                 ticktext=['Weekend', 'Weekday']))
    # Rental Counts by holiday
    grouped_holiday = df.groupby("holiday").sum()["cnt"]

    fig6 = px.bar(grouped_holiday, title="Rental Counts if the Day is a holiday")
    fig6.update_layout(xaxis_title="Holiday?", yaxis_title="Rental counts",
                      xaxis=dict(tickmode='array', tickvals=[0, 1],
                                 ticktext=['Non-holiday', 'Holiday']))
    tab2.plotly_chart(fig2, use_container_width=True)
    tab3.plotly_chart(fig3, use_container_width=True)
    tab4.plotly_chart(fig4, use_container_width=True)
    tab5.plotly_chart(fig5, use_container_width=True)
    tab6.plotly_chart(fig6, use_container_width=True)
    st.markdown("By Weather Condition:")
    df = pd.read_csv('day.csv')
    

# 7. Rental Counts by weather situation
    df = pd.read_csv('day.csv')
    tab7, tab8, tab9 = st.tabs(["🌀 by Weather", "🔆 by Temperature", "💦 by Humidity"])
    grouped_weather = df.groupby("weathersit").sum()["cnt"]
    fig7 = px.bar(grouped_weather, title="Rental Counts by Weather situation")
    fig7.update_layout(xaxis_title="Weather Situation", yaxis_title="Rental counts", 
                   xaxis=dict(tickmode='array', tickvals=[1,2,3,4], 
                              ticktext=['Clear, Few clouds, Partly cloudy', 
                                        'Mist + Cloudy, Mist + Broken clouds', 
                                        'Light Snow, Light Rain + Thunderstorm', 
                                        'Heavy Rain + Ice Pallets + Thunderstorm + Snow, Fog']))

# 8. Rental Counts by Temperature
    fig8 = px.scatter(df, x="temp", y="cnt", trendline="lowess", title="Rental Counts by Temperature", trendline_color_override="red")
    fig8.update_layout(xaxis_title="Temperature", yaxis_title="Rental counts")

# 9. Rental Counts by Humidity
    fig9 = px.scatter(df, x="hum", y="cnt", trendline="lowess", title="Rental Counts by Humidity", trendline_color_override="red")
    fig9.update_layout(xaxis_title="Humidity", yaxis_title="Rental counts")

    tab7.plotly_chart(fig7, use_container_width=True)
    tab8.plotly_chart(fig8, use_container_width=True)
    tab9.plotly_chart(fig9, use_container_width=True)
    # above is all about the second page

#--------------------------------------

# Auxiliary functions
def get_season(month):
    if month in [12, 1, 2]:
        return 0
    elif month in [3, 4, 5]:
        return 1
    elif month in [6, 7, 8]:
        return 2
    else:
        return 3

    

#the third page is about the model
def page_model():
    loaded_model = pickle.load(open('trained_model.sav','rb'))
    df = pd.read_csv("preprocessed-df.csv")
    
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
    st.markdown('Time-wise:') 
    col1, col2 = st.columns(2)

    with col1:
        year = st.selectbox('Year', options=[0, 1], format_func=lambda x: year_values[x])
        month = st.selectbox('Month', options=range(1, 13), format_func=lambda x: month_values[x-1])
        weekday = st.selectbox('Weekday', options=[0, 1, 2, 3, 4, 5, 6], format_func=lambda x: weekday_values[x])
        st.header('  ') 
        holiday = st.selectbox('Holiday', options=[0, 1], format_func=lambda x: boolean_values[x])
    with col2:
        st.markdown('Weather-wise:') 
        weather = st.selectbox('Weather', options=[1, 2, 3, 4], format_func=lambda x: weather_values[x-1])
        conv_factor = 41.0
        temp = st.slider('Temperature (°C)', min_value=0, max_value=int(conv_factor), step=1, value=int(0.5*conv_factor), format='%d °C')
        temp_normalized = temp / conv_factor
        conv_factor1 = 67.0
        windspeed = st.slider('Wind Speed (km/h)', min_value=0, max_value=int(conv_factor1), step=1, value=int(0.5*conv_factor1), format='%d km/h')
        windspeed_normalized = windspeed / conv_factor1
        conv_factor2 = 100.0
        humidity = st.slider('Humidity (%)', min_value=0, max_value=int(conv_factor2), step=1, value=int(0.5*conv_factor2), format='%d %%')
        humidity_normalized = humidity / conv_factor2
        

        
                
    input_data = {
        'season': get_season(month),
        'yr': year,
        'mnth': month,
        'holiday': holiday,
        'weekday': weekday,
        'workingday': 1 - holiday,
        'weathersit': weather,
        'atemp': temp_normalized,
        'hum': humidity_normalized,
        'windspeed': windspeed_normalized
    }

    input_df = pd.DataFrame([input_data])

    prediction = loaded_model.predict(input_df)
    
    rounded_prediction = round(prediction[0])
    
    st.subheader('Predicted Number of Bike Rentals:')
    st.markdown(f"<p style='font-size:30px; color:red'>{rounded_prediction}</p>", unsafe_allow_html=True)
    bike_emoji = '<span style="font-size:10px"> 🚲 </span>'
    st.write(bike_emoji * rounded_prediction, unsafe_allow_html=True)
# Run the app
if __name__ == "__main__":
    page_navigation()
