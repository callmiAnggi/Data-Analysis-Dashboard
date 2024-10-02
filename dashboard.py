import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# helper functions
def create_monthly_users_2011(df):
    monthly_users_2011 = df[df['yr']==2011].resample(rule='D', on='dteday').agg({
        "registered": "sum",
        "casual": "sum",
        "cnt" : "sum"
    })
    monthly_users_2011 = monthly_users_2011.reset_index()
    monthly_users_2011.rename(columns={'dteday':'date'}, inplace=True)
    return monthly_users_2011

def create_monthly_users_2012(df):
    monthly_users_2012 = df[df['yr'] == 2012].resample(rule='D', on='dteday').agg({
        "registered": "sum",
        "casual": "sum",
        "cnt" : "sum"
    })
    monthly_users_2012 = monthly_users_2012.reset_index()
    monthly_users_2012.rename(columns={'dteday':'date'}, inplace=True)
    return monthly_users_2012

def create_byworkingday_df(df):
    workingday_df = df.groupby(by="workingday").cnt.sum().reset_index()        
    workingday_df.rename(columns={
        "workingday": "working_day",
        "cnt": "total_rental"
    }, inplace=True)
    return workingday_df

#             --LOAD DATA--
day_hour_df = pd.read_csv("day_hour_data.csv")
day_hour_df['dteday'] = pd.to_datetime(day_hour_df['dteday'])

#            --COMPONENT--
min_date = day_hour_df["dteday"].min()
max_date = day_hour_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    # st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='periode',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

storage_df = day_hour_df[(day_hour_df["dteday"] >= str(start_date)) & 
                (day_hour_df["dteday"] <= str(end_date))]

monthly_users_2011 = create_monthly_users_2011(storage_df)
monthly_users_2012 = create_monthly_users_2012(storage_df)
workingday_df = create_byworkingday_df(storage_df)

#        --VISUAL DISPLAY--
st.header('AUTOMATIC RENTAL BIKES SYSTEM')
# in this part will display the dteday as month and total number of bike users (cnt)

st.subheader('bike users per month')

col1, col2 = st.columns(2)
with col1:
    total_users_2011 = monthly_users_2011['cnt'].sum()
    col1.metric("Total users (periode 2011)", value=total_users_2011)
    fig, ax = plt.subplots(figsize=(26, 18))
    ax.plot(
        monthly_users_2011["date"],
        monthly_users_2011["cnt"],
        label='2011',
        marker='o', 
        linewidth=4,
        color="red"
    )
    ax.tick_params(axis='y', labelsize=50)
    ax.tick_params(axis='x', labelsize=55)
    plt.xticks(rotation=45)
    st.pyplot(fig)
with col2:
    total_users_2012 = monthly_users_2012['cnt'].sum()
    col2.metric("Total users (periode 2012)", value=total_users_2012)
    fig, ax = plt.subplots(figsize=(26, 18))
    ax.plot(
        monthly_users_2012["date"],
        monthly_users_2012["cnt"],
        label='2012',
        marker='o', 
        linewidth=4,
        color="blue"
    )
    ax.tick_params(axis='y', labelsize=50)
    ax.tick_params(axis='x', labelsize=55)
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.subheader("bike users during working day vs holiday/weekend")
# col1, col2 = st.columns(2)

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="total_rental", 
    x="working_day",
    data=workingday_df.sort_values(by="total_rental", ascending=False),
    palette=['blue', 'red'],
    ax=ax
    )
for index, value in enumerate(workingday_df.sort_values(by="total_rental", ascending=False)['total_rental']):
    plt.text(index, value, f'{value:,}', ha='center', va='bottom', fontsize=30)

# ax.set_title("Number of Customer by Gender", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)