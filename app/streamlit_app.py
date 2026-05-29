"""Minimal Streamlit app to explore Zepto dataset.
Run: streamlit run app/streamlit_app.py
"""
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv('zepto_v2.csv', encoding='utf-8')

st.title('Zepto Inventory Explorer')

df = load_data()

st.sidebar.header('Filters')
cat = st.sidebar.multiselect('Category', options=sorted(df['category'].unique()), default=None)

if cat:
    df = df[df['category'].isin(cat)]

st.write('Records:', len(df))
st.dataframe(df.head(50))

if 'discountPercent' in df.columns:
    st.bar_chart(df.groupby('category')['discountPercent'].mean().sort_values(ascending=False).head(10))
