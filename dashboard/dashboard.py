import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_theme(style='dark')

def create_bike_users_daily_df(df):
    bike_users_daily_df = df.groupby(by=['dteday']).agg({
        "casual_day": "sum",
        "registered_day": "sum",
    }).reset_index()
    return bike_users_daily_df

def create_bike_users_weekly_df(df):
    weekday_order = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    weekly_users_daily_df = df.groupby(by=['weekday']).agg({
        "casual_day": "sum",
        "registered_day": "sum",
    }).reindex(weekday_order)
    return weekly_users_daily_df

def create_bike_users_hourly(df):
    bike_users_hourly_df = df.groupby(by=['hr']).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return bike_users_hourly_df

def create_bike_users_working_day(df):
    bike_users_working_day_df = df.groupby(by=['workingday']).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return bike_users_working_day_df

def create_bike_users_holiday(df):
    bike_users_holiday_df = df.groupby(by=['holiday']).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return bike_users_holiday_df

def create_bike_users_season(df):
    bike_users_season_df = df.groupby(by=['season']).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return bike_users_season_df

st.header('Bike Sharing Dashboard :bicyclist:')
st.subheader('Total Users')

with st.sidebar:
    pass