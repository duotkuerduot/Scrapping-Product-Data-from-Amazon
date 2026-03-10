from datetime import datetime
from pathlib import Path
from typing import List
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import load_config
from etl.extract import get_product_links, make_driver, scrape_product_raw
from etl.load import save_csv
from etl.transform import FIELD_NAMES, build_row, fallback_row


def main() -> None:
    config = load_config()
    root_url = config["root_url"]
    output_csv = config["output_csv"]
    max_products = config["max_products"]

    run_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    driver = make_driver()
    rows: List[dict] = []
    try:
        links = get_product_links(driver, root_url, max_products)
        if len(links) < max_products:
            print(f"Warning: found only {len(links)} product links from root page.")

        for idx, link in enumerate(links[:max_products], start=1):
            try:
                raw = scrape_product_raw(driver, link)
                row = build_row(raw, link, idx, run_datetime)
                rows.append(row)
                print(f"[{idx}/{max_products}] OK")
            except Exception as ex:
                print(f"[{idx}/{max_products}] FAILED: {link} | {ex}")
                rows.append(fallback_row(link, idx, run_datetime))

        save_csv(rows, output_csv, FIELD_NAMES)
        print(f"Saved {len(rows)} rows to {output_csv}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
