import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# App Title
st.title("📊 Sales Analysis Dashboard")

# File Upload
file = st.file_uploader("Upload your CSV file", type=["csv"])

if file:
    df = pd.read_csv(file)

    # Clean columns
    df.columns = df.columns.str.strip().str.title()

    # Check necessary columns
    if 'Sales' not in df.columns or 'Order Date' not in df.columns:
        st.error("Required columns like 'Sales' or 'Order Date' not found!")
    else:
        # Convert Order Date
        df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')
        df.dropna(subset=['Order Date'], inplace=True)
        df['Month'] = df['Order Date'].dt.to_period('M')

        # Show dataframe
        if st.checkbox("Show raw data"):
            st.write(df.head())

        # Total Sales
        total_sales = df['Sales'].sum()
        st.metric(label="💰 Total Sales", value=f"₹{total_sales:,.2f}")

        # Sales by Category
        if 'Category' in df.columns:
            st.subheader("🗂️ Sales by Category")
            category_sales = df.groupby('Category')['Sales'].sum().sort_values()
            fig1, ax1 = plt.subplots()
            category_sales.plot(kind='barh', ax=ax1, color='skyblue')
            st.pyplot(fig1)

        # Monthly Sales Trend
        st.subheader("📅 Monthly Sales Trend")
        monthly_sales = df.groupby('Month')['Sales'].sum()
        fig2, ax2 = plt.subplots()
        monthly_sales.plot(ax=ax2, marker='o')
        ax2.set_xlabel("Month")
        ax2.set_ylabel("Sales (₹)")
        st.pyplot(fig2)

        # Top 10 Products
        if 'Product Name' in df.columns:
            st.subheader("🏆 Top 10 Products by Sales")
            top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
            fig3, ax3 = plt.subplots()
            top_products.plot(kind='barh', ax=ax3, color='green')
            ax3.invert_yaxis()
            st.pyplot(fig3)
