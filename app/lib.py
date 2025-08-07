import re

def clean_number(phone: str)->str:
    cleaned = re.sub(r"[^0-9]+", "", str(phone))
    with_city_code_only = str(cleaned)[-10:]
    return with_city_code_only