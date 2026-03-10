from typing import Dict, List

from src.data import (
    parse_review_count,
    parse_review_rating,
    parse_selling_price,
    parse_title_attributes,
)

FIELD_NAMES: List[str] = [
    "scrape_datetime",
    "website_url",
    "title",
    "rank",
    "brand",
    "type",
    "type_2",
    "tonnage",
    "star_rating",
    "selling_price",
    "review count",
    "review_rating",
]


def build_row(raw: Dict[str, str], url: str, rank: int, run_datetime: str) -> Dict[str, str]:
    title = raw.get("title", "")
    brand, type_1, type_2, tonnage, star_rating = parse_title_attributes(title)

    selling_price = parse_selling_price(raw.get("price_text", ""))
    review_rating = parse_review_rating(raw.get("rating_text", ""))
    review_count = parse_review_count(raw.get("review_count_text", ""))

    return {
        "scrape_datetime": run_datetime,
        "website_url": url,
        "title": title,
        "rank": str(rank),
        "brand": brand,
        "type": type_1,
        "type_2": type_2,
        "tonnage": tonnage,
        "star_rating": star_rating,
        "selling_price": selling_price,
        "review count": review_count,
        "review_rating": review_rating,
    }


def fallback_row(url: str, rank: int, run_datetime: str) -> Dict[str, str]:
    return {
        "scrape_datetime": run_datetime,
        "website_url": url,
        "title": "",
        "rank": str(rank),
        "brand": "",
        "type": "",
        "type_2": "",
        "tonnage": "",
        "star_rating": "",
        "selling_price": "",
        "review count": "",
        "review_rating": "",
    }
