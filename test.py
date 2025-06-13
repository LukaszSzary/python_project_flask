import requests
import pandas as pd

VAR_ID = 64428
YEARS = list(range(2002, 2024))
params = {"format": "json" , "page-size": 100}
for y in YEARS:
    params.setdefault("year", []).append(y)

url = f"https://bdl.stat.gov.pl/api/v1/data/by-variable/{VAR_ID}"
#headers = {"X-ClientId": "TWÓJ_KLUCZ_API"}


resp = requests.get(url, params=params)
resp.raise_for_status()
vals = resp.json()["results"]
print(f"Received {len(vals)} records")

