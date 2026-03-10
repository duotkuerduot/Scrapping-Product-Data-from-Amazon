import csv
from typing import Dict, Iterable, List


def save_csv(rows: List[Dict[str, str]], out_file: str, field_names: Iterable[str]) -> None:
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=field_names, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
