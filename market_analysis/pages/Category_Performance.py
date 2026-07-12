import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_data
from src.analytics import get_profitability

st.set_page_config(page_title="Category Performance", page_icon="📊")
st.title("📊 Category Performance & Seasonality")

df = load_data()

try:
    profit_df = get_profitability(df)
except KeyError as e:
    st.error(f"Data error: {e}")
    st.write("Please check your CSV. The current column names are:", df.columns.tolist())
    st.stop()

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

# Reorder days, ensuring we only reorder days that exist in the data
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
days_order = [day for day in days_order if day in heatmap_data.index]
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
