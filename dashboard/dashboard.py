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
    month = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]
    bike_users_monthly_df = df.groupby("mnth").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reindex(month).reset_index()
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
    }).reset_index()
    return bike_users_season_df

def create_bike_users_weather_df(df):
    bike_users_weather_df = df.groupby(by=['weathersit']).agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
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
bike_users_season_df = create_bike_users_season_df(main_df)
bike_users_weather_df = create_bike_users_weather_df(main_df)
bike_users_temp_df = create_bike_users_temp_df(main_df)

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
if choice == 'All':
    ax.plot(
        bike_users_daily_df["dteday"],
        bike_users_daily_df["cnt_day"],
        linewidth=2.5,
        color="orange"
    )
elif choice == 'Registered':
    ax.plot(
        bike_users_daily_df["dteday"],
        bike_users_daily_df["registered_day"],
        linewidth=2.5,
        color="#456A50"
    )
else:
    ax.plot(
        bike_users_daily_df["dteday"],
        bike_users_daily_df["casual_day"],
        linewidth=2.5,
    )
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)

st.pyplot(fig)

# Hourly Trend
st.subheader('Hourly Trend')
if choice == 'All':
    peak_hour = bike_users_hourly_df.loc[bike_users_hourly_df['cnt'].idxmax(), 'hr']
    color_column = 'cnt'
    base_color = "#F9CA77"
    highlight_color = "orange"
elif choice == 'Registered':
    peak_hour = bike_users_hourly_df.loc[bike_users_hourly_df['registered'].idxmax(), 'hr']
    color_column = 'registered'
    base_color = "#7DB17D"
    highlight_color = "#3F704D"
else:
    peak_hour = bike_users_hourly_df.loc[bike_users_hourly_df['casual'].idxmax(), 'hr']
    color_column = 'casual'
    base_color = "#5975A4"
    highlight_color = "#2E4E7E"

st.metric("Peak hour", value=peak_hour)

fig, ax = plt.subplots(figsize=(30, 10))
colors = [highlight_color if hr == peak_hour else base_color for hr in bike_users_hourly_df['hr']]
sns.barplot(x="hr", y=color_column, data=bike_users_hourly_df, palette=colors, ax=ax)

ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Weekly Trend
st.subheader('Weekly Trend')
if choice == 'All':
    peak_day = bike_users_weekly_df.loc[bike_users_weekly_df['cnt'].idxmax(), 'weekday']
    color_column = 'cnt'
    base_color = "#F9CA77"
    highlight_color = "orange"
elif choice == 'Registered':
    peak_day = bike_users_weekly_df.loc[bike_users_weekly_df['registered'].idxmax(), 'weekday']
    color_column = 'registered'
    base_color = "#7DB17D"
    highlight_color = "#3F704D"
else:
    peak_day = bike_users_weekly_df.loc[bike_users_weekly_df['casual'].idxmax(), 'weekday']
    color_column = 'casual'
    base_color = "#5975A4"
    highlight_color = "#2E4E7E"

st.metric("Peak day", value=peak_day.capitalize())

fig, ax = plt.subplots(figsize=(30, 10))
colors = [highlight_color if day == peak_day else base_color for day in bike_users_weekly_df['weekday']]

sns.barplot(x="weekday", y=color_column, data=bike_users_weekly_df, palette=colors, ax=ax)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Monthly Trend
st.subheader('Monthly Trend')
if choice == 'All':
    peak_month = bike_users_monthly_df.loc[bike_users_monthly_df['cnt'].idxmax(), 'mnth']
    color_column = 'cnt'
    base_color = "#F9CA77"
    highlight_color = "orange"
elif choice == 'Registered':
    peak_month = bike_users_monthly_df.loc[bike_users_monthly_df['registered'].idxmax(), 'mnth']
    color_column = 'registered'
    base_color = "#7DB17D"
    highlight_color = "#3F704D"
