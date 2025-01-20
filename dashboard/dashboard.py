import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set_theme(style='dark')

def create_bike_users_daily_df(df):
    bike_users_daily_df = df.groupby(by=['dteday']).agg({
        "casual_day": "first",
        "registered_day": "first",
        "cnt_day": "first"
    }).reset_index()
    return bike_users_daily_df

def create_bike_users_hourly_df(df):
    bike_users_hourly_df = df.groupby(by=['hr']).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
    return bike_users_hourly_df

def create_bike_users_weekly_df(df):
    weekday_order = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    bike_users_weekly_df = df.groupby(by=['weekday']).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reindex(weekday_order).reset_index()
    return bike_users_weekly_df

def create_bike_users_monthly_df(df):
    month = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    bike_users_monthly_df = df.groupby("mnth").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
    bike_users_monthly_df["mnth"] = bike_users_monthly_df["mnth"].map(month)
    return bike_users_monthly_df

def create_bike_users_working_day_df(df):
    bike_users_working_day_df = df.groupby(by=['workingday']).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return bike_users_working_day_df

def create_bike_users_holiday_df(df):
    bike_users_holiday_df = df.groupby(by=['holiday']).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return bike_users_holiday_df

def create_bike_users_season_df(df):
    bike_users_season_df = df.groupby(by=['season']).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return bike_users_season_df

def create_bike_users_weather_df(df):
    bike_users_weather_df = df.groupby(by=['weather']).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return bike_users_weather_df

def create_bike_users_temp_df(df):
    bike_users_temp_df = df.groupby(by=['temp']).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return bike_users_temp_df

all_df = pd.read_csv("./dashboard/all_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

st.header('Bike Sharing Dashboard :bicyclist:')
st.subheader('Daily Trend')

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Date Range',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    choice = st.radio(
    label="User Type:",
    options=('All', 'Registered', 'Casual'),
    horizontal=False
)

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]


bike_users_daily_df = create_bike_users_daily_df(main_df)
bike_users_hourly_df = create_bike_users_hourly_df(main_df)
bike_users_weekly_df = create_bike_users_weekly_df(main_df)
bike_users_monthly_df = create_bike_users_monthly_df(main_df)
bike_users_working_day_df = create_bike_users_working_day_df(main_df)
bike_users_holiday_df = create_bike_users_holiday_df(main_df)

col1, col2 = st.columns(2)
with col1:
    days = len(main_df["dteday"].unique())
    st.metric("Total days", value=days)

with col2:
    if choice == 'Casual':
        bike_users = bike_users_daily_df.casual_day.sum()
        st.metric("Total bike users", value=bike_users)
    elif choice == 'Registered':
        bike_users = bike_users_daily_df.registered_day.sum()
        st.metric("Total bike users", value=bike_users)
    else:
        bike_users = bike_users_daily_df.cnt_day.sum()
        st.metric("Total bike users", value=bike_users)

# Daily Trend
fig, ax = plt.subplots(figsize=(30, 10))
if choice == 'Casual':
    ax.plot(
        bike_users_daily_df["dteday"],
        bike_users_daily_df["casual_day"],
        linewidth=2.5,
        color="#90CAF9"
    )
elif choice == 'Registered':
    ax.plot(
        bike_users_daily_df["dteday"],
        bike_users_daily_df["registered_day"],
        linewidth=2.5,
        color="#90CAF9"
    )
else:
    ax.plot(
        bike_users_daily_df["dteday"],
        bike_users_daily_df["cnt_day"],
        linewidth=2.5,
        color="#90CAF9"
    )
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)

st.pyplot(fig)

st.subheader('Hourly Trend')
if choice == 'All':
    peak_hour = bike_users_hourly_df.loc[bike_users_hourly_df['cnt'].idxmax(), 'hr']
elif choice == 'Registered':
    peak_hour = bike_users_hourly_df.loc[bike_users_hourly_df['registered'].idxmax(), 'hr']
else:
    peak_hour = bike_users_hourly_df.loc[bike_users_hourly_df['casual'].idxmax(), 'hr']
st.metric("Peak hour", value=peak_hour)

fig, ax = plt.subplots(figsize=(30, 10))
if choice == 'All':
    sns.barplot(x="hr", y="cnt", data=bike_users_hourly_df,ax=ax)
elif choice == 'Registered':
    sns.barplot(x="hr", y="registered", data=bike_users_hourly_df,ax=ax)
else:
    sns.barplot(x="hr", y="casual", data=bike_users_hourly_df,ax=ax)

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)

st.pyplot(fig)

st.subheader('Weekly Trend')
if choice == 'All':
    peak_day = bike_users_weekly_df.loc[bike_users_weekly_df['cnt'].idxmax(), 'weekday']
elif choice == 'Registered':
    peak_day = bike_users_weekly_df.loc[bike_users_weekly_df['registered'].idxmax(), 'weekday']
else:
    peak_day = bike_users_weekly_df.loc[bike_users_weekly_df['casual'].idxmax(), 'weekday']
st.metric("Peak day", value=peak_day.capitalize())

fig, ax = plt.subplots(figsize=(30, 10))
if choice == 'All':
    sns.barplot(x="weekday", y="cnt", data=bike_users_weekly_df,ax=ax)
elif choice == 'Registered':
    sns.barplot(x="weekday", y="registered", data=bike_users_weekly_df,ax=ax)
else:
    sns.barplot(x="weekday", y="casual", data=bike_users_weekly_df,ax=ax)
    
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)

st.pyplot(fig)



