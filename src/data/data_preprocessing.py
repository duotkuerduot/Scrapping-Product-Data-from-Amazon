import re
from typing import Tuple


def parse_title_attributes(title: str) -> Tuple[str, str, str, str, str]:
    """Extracts granular characteristics directly from product title string."""
    brand = title.split(" ")[0] if title else ""

    type_1 = "Inverter" if "inverter" in title.lower() else "Non-Inverter"

    if "split" in title.lower():
        type_2 = "Split"
    elif "window" in title.lower():
        type_2 = "Window"
    else:
        type_2 = ""

    tonnage_match = re.search(r"(\d+(?:\.\d+)?)\s*[Tt]on", title)
    tonnage = tonnage_match.group(1) if tonnage_match else ""

    star_match = re.search(r"(\d)\s*[Ss]tar", title)
    star_rating = star_match.group(1) if star_match else ""

    return brand, type_1, type_2, tonnage, star_rating


def parse_selling_price(price_text: str) -> str:
    if not price_text:
        return ""
    return re.sub(r"[^\d]", "", price_text.split(".")[0])


def parse_review_rating(rating_text: str) -> str:
    review_rating_match = re.search(r"(\d\.\d)", rating_text or "")
    return review_rating_match.group(1) if review_rating_match else ""


def parse_review_count(review_count_text: str) -> str:
    return re.sub(r"[^\d]", "", review_count_text or "")
