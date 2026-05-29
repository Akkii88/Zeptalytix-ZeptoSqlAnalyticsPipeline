"""Simple data quality checks for the Zepto dataset.
Run: python tests/data_quality.py
"""
import pandas as pd
import sys

CSV = 'zepto_v2.csv'

def main():
    df = pd.read_csv(CSV, encoding='utf-8')
    errors = []

    # Basic checks
    if df.empty:
        errors.append('Dataset is empty')

    if 'mrp' in df.columns and (df['mrp'] <= 0).any():
        errors.append('Some rows have mrp <= 0')

    if 'discountedSellingPrice' in df.columns and (df['discountedSellingPrice'] <= 0).any():
        errors.append('Some rows have discountedSellingPrice <= 0')

    if 'sku_id' in df.columns and df['sku_id'].duplicated().any():
        errors.append('Duplicate sku_id values found')

    print('Rows:', len(df))
    print('Columns:', list(df.columns))
    print('\nErrors found:')
    if not errors:
        print('No obvious data quality issues found')
        sys.exit(0)
    else:
        for e in errors:
            print('-', e)
        sys.exit(2)

if __name__ == '__main__':
    main()
