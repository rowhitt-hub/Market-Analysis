import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import streamlit as st

def get_profitability(df):
    """Calculates gross margin and total revenue per category."""
    # Defensive check to ensure columns exist before aggregating
    req_cols = ['product_line', 'sales', 'gross_income', 'gross_margin_percentage', 'invoice_id']
    missing = [c for c in req_cols if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns in dataset: {missing}. Available columns: {list(df.columns)}")

    profit = df.groupby('product_line').agg(
        total_revenue=('sales', 'sum'),
        total_profit=('gross_income', 'sum'),
        avg_margin=('gross_margin_percentage', 'mean'),
        transactions=('invoice_id', 'count')
    ).reset_index()
    return profit

def get_basket_rules(df, min_support=0.01):
    """Performs Market Basket Analysis."""
    # Create a simulated basket
    df['basket_id'] = df['branch'] + "_" + df['date'].astype(str) + "_" + df['customer_type']
    
    # Pivot data into a one-hot encoded matrix
    basket = (df.groupby(['basket_id', 'product_line'])['quantity']
              .sum().unstack().reset_index().fillna(0)
              .set_index('basket_id'))
    
    # Resolves AttributeError in pandas>=2.1.0
    basket_sets = basket.map(lambda x: 1 if x > 0 else 0)
    
    # Apply Apriori
    frequent_itemsets = apriori(basket_sets, min_support=min_support, use_colnames=True)
    if frequent_itemsets.empty:
        return pd.DataFrame()
        
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
    
    # Format rules for display
    rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
    return rules
