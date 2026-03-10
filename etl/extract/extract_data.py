import re
import time
from typing import Dict, List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils import clean_text


def make_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,2200")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    return webdriver.Chrome(options=options)


def extract_asin(url: str) -> str:
    m = re.search(r"/dp/([A-Z0-9]{10})", url)
    return m.group(1) if m else ""


def get_product_links(driver: webdriver.Chrome, root_url: str, max_products: int) -> List[str]:
    links: List[str] = []
    seen_asins = set()
    page = 1

    while len(links) < max_products and page <= 2:
        current_url = root_url if page == 1 else f"{root_url}/ref=zg_bs_pg_{page}_kitchen?ie=UTF8&pg={page}"
        driver.get(current_url)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.a-link-normal[href*='/dp/']"))
            )
        except TimeoutException:
            print(f"Timeout waiting for elements on page {page}")
            break

        time.sleep(3)

        candidates = driver.find_elements(By.CSS_SELECTOR, "a.a-link-normal[href*='/dp/']")

        for a in candidates:
            href = (a.get_attribute("href") or "").split("?")[0]
            asin = extract_asin(href)
            if not asin or asin in seen_asins:
                continue
            seen_asins.add(asin)
            links.append(href)
            if len(links) >= max_products:
                break
        page += 1

    return links


def first_text(driver: webdriver.Chrome, selectors: List[Dict[str, str]]) -> str:
    for sel in selectors:
        try:
            el = driver.find_element(sel["by"], sel["value"])
            txt = clean_text(el.text)
            if txt:
                return txt
        except NoSuchElementException:
            continue
    return ""


def scrape_product_raw(driver: webdriver.Chrome, url: str) -> Dict[str, str]:
    driver.get(url)
    time.sleep(2)

    title = first_text(driver, [{"by": By.ID, "value": "productTitle"}])

    price_text = first_text(
        driver,
        [
            {"by": By.CSS_SELECTOR, "value": "span.a-price.aok-align-center span.a-offscreen"},
            {"by": By.CSS_SELECTOR, "value": "span.a-price span.a-offscreen"},
            {"by": By.ID, "value": "corePriceDisplay_desktop_feature_div"},
        ],
    )

    rating_text = first_text(
        driver,
        [
            {"by": By.CSS_SELECTOR, "value": "span[data-hook='rating-out-of-text']"},
            {"by": By.CSS_SELECTOR, "value": "i.a-icon-star span.a-icon-alt"},
        ],
    )

    review_count_text = first_text(driver, [{"by": By.ID, "value": "acrCustomerReviewText"}])

    return {
        "title": title,
        "price_text": price_text,
        "rating_text": rating_text,
        "review_count_text": review_count_text,
    }
