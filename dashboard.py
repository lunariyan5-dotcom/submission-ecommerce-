import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="E-Commerce Performance Dashboard", layout="wide")

st.markdown("""
    <style>
    .stDateInput div[data-baseweb="input"] > input {
        caret-color: transparent;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNGSI LOAD DATA ---
@st.cache_data
def load_data():
    # Pastikan main_data.csv sudah ada di folder yang sama
    df = pd.read_csv("main_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

all_df = load_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("E-Commerce Project")
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    st.markdown("### 📅 Periode Analisis")
    
    # Rentang data dikunci hanya 2017 - 2018 sesuai ketersediaan data
    min_date = datetime.date(2017, 1, 1)
    max_date = datetime.date(2018, 12, 31)
    
    try:
        user_date = st.date_input(
            label='Pilih Rentang Tanggal',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
        
        if isinstance(user_date, (list, tuple)) and len(user_date) == 2:
            start_date, end_date = user_date
        else:
            st.info("Silakan pilih tanggal mulai dan tanggal akhir pada kalender.")
            st.stop()
    except Exception:
        st.stop()

    st.markdown("---")
    st.info("""
    **🛠️ Cara Pemakaian Fitur Dashboard:**
    1. Klik kotak tanggal di atas untuk memunculkan kalender.
    2. Pilih **Tanggal Mulai** (Klik pertama).
    3. Pilih **Tanggal Akhir** (Klik kedua).
    """)

# --- 5. FILTERING DATA ---
main_df = all_df[(all_df["order_purchase_timestamp"].dt.date >= start_date) & 
                (all_df["order_purchase_timestamp"].dt.date <= end_date)]

# --- 6. TAMPILAN UTAMA ---
st.header('Performance Dashboard 📊')

# --- VISUALISASI 1: TREN PENDAPATAN & PERTUMBUHAN ---
st.subheader('Monthly Revenue Trend & Growth')

# Agregasi data bulanan
monthly_rev = main_df.resample(rule='M', on='order_purchase_timestamp').agg({"payment_value": "sum"}).reset_index()
monthly_rev['growth'] = monthly_rev['payment_value'].pct_change() * 100

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(monthly_rev["order_purchase_timestamp"], monthly_rev["payment_value"], marker='o', color='#27ae60', linewidth=2.5)

# Menambahkan anotasi persentase pertumbuhan di atas titik data
for i in range(len(monthly_rev)):
    growth = monthly_rev['growth'].iloc[i]
    if not pd.isna(growth):
        color = 'green' if growth > 0 else 'red'
        ax.text(monthly_rev['order_purchase_timestamp'].iloc[i], 
                monthly_rev['payment_value'].iloc[i] * 1.05, 
                f'{growth:+.1f}%', 
                fontsize=10, ha='center', fontweight='bold', color=color)

ax.set_ylabel("Revenue (BRL)")
ax.set_xlabel(None)
ax.grid(axis='y', linestyle='--', alpha=0.3)
st.pyplot(fig)

st.divider()

# --- VISUALISASI 2: PERFORMA KATEGORI PRODUK ---
st.subheader("Product Category Performance")
category_perf = main_df.groupby("product_category_name_english")["order_item_id"].count().sort_values(ascending=False).reset_index()

col1, col2 = st.columns(2)

with col1:
    st.write("**Top 5 Categories (Highest Sales)**")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="order_item_id", y="product_category_name_english", data=category_perf.head(5), palette="Greens_r")
    ax.set_xlabel("Total Items Sold")
    ax.set_ylabel(None)
    st.pyplot(fig)

with col2:
    st.write("**Bottom 5 Categories (Lowest Sales)**")
    # Diurutkan agar yang paling rendah ada di posisi yang rapi
    bottom_5 = category_perf.tail(5).sort_values(by="order_item_id")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="order_item_id", y="product_category_name_english", data=bottom_5, palette="Reds")
    ax.set_xlabel("Total Items Sold")
    ax.set_ylabel(None)
    st.pyplot(fig)

st.caption(f'Data ditampilkan dari periode {start_date} hingga {end_date} | Status: Delivered')
