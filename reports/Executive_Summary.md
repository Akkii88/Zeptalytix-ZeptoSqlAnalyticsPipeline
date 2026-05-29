Executive Summary — Zepto E-commerce SQL Data Analysis

Objective
- Provide quick, actionable insights from the Zepto inventory dataset to demonstrate SQL-driven business analysis.

Dataset
- Source: `zepto_v2.csv` (raw product-level SKUs)
- Sample size (after quick cleaning): 3,731 records

Key metrics (quick run)
- Total records: 3,731
- In-stock products: 3,278 (≈87.9%)
- Out-of-stock products: 453 (≈12.1%)

Top findings
- Discounts: Several SKUs show very high discount percentages (up to ~51%). High-discount SKUs are concentrated in packaged snack categories.
- Stock risk: Some high-MRP items (> ₹500) are out of stock — potential lost revenue and replenishment priority.
- Price-per-gram: A wide distribution; many convenience/packaged items are higher price-per-gram than loose produce.
- Data quality: The dataset includes paise-based prices (needs conversion), and some rows may need deduplication by product/size.

Business recommendations
- Prioritize restocking for high-MRP, out-of-stock items with steady demand to recover revenue.
- Investigate high-discount SKUs: confirm if markdowns are promotional or pricing errors, and adjust margin estimates.
- Use price-per-gram to build value-based product tags (value, premium) for merchandising and search ranking.

Next steps for interview-ready polish
- Produce a 1-page slide summarizing insights and top SQL queries used.
- Add 3–4 annotated notebook cells (in `notebooks/EDA.ipynb`) showing the SQL→pandas workflow and plots.
- Add a small `reports/plots_overview.md` with embedded PNGs for quick visual reference.

Files produced/used
- `Zepto_SQL_data_analysis.sql` — SQL queries and DDL
- `notebooks/EDA.py`, `notebooks/EDA.ipynb` — reproducible EDA and plots
- `plots/top_discounts.png`, `plots/price_per_gram_hist.png`
- `tests/data_quality.py` — quick data checks

If you want, I can now:
- Add a one-slide `slides/` PDF highlighting the above (good for interviews), or
- Insert the executive-summary text at the top of `README.md` and link to the plots.

Which should I do next? (slide PDF or README insertion?)