else:
    peak_month = bike_users_monthly_df.loc[bike_users_monthly_df['casual'].idxmax(), 'mnth']
    color_column = 'casual'
    base_color = "#5975A4"
    highlight_color = "#2E4E7E"

st.metric("Peak month", value=peak_month.capitalize())

fig, ax = plt.subplots(figsize=(30, 10))
colors = [highlight_color if month == peak_month else base_color for month in bike_users_monthly_df['mnth']]

sns.barplot(x="mnth", y=color_column, data=bike_users_monthly_df, palette=colors, ax=ax)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Day Type Trend
st.subheader('Bike Sharing Usage Based on Day Type')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30, 10))
if choice == 'All':
    sns.barplot(x="workingday", y="cnt", data=bike_users_working_day_df,color= "orange",ax=ax[0])
    sns.barplot(x="holiday", y="cnt", data=bike_users_holiday_df,color= "orange",ax=ax[1])
elif choice == 'Registered':
    sns.barplot(x="workingday", y="registered", data=bike_users_working_day_df,color= "#456A50",ax=ax[0])
    sns.barplot(x="holiday", y="registered", data=bike_users_holiday_df, color= "#456A50",ax=ax[1])
else:
    sns.barplot(x="workingday", y="casual", data=bike_users_working_day_df,color='#385074',ax=ax[0])
    sns.barplot(x="holiday", y="casual", data=bike_users_holiday_df,color='#385074',ax=ax[1])

ax[0].set_xlabel(None)
ax[0].set_ylabel(None)
ax[0].set_title("Working Day", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

ax[1].set_xlabel(None)
ax[1].set_ylabel(None)
ax[1].set_title("Holiday", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Season Trend
st.subheader('Seasonal Trend')
if choice == 'All':
    peak_season = bike_users_season_df.loc[bike_users_season_df['cnt'].idxmax(), 'season']
    color_column = 'cnt'
    base_color = "#F9CA77"
    highlight_color = "orange"
elif choice == 'Registered':
    peak_season = bike_users_season_df.loc[bike_users_season_df['registered'].idxmax(), 'season']
    color_column = 'registered'
    base_color = "#7DB17D"
    highlight_color = "#3F704D"
else:
    peak_season = bike_users_season_df.loc[bike_users_season_df['casual'].idxmax(), 'season']
    color_column = 'casual'
    base_color = "#5975A4"
    highlight_color = "#2E4E7E"

st.metric("Peak season", value=peak_season.capitalize())

fig, ax = plt.subplots(figsize=(30, 10))
colors = [highlight_color if season == peak_season else base_color for season in bike_users_season_df['season']]

sns.barplot(x="season", y=color_column, data=bike_users_season_df, palette=colors, ax=ax)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Weather Trend
st.subheader('Weather Trend')
if choice == 'All':
    peak_weather = bike_users_weather_df.loc[bike_users_weather_df['cnt'].idxmax(), 'weathersit']
    color_column = 'cnt'
    base_color = "#F9CA77"
    highlight_color = "orange"
elif choice == 'Registered':
    peak_weather = bike_users_weather_df.loc[bike_users_weather_df['registered'].idxmax(), 'weathersit']
    color_column = 'registered'
    base_color = "#7DB17D"
    highlight_color = "#3F704D"
else:
    peak_weather = bike_users_weather_df.loc[bike_users_weather_df['casual'].idxmax(), 'weathersit']
    color_column = 'casual'
    base_color = "#5975A4"
    highlight_color = "#2E4E7E"

st.metric("Peak weather", value=peak_weather)

fig, ax = plt.subplots(figsize=(30, 10))
colors = [highlight_color if weather == peak_weather else base_color for weather in bike_users_weather_df['weathersit']]

sns.barplot(x="weathersit", y=color_column, data=bike_users_weather_df, palette=colors, ax=ax)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.write("*Description :*")
st.write("1 : Clear, Few clouds, Partly cloudy, Partly cloudy")
st.write("2 : Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist")
st.write("3 : Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds")
st.write("4 : Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog")
