SQL Performance Notes

- Index common filter/join columns: `category`, `sku_id` (if present), and `outOfStock` for fast filters.
- Use `EXPLAIN ANALYZE` to profile expensive queries (aggregation over large tables).
- For repeated aggregations, consider summary tables or materialized views (e.g., daily category revenue).
- Avoid SELECT * in production queries; select only needed columns to reduce IO.
- Use appropriate numeric precision for `mrp`/prices to save space when possible.
