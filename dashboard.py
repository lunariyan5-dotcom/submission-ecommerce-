import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title('Analisis Data E-Commerce Public Dataset')

# Load data
def load_data(file):
    try:
        return pd.read_csv(file)
    except:
        return pd.read_excel(file)

orders = load_data("orders_dataset.csv")
payments = load_data("order_payments_dataset.csv")
items = load_data("order_items_dataset.csv")
products = load_data("products_dataset.csv")
translation = load_data("product_category_name_translation.csv")

# Filter sederhana
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders = orders[orders['order_status'] == 'delivered']

with st.sidebar:
    st.header("Filter")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=orders['order_purchase_timestamp'].min(),
        max_value=orders['order_purchase_timestamp'].max(),
        value=[orders['order_purchase_timestamp'].min(), orders['order_purchase_timestamp'].max()]
    )

df = orders[(orders["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
            (orders["order_purchase_timestamp"] <= pd.to_datetime(end_date))]

# Visualisasi 1: Revenue
st.subheader('Trend Pendapatan')
rev_df = pd.merge(df, payments, on="order_id")
rev_df['month'] = rev_df['order_purchase_timestamp'].dt.to_period('M').dt.to_timestamp()
monthly_rev = rev_df.groupby('month')['payment_value'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(monthly_rev['month'], monthly_rev['payment_value'], marker='o', color='#2ecc71')
st.pyplot(fig)

# Visualisasi 2: Produk
st.subheader('Kategori Produk Terlaris & Terendah')
prod_df = pd.merge(items, products, on="product_id")
prod_df = pd.merge(prod_df, translation, on="product_category_name")
cat_df = prod_df.groupby("product_category_name_english").order_item_id.count().sort_values(ascending=False).reset_index()

c1, c2 = st.columns(2)
with c1:
    st.write("Top 5")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="order_item_id", y="product_category_name_english", data=cat_df.head(5), palette="rocket", ax=ax)
    st.pyplot(fig)

with c2:
    st.write("Bottom 5")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="order_item_id", y="product_category_name_english", data=cat_df.tail(5), palette="rocket", ax=ax)
    st.pyplot(fig)

st.caption('Submission Proyek Akhir - 2026')