"""Simple ETL script to load `zepto_v2.csv` into Postgres.
Usage (env vars):
  export PGHOST=localhost
  export PGPORT=5432
  export PGUSER=postgres
  export PGPASSWORD=postgres
  export PGDATABASE=zepto
  python etl/etl.py
"""
import os
import csv
import psycopg2

CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'zepto_v2.csv')

CREATE_TABLE = '''
CREATE TABLE IF NOT EXISTS zepto (
  id SERIAL PRIMARY KEY,
  category TEXT,
  name TEXT,
  mrp NUMERIC,
  discountPercent NUMERIC,
  availableQuantity INTEGER,
  discountedSellingPrice NUMERIC,
  weightInGms INTEGER,
  outOfStock BOOLEAN,
  quantity INTEGER
);
'''

COPY_SQL = """
COPY zepto(category,name,mrp,discountPercent,availableQuantity,discountedSellingPrice,weightInGms,outOfStock,quantity)
FROM STDIN WITH CSV HEADER DELIMITER ',' QUOTE '"'
"""


def get_conn():
    return psycopg2.connect(
        host=os.environ.get('PGHOST', 'localhost'),
        port=int(os.environ.get('PGPORT', 5432)),
        user=os.environ.get('PGUSER', 'postgres'),
        password=os.environ.get('PGPASSWORD', ''),
        dbname=os.environ.get('PGDATABASE', 'postgres')
    )


def main():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(CREATE_TABLE)
    conn.commit()

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        cur.copy_expert(COPY_SQL, f)
    conn.commit()
    cur.close()
    conn.close()
    print('Data loaded into table `zepto`')


if __name__ == '__main__':
    main()
