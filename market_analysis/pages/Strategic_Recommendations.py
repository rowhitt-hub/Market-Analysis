import streamlit as st
import plotly.express as px
from src.data_loader import load_data
from src.analytics import get_profitability

st.set_page_config(page_title="Strategic Recommendations", page_icon="🎯")
st.title("🎯 Shelf Space Optimization Matrix")

df = load_data()

try:
    profit_df = get_profitability(df)
except KeyError as e:
    st.error(f"Data error: {e}")
    st.stop()

# Calculate a proxy for "Shelf Allocation" (we assume current allocation correlates to inventory quantity)
shelf_proxy = df.groupby('product_line')['quantity'].sum().reset_index()
profit_df = profit_df.merge(shelf_proxy, on='product_line')

# Quadrant Analysis Scatter Plot
st.subheader("The Expansion Quadrant")
fig = px.scatter(
    profit_df,
    x='transactions',
    y='total_profit',
    size='quantity',
    color='product_line',
    hover_name='product_line',
    labels={'transactions': 'Purchase Frequency (Total Invoices)', 'total_profit': 'Total Profit ($)', 'quantity': 'Current Inventory/Shelf Proxy'},
    title="Frequency vs. Profitability"
)

# Add quadrant lines (Medians)
fig.add_hline(y=profit_df['total_profit'].median(), line_dash="dot", annotation_text="Median Profit")
fig.add_vline(x=profit_df['transactions'].median(), line_dash="dot", annotation_text="Median Frequency")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Automated Insights Engine
st.subheader("Automated Shelf Strategies")

med_profit = profit_df['total_profit'].median()
med_freq = profit_df['transactions'].median()

for _, row in profit_df.iterrows():
    cat = row['product_line']
    prof = row['total_profit']
    freq = row['transactions']
    
    if prof > med_profit and freq > med_freq:
        st.success(f"**🌟 Expand Shelf Space: {cat}** (High Profit, High Frequency). This is an anchor category.")
    elif prof > med_profit and freq <= med_freq:
        st.info(f"**🏷️ Increase Promotions: {cat}** (High Profit, Low Frequency). High margin, but needs volume. Place at endcaps.")
    elif prof <= med_profit and freq > med_freq:
        st.warning(f"**📦 Maintain but don't expand: {cat}** (Low Profit, High Frequency). Traffic driver, but low margin. Place at the back of the store.")
    else:
        st.error(f"**📉 Reduce Shelf Space: {cat}** (Low Profit, Low Frequency). Candidate for SKU rationalization.")
