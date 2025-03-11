import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def monthly_rent(df):
    monthly_rent_df = df.resample(rule='M', on='dteday').agg({"cnt": "sum"})
    monthly_rent_df.index = monthly_rent_df.index.strftime('%B %Y')
    monthly_rent_df = monthly_rent_df.reset_index()
    monthly_rent_df.rename(columns={"dteday": "bulan","cnt": "total_penyewa"}, inplace=True)
    return monthly_rent_df

def hour_rent(df):
    df["workingday"] = df.workingday.apply(lambda x: "Workingday" if x == 1 else "Holiday")
    
    sum_hour_workingday_df = df[df['workingday']=='Workingday'].groupby(["hr"]).cnt.mean().sort_values(ascending=False).reset_index()
    sum_hour_workingday_df['hr'] = list(map(lambda x: f'{x}:00', sum_hour_workingday_df.hr))

    sum_hour_holiday_df = df[df['workingday']=='Holiday'].groupby(["hr"]).cnt.mean().sort_values(ascending=False).reset_index()
    sum_hour_holiday_df['hr'] = list(map(lambda x: f'{x}:00', sum_hour_holiday_df.hr))
    return sum_hour_workingday_df, sum_hour_holiday_df

st.title("Analisis Data Penyewaan Sepeda")
st.image("https://assets.promediateknologi.id/crop/0x0:0x0/0x0/webp/photo/indizone/2022/03/09/Z8sPZ7J/pak-anies-tolong-sepeda-sewa-di-jakarta-kondisinya-memprihatinkan92.jpg")
st.caption("Source: travel.indozone.id")

hour_df = pd.read_csv('dashboard/hour.csv')
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Menambahkan filter berdasarkan rentang tanggal
st.sidebar.header("Filter Tanggal")
start_date = st.sidebar.date_input("Mulai", hour_df["dteday"].min())
end_date = st.sidebar.date_input("Selesai", hour_df["dteday"].max())

if start_date > end_date:
    st.sidebar.error("Tanggal mulai tidak boleh lebih besar dari tanggal selesai")
else:
    hour_df = hour_df[(hour_df["dteday"] >= pd.to_datetime(start_date)) & (hour_df["dteday"] <= pd.to_datetime(end_date))]

st.header("Jumlah Sewa Bulanan")
monthly_rent_df = monthly_rent(hour_df)
with st.container():
    col_1, col_2 = st.columns(2)
    with col_1:
        sum_rent = monthly_rent_df.total_penyewa.sum()
        st.metric("Total Sewa", value=sum_rent)
    with col_2:
        mean_rent = monthly_rent_df.total_penyewa.mean()
        st.metric("Rata-Rata Jumlah Sewa", value=int(mean_rent))

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_rent_df["bulan"],
    monthly_rent_df["total_penyewa"],
    marker='o',
    linewidth=2,
    color="#72BCD4"
)
ax.set_title("Number of Rent Every Month (2011-2012)", loc="center", fontsize=20)
ax.set_xticks(monthly_rent_df.index, monthly_rent_df["bulan"], rotation=45, fontsize=10)
st.pyplot(fig)

st.header("Jumlah Waktu Sewa")
sum_hour_workingday_df, sum_hour_holiday_df = hour_rent(hour_df)

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(24, 12))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="cnt", y="hr", data=sum_hour_workingday_df.head(5), palette=colors, ax=ax[0][0])
ax[0][0].set_ylabel(None)
ax[0][0].set_xlabel(None)
ax[0][0].set_title("Best Performing Hour on Workingday", loc="center", fontsize=15)
ax[0][0].tick_params(axis ='y', labelsize=12)

sns.barplot(x="cnt", y="hr", data=sum_hour_workingday_df.sort_values(by="cnt", ascending=True).head(5), palette=colors, ax=ax[0][1])
ax[0][1].set_ylabel(None)
ax[0][1].set_xlabel(None)
ax[0][1].invert_xaxis()
ax[0][1].yaxis.set_label_position("right")
ax[0][1].yaxis.tick_right()
ax[0][1].set_title("Worst Performing Hour on Workingday", loc="center", fontsize=15)
ax[0][1].tick_params(axis='y', labelsize=12)

sns.barplot(x="cnt", y="hr", data=sum_hour_holiday_df.head(5), palette=colors, ax=ax[1][0])
ax[1][0].set_ylabel(None)
ax[1][0].set_xlabel(None)
ax[1][0].set_title("Best Performing Hour on Holiday", loc="center", fontsize=15)
ax[1][0].tick_params(axis ='y', labelsize=12)

sns.barplot(x="cnt", y="hr", data=sum_hour_holiday_df.sort_values(by="cnt", ascending=True).head(5), palette=colors, ax=ax[1][1])
ax[1][1].set_ylabel(None)
ax[1][1].set_xlabel(None)
ax[1][1].invert_xaxis()
ax[1][1].yaxis.set_label_position("right")
ax[1][1].yaxis.tick_right()
ax[1][1].set_title("Worst Performing on Holiday", loc="center", fontsize=15)
ax[1][1].tick_params(axis='y', labelsize=12)

plt.suptitle("Best and Worst Performing hour by Number of Rent", fontsize=20)
st.pyplot(fig)

st.caption('Copyright (c) Eko Prabowo 2025')
