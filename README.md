# Amazon Top 50 Product Scraper (ETL)

## Overview
This project implements a lightweight **data engineering ETL pipeline** that scrapes top-ranked products from an Amazon bestsellers category page and writes a structured CSV dataset.

- **Pipeline entrypoint:** `pipelines/pipeline_1.py`
- **Notebook wrapper:** `product_scraping.ipynb`
- **Output dataset:** `amazon_top50.csv`
- **Config file:** `config/config.yaml`
- **Current target category URL:** `https://www.amazon.in/gp/bestsellers/kitchen/3474656031`
- **Configured extract size:** 50 products

The pipeline is designed to:
- **Extract** product links and product-page attributes using Selenium.
- **Transform** raw text into standardized fields (brand, type, tonnage, star rating, numeric price/review fields).
- **Load** the curated records into a quoted CSV file for downstream analytics.

## Project Structure

```
config/
  config.yaml
  __init__.py

data/
  raw/
  processed/

docs/
  README.md

etl/
  extract/
    extract_data.py
  transform/
    transform_data.py
  load/
    load_data.py

pipelines/
  pipeline_1.py

src/
  data/
    data_preprocessing.py
  utils/
    text.py
  validation/
    data_validation.py

tests/
```

## ETL Design

### 1) Extract
Extraction logic in `etl/extract/extract_data.py`:
- Launches Chrome in headless mode with Selenium.
- Reads bestseller listing pages (page 1 and page 2) to collect up to 50 unique product links.
- Uses ASIN parsing to deduplicate links.
- Opens each product URL and captures page-level signals (title, price, rating, review count).

Core extraction methods:
- `make_driver()`
- `get_product_links()`
- `scrape_product_raw()`
- `first_text()`

### 2) Transform
Transformation logic in `etl/transform/transform_data.py` (with helpers in `src/data/data_preprocessing.py`):
- Normalizes text with whitespace cleanup.
- Derives `brand` as the first token in title.
- Derives `type` as `Inverter` vs `Non-Inverter` from title text.
- Derives `type_2` as `Split` or `Window` from title text.
- Uses regex to parse:
  - `tonnage` from patterns like `1.5 Ton`
  - `star_rating` from patterns like `5 Star`
  - `review_rating` from patterns like `4.3`
- Converts `selling_price` and `review count` to digit-only strings.
- Stamps each row with a run-level timestamp (`scrape_datetime`).

Core transformation methods:
- `build_row()`
- `fallback_row()`
- `parse_title_attributes()`

### 3) Load
Load logic in `etl/load/load_data.py`:
- Writes rows to `amazon_top50.csv` using `csv.DictWriter`.
- Enforces a fixed schema (`FIELD_NAMES`).
- Quotes all CSV values (`csv.QUOTE_ALL`) for safe ingestion.
- Preserves rank and URL even when product-level extraction fails (fallback blank fields).

Core load method:
- `save_csv()`

## Output Schema (`amazon_top50.csv`)

Columns produced by the pipeline:
1. `scrape_datetime`
2. `website_url`
3. `title`
4. `rank`
5. `brand`
6. `type`
7. `type_2`
8. `tonnage`
9. `star_rating`
10. `selling_price`
11. `review count`
12. `review_rating`

## Observed Output Characteristics
Based on the provided `amazon_top50.csv`:
- File contains **50 rows**.
- Rank values span **1 to 50**.
- Some records have missing numeric fields where source page values were not captured (for example, blank `selling_price` or blank `review_rating`).
- `scrape_datetime` is constant within a run (single timestamp generated at pipeline start).

## How To Run
Pipeline script:
- `python pipelines/pipeline_1.py`
- Or `python -m pipelines.pipeline_1`

Notebook wrapper:
- Run the single cell in `product_scraping.ipynb`.

Expected artifact after run:
- `amazon_top50.csv` in the project root.

## Dependencies (from code imports)
- Python 3
- `selenium`
- Chrome browser + compatible ChromeDriver available to Selenium
- Standard library modules used: `csv`, `re`, `time`, `datetime`, `typing`

## Reliability Notes
Current implementation includes basic resilience:
- Explicit waits for listing-page elements.
- Multiple selectors for price and rating fields.
- Per-product exception handling with fallback row creation.

Known practical limitations from current logic:
- Category URL is hardcoded (in `config/config.yaml`).
- Parsing quality depends on product-title conventions.
- Dynamic page changes or anti-bot behavior can affect completeness.

## Use Case
This pipeline is suitable as a starter **ecommerce ETL ingestion job** for:
- price monitoring,
- competitive product benchmarking,
- category trend analysis,
- downstream BI/dashboard datasets.
