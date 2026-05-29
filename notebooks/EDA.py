"""Simple EDA script for Zepto dataset
Run with: python notebooks/EDA.py
Saves a few PNG plots to the `plots/` folder.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style='whitegrid')

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'zepto_v2.csv')
PLOTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'plots')
os.makedirs(PLOTS_DIR, exist_ok=True)

def load_data(path=DATA_PATH):
    df = pd.read_csv(path, encoding='utf-8')
    return df


def basic_overview(df):
    print('Rows, cols:', df.shape)
    display = df.head(5).to_string()
    print('\nSample rows:\n', display)
    print('\nDtypes:\n', df.dtypes)
    print('\nNull counts:\n', df.isnull().sum())


def clean_data(df):
    df = df.copy()
    # coerce numeric columns
    for col in ['mrp', 'discountPercent', 'discountedSellingPrice', 'availableQuantity', 'weightInGms', 'quantity']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # drop rows with missing critical prices
    df = df[~((df['mrp'].isna()) & (df['discountedSellingPrice'].isna()))]

    # drop zero-priced rows
    if 'mrp' in df.columns:
        df = df[~(df['mrp'] == 0)]
    if 'discountedSellingPrice' in df.columns:
        df = df[~(df['discountedSellingPrice'] == 0)]

    # convert paise -> rupees if values look large
    if 'mrp' in df.columns:
        if df['mrp'].max() > 10000:
            df['mrp'] = df['mrp'] / 100.0
            df['discountedSellingPrice'] = df['discountedSellingPrice'] / 100.0

    # price-per-gram (where weight available)
    if 'weightInGms' in df.columns and 'discountedSellingPrice' in df.columns:
        df['price_per_gram'] = df['discountedSellingPrice'] / df['weightInGms'].replace({0: pd.NA})

    return df


def plots(df):
    # Category revenue (approx): availableQuantity * discountedSellingPrice
    if 'availableQuantity' in df.columns and 'discountedSellingPrice' in df.columns and 'category' in df.columns:
        df['est_revenue'] = df['availableQuantity'].fillna(0) * df['discountedSellingPrice'].fillna(0)
        rev = df.groupby('category', dropna=False)['est_revenue'].sum().sort_values(ascending=False).head(15)
        plt.figure(figsize=(10,6))
        sns.barplot(x=rev.values, y=rev.index, palette='viridis')
        plt.xlabel('Estimated Revenue (₹)')
        plt.title('Top 15 Categories by Estimated Revenue')
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, 'top_categories_revenue.png'))
        plt.close()

    # Price-per-gram histogram
    if 'price_per_gram' in df.columns:
        plt.figure(figsize=(8,5))
        sns.histplot(df['price_per_gram'].dropna(), bins=50)
        plt.xlabel('Price per gram (₹)')
        plt.title('Price per gram distribution')
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, 'price_per_gram_hist.png'))
        plt.close()

    # Top discounts
    if 'discountPercent' in df.columns and 'name' in df.columns:
        topd = df.sort_values('discountPercent', ascending=False).dropna(subset=['discountPercent']).head(15)
        plt.figure(figsize=(10,6))
        sns.barplot(x='discountPercent', y='name', data=topd, palette='magma')
        plt.xlabel('Discount %')
        plt.title('Top 15 Discounted Products')
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, 'top_discounts.png'))
        plt.close()


def summaries(df):
    print('\nTotal records:', len(df))
    if 'category' in df.columns:
        print('\nTop categories:\n', df['category'].value_counts().head(10))
    if 'outOfStock' in df.columns:
        print('\nIn-stock vs out-of-stock:\n', df['outOfStock'].value_counts(dropna=False))
    if 'discountPercent' in df.columns:
        print('\nTop 10 discounts:\n', df.sort_values('discountPercent', ascending=False)[['name','discountPercent']].head(10).to_string(index=False))


if __name__ == '__main__':
    df = load_data()
    basic_overview(df)
    df_clean = clean_data(df)
    summaries(df_clean)
    plots(df_clean)
    print('\nPlots saved to', PLOTS_DIR)
