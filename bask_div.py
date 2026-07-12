import streamlit as st
from src.data_loader import load_data
from src.analytics import get_basket_rules

st.set_page_config(page_title="Basket Diversity", page_icon="🛍️")
st.title("🛍️ Market Basket Analysis (Diversity)")

st.markdown("""
This page uses the **Apriori Algorithm** to calculate which categories are frequently bought together. 
Categories with high *Lift* are strong anchors that drive cross-selling and deserve prominent shelf placement.
""")

df = load_data()

with st.spinner("Calculating association rules..."):
    rules = get_basket_rules(df)

if rules.empty:
    st.warning("No strong association rules found in the current dataset.")
else:
    # Filter rules
    min_lift = st.slider("Minimum Lift Threshold", 1.0, float(rules['lift'].max()), 1.1)
    filtered_rules = rules[rules['lift'] >= min_lift].sort_values('lift', ascending=False)
    
    # Display table
    st.dataframe(
        filtered_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
        .style.background_gradient(subset=['lift'], cmap='Greens'),
        use_container_width=True
    )
    
    st.info("**How to read this:** If a customer buys the [Antecedent], there is a [Confidence %] chance they will also buy the [Consequent]. A Lift > 1 means they are bought together more often than random chance.")