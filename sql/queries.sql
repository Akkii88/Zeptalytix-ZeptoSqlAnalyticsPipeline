-- SQL queries and snippets for the Zepto dataset
-- Save this as sql/queries.sql and run against your Postgres DB after importing the CSV

-- 1) Table DDL (example)
CREATE TABLE IF NOT EXISTS zepto (
  sku_id SERIAL PRIMARY KEY,
  category VARCHAR(120),
  name VARCHAR(255) NOT NULL,
  mrp NUMERIC(10,2),
  discountPercent NUMERIC(5,2),
  availableQuantity INTEGER,
  discountedSellingPrice NUMERIC(10,2),
  weightInGms INTEGER,
  outOfStock BOOLEAN,
  quantity INTEGER
);

-- 2) Import hint (psql)
-- \copy zepto(category,name,mrp,discountPercent,availableQuantity,discountedSellingPrice,weightInGms,outOfStock,quantity) FROM 'zepto_v2.csv' CSV HEADER

-- 3) Basic checks
SELECT COUNT(*) AS total_rows FROM zepto;
SELECT COUNT(*) FILTER (WHERE mrp IS NULL OR discountedSellingPrice IS NULL) AS missing_prices FROM zepto;
SELECT COUNT(DISTINCT category) AS categories FROM zepto;

-- 4) Top categories by record count
SELECT category, COUNT(*) AS cnt FROM zepto GROUP BY category ORDER BY cnt DESC LIMIT 20;

-- 5) In-stock vs out-of-stock
SELECT outOfStock, COUNT(*) FROM zepto GROUP BY outOfStock;

-- 6) Top 10 discounts
SELECT name, discountPercent, discountedSellingPrice, mrp FROM zepto WHERE discountPercent IS NOT NULL ORDER BY discountPercent DESC LIMIT 10;

-- 7) Price per gram (where weight known)
SELECT name, weightInGms, discountedSellingPrice, (discountedSellingPrice::numeric / NULLIF(weightInGms,0)) AS price_per_gram FROM zepto WHERE weightInGms > 0 ORDER BY price_per_gram LIMIT 20;

-- 8) Estimated revenue per category
SELECT category, SUM(COALESCE(availableQuantity,0) * COALESCE(discountedSellingPrice,0)) AS est_revenue FROM zepto GROUP BY category ORDER BY est_revenue DESC LIMIT 20;

-- 9) High-MRP out-of-stock items
SELECT name, mrp, availableQuantity FROM zepto WHERE outOfStock = true AND mrp > 500 ORDER BY mrp DESC LIMIT 20;

-- 10) Sample cleaning: remove zero-priced rows
-- CREATE TABLE zepto_clean AS
-- SELECT * FROM zepto WHERE mrp > 0 AND discountedSellingPrice > 0;

-- ------------------------------
-- Advanced SQL examples
-- ------------------------------

-- Window function: rank top discounted products per category
SELECT category, name, discountPercent,
  RANK() OVER (PARTITION BY category ORDER BY discountPercent DESC) AS discount_rank
FROM zepto
WHERE discountPercent IS NOT NULL
ORDER BY category, discount_rank
LIMIT 100;

-- Cohort-style example (by first-seen category month) - requires a date column.
-- This is illustrative; adapt if you have a timestamp column like `first_seen`.
-- WITH first_seen AS (
--   SELECT sku_id, MIN(date_trunc('month', first_seen::date)) AS cohort_month
--   FROM zepto
--   GROUP BY sku_id
-- )
-- SELECT f.cohort_month, date_trunc('month', z.first_seen::date) AS month, COUNT(*)
-- FROM zepto z JOIN first_seen f USING (sku_id)
-- GROUP BY f.cohort_month, date_trunc('month', z.first_seen::date)
-- ORDER BY f.cohort_month, month;

-- Running totals example: cumulative estimated revenue by category
SELECT category, sale_month,
  SUM(month_revenue) AS month_revenue,
  SUM(SUM(month_revenue)) OVER (PARTITION BY category ORDER BY sale_month) AS cumulative_revenue
FROM (
  SELECT category, date_trunc('month', now())::date AS sale_month,
    SUM(COALESCE(availableQuantity,0) * COALESCE(discountedSellingPrice,0)) AS month_revenue
  FROM zepto
  GROUP BY category
) t
GROUP BY category, sale_month
ORDER BY category, sale_month;
