import requests
import pandas as pd

VAR_ID = 64428
YEARS = list(range(2002, 2024))



def clean_code(right_code: str) -> str:
    if len(right_code) != 12:
        raise ValueError("Kod prawy musi mieć 12 znaków")
    return right_code[2] + right_code[3] + right_code[7] + right_code[8:]

def get_data(unit_level):
    base_url = f"https://bdl.stat.gov.pl/api/v1/data/by-variable/{VAR_ID}"
    page = 0   # STARTUJEMY OD 0
    all_rows = []

    while True:
        params = [
            ("format", "json"),
            ("page-size", "100"),
            ("unit-level", unit_level),
            ("page", page),
        ]
        for y in YEARS:
            params.append(("year", y))

        resp = requests.get(base_url, params=params)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])

        print(f"Pobieram stronę {page}, poziomu {unit_level}, liczba wyników: {len(results)}")

        if not results:
            break

        for entry in results:
            row = {
                "Kod": clean_code(entry["id"]),
                "Nazwa": entry["name"],
            }
            for val in entry.get("values", []):
                row[val["year"]] = val["val"]
            all_rows.append(row)

        if len(results) < 100:
            # Ostatnia strona - mniej niż page-size wyników
            break

        page += 1

    return all_rows



def get_data_from_api():
    print("Pobieranie danych z API...")
    powiaty = get_data(5)
    polska = get_data(0)
    wojewodztwa = get_data(2)
    print(f"Łącznie pobrano powiatów: {len(powiaty)}")
    print(f"Łącznie pobrano krajów: {len(polska)}")
    print(f"Łącznie pobrano województw: {len(wojewodztwa)}")


    all_data = powiaty + polska + wojewodztwa

    # Tworzymy DataFrame
    df = pd.DataFrame(all_data)

    df_sorted = df.sort_values(by="Kod").reset_index(drop=True)

    print(df_sorted)
    return df_sorted
