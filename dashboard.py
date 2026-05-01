import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set Page Config
st.set_page_config(page_title="E-Commerce Data Dashboard", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

all_df = load_data()

# --- SIDEBAR (FITUR INTERAKTIF) ---
with st.sidebar:
    st.title(" E-Commerce Project")
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Filter Rentang Waktu
    min_date = all_df["order_purchase_timestamp"].min()
    max_date = all_df["order_purchase_timestamp"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataframe berdasarkan input
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

# --- DASHBOARD MAIN PAGE ---
st.header('E-Commerce Performance Dashboard ')

# --- VISUALISASI 1: REVENUE TREND ---
st.subheader('Total Revenue & Growth (2017 Fokus)')

# Menghitung data untuk grafik
revenue_df = main_df.resample(rule='M', on='order_purchase_timestamp').agg({
    "payment_value": "sum"
}).reset_index()
revenue_df.rename(columns={"payment_value": "revenue"}, inplace=True)
revenue_df['growth_pct'] = revenue_df['revenue'].pct_change() * 100

# Metric Cards
col1, col2 = st.columns(2)
with col1:
    total_rev = format_currency(revenue_df.revenue.sum(), "BRL", locale='pt_BR')
    st.metric("Total Revenue", value=total_rev)
with col2:
    # Mengambil growth bulan terakhir yang ada di filter
    last_growth = revenue_df['growth_pct'].iloc[-1] if len(revenue_df) > 1 else 0
    st.metric("Last Month Growth", value=f"{last_growth:.2f}%", delta=f"{last_growth:.2f}%")

# Plotting Line Chart
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x='order_purchase_timestamp', y='revenue', data=revenue_df, marker='o', color='#2ecc71', linewidth=3, ax=ax)

# Tambahkan label persentase pertumbuhan
for i in range(len(revenue_df)):
    growth = revenue_df['growth_pct'].iloc[i]
    if not pd.isna(growth):
        ax.text(revenue_df['order_purchase_timestamp'].iloc[i], 
                revenue_df['revenue'].iloc[i] + (revenue_df['revenue'].max()*0.05), 
                f'{growth:+.1f}%', fontsize=12, ha='center', fontweight='bold', 
                color='green' if growth > 0 else 'red')

ax.set_title("Monthly Revenue Trend", fontsize=20)
ax.set_xlabel(None)
ax.set_ylabel("Revenue (BRL)")
st.pyplot(fig)

# --- VISUALISASI 2: PRODUCT PERFORMANCE ---
st.subheader("Best & Worst Performing Product Category")

# Menghitung volume produk (Hanya status Delivered sudah terjamin di main_data.csv)
category_sales = main_df.groupby('product_category_name_english')['order_item_id'].count().reset_index()
category_sales.rename(columns={'order_item_id': 'total_sold'}, inplace=True)
category_sales = category_sales.sort_values(by='total_sold', ascending=False)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Top 5
sns.barplot(x="total_sold", y="product_category_name_english", data=category_sales.head(5), palette="Greens_r", ax=ax[0])
ax[0].set_title("5 Kategori Produk Terlaris", fontsize=40)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=25)

# Bottom 5
sns.barplot(x="total_sold", y="product_category_name_english", data=category_sales.tail(5).sort_values(by="total_sold", ascending=True), palette="Reds", ax=ax[1])
ax[1].set_title("5 Kategori Produk Terendah", fontsize=40)
ax[1].invert_xaxis() # Supaya bar chart terendah menghadap ke kiri atau tetap rapi
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=25)

st.pyplot(fig)

st.caption('Copyright (c) Devan Project 2024 - Data Terfilter: Status Delivered')