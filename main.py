import streamlit as st
import plotly.express as px
from src.data_loader import load_data

st.set_page_config(page_title="Supermarket Expansion Study", page_icon="🛒", layout="wide")

st.title("🛒 Supermarket Category Expansion Study")
st.markdown("""
Welcome to the interactive data study. This dashboard analyzes point-of-sale transaction data 
to determine which product categories warrant increased physical shelf space based on profitability, 
purchase frequency, and basket diversity.
""")

df = load_data()

# Executive Summary KPIs
st.header("Executive Summary")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${df['total'].sum():,.2f}")
col2.metric("Total Transactions", f"{len(df):,}")
col3.metric("Top Category (Revenue)", df.groupby('product_line')['total'].sum().idxmax())
col4.metric("Avg Basket Size", f"{df['quantity'].mean():.1f} items")

st.divider()

# High-level Revenue Trend
st.subheader("Revenue Timeline")
daily_sales = df.groupby('date')['total'].sum().reset_index()
fig = px.line(daily_sales, x='date', y='total', title="Daily Revenue Trend")
st.plotly_chart(fig, use_container_width=True)

st.info("👈 **Use the sidebar to navigate through specific analyses.**")