import streamlit as st
import plotly.express as px
from src.data_loader import load_data
from src.analytics import get_profitability
import pandas as pd

st.set_page_config(page_title="Category Performance", page_icon="📊")
st.title("📊 Category Performance & Seasonality")

df = load_data()
profit_df = get_profitability(df)

# Profitability Chart
st.subheader("Revenue vs. Profit by Category")
fig_bar = px.bar(
    profit_df, 
    x='product_line', 
    y=['total_revenue', 'total_profit'], 
    barmode='group',
    labels={'value': 'USD ($)', 'product_line': 'Category', 'variable': 'Metric'}
)
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# Seasonality Heatmap
st.subheader("Seasonal Shopping Behaviors")
category = st.selectbox("Select a Category to view buying patterns:", df['product_line'].unique())

filtered_df = df[df['product_line'] == category]
heatmap_data = pd.crosstab(filtered_df['day_of_week'], filtered_df['hour'])

# Reorder days
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
heatmap_data = heatmap_data.reindex(days_order)

fig_heat = px.imshow(
    heatmap_data, 
    labels=dict(x="Hour of Day", y="Day of Week", color="Transactions"),
    x=heatmap_data.columns,
    y=heatmap_data.index,
    color_continuous_scale="Viridis",
    title=f"Peak Purchasing Times for {category}"
)
st.plotly_chart(fig_heat, use_container_width=True)