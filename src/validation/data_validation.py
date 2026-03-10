from typing import Dict, Iterable


def validate_row_schema(row: Dict[str, str], field_names: Iterable[str]) -> bool:
    return set(row.keys()) == set(field_names)
