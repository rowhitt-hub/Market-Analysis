import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """
    Loads and preprocesses the Kaggle Supermarket Sales dataset.
    Cached by Streamlit to prevent reloading on every UI interaction.
    """
    try:
        # Load the standard Kaggle Supermarket Sales dataset
        df = pd.read_csv("data/supermarket_sales.csv")
        
        # Standardize column names for easier coding
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # Convert Date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Extract useful time features
        df['hour'] = pd.to_datetime(df['time']).dt.hour
        df['day_of_week'] = df['date'].dt.day_name()
        
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please ensure 'supermarket_sales.csv' is in the 'data/' folder.")
        st.stop()