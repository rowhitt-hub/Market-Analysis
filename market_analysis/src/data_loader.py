import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    """
    Loads and preprocesses the Kaggle Supermarket Sales dataset.
    Includes smart pathing to handle nested GitHub repositories.
    """
    # Check for the file in multiple possible locations
    file_path = "data/supermarket_sales.csv"
    if not os.path.exists(file_path):
        file_path = "market_analysis/data/supermarket_sales.csv"
        
    try:
        df = pd.read_csv(file_path)
        
        # Strip whitespace before lowering and replacing spaces to prevent KeyErrors
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Convert Date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Extract useful time features
        if 'time' in df.columns:
            df['hour'] = pd.to_datetime(df['time']).dt.hour
        df['day_of_week'] = df['date'].dt.day_name()
        
        return df
    except FileNotFoundError:
        st.error(f"Data file not found. Checked for '{file_path}'. Please ensure your dataset is uploaded to GitHub.")
        st.stop()
