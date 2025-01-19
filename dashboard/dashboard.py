import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_theme(style='dark')

def create_bike_users_daily_df(df):
    bike_users_daily_df = all_df.groupby(by=['dteday']).agg({
        "casual_day": "sum",
        "registered_day": "sum",
    }).reset_index()
    return bike_users_daily_df

st.header('Bike Sharing Dashboard')
st.subheader('Total Users')

with st.sidebar:
    pass