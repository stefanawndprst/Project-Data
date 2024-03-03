import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from babel.numbers import format_currency
sns.set(style='dark')

def create_bypayment_df(df):
    bypayment_df = df.groupby(by="payment_type").order_id.nunique().reset_index()
    bypayment_df.rename(columns={
        "order_id": "payment_count"
    }, inplace=True)
    
    return bypayment_df

def create_favproduct_df(df):
    favproduct_df = df.groupby(by="product_category_name_english").product_id.nunique().reset_index()
    favproduct_df.rename(columns={
        "product_id": "product_count"
    }, inplace=True)
    
    return favproduct_df

order_product_df = pd.read_csv(r'https://raw.githubusercontent.com/stefanawndprst/e-commerce-public/main/order_product.csv')

bypayment_df = create_bypayment_df(order_product_df)
favproduct_df = create_favproduct_df(order_product_df)

st.header('Olist Store Dashboard')

col1, col2 = st.columns(2)

with col1 :
    jumlah_orders = order_product_df.order_item_id.sum()
    st.metric("Total penjualan", value=jumlah_orders)

    jumlah_pendapatan = (order_product_df.order_item_id*order_product_df.price).sum()
    st.metric("Total pendapatan", value=jumlah_pendapatan)

with col2 :
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#ce796b"]

    st.subheader('Metode Pembayaran')

    sns.barplot(x="payment_count", y="payment_type", data=bypayment_df.sort_values(by="payment_count", ascending=False).head(5), palette=colors, ax=ax)
    ax.set_xlabel(None)
    ax.set_ylabel("Payment Method", fontsize=30)
    ax.set_title("By Payment", loc="center", fontsize=50)
    ax.tick_params(axis='y', labelsize=30)
    ax.tick_params(axis='x', labelsize=35)
    st.pyplot(fig)

st.subheader('Barang Terlaris')

fig, ax = plt.subplots(figsize=(20, 50))
colors = ["#ce796b"]

sns.barplot(x="product_count", y="product_category_name_english", data=favproduct_df.sort_values(by="product_count", ascending=False), palette=colors, ax=ax)
ax.set_xlabel(None)
ax.set_ylabel("Product Category", fontsize=30)
ax.set_title("The Most Favorite Product", loc="center", fontsize=15)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=35)
st.pyplot(fig)
