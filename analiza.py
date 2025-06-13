import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from pymongo import MongoClient
import data_from_api


# Dane wejściowe jako string CSV

# Wczytaj dane do DataFrame
df = data_from_api.get_data_from_api()


#usunięcie całego wiersza, jesli ma pusta wartosc
df = df.dropna()

# Lata (features) i przygotowanie modelu
years = np.array(list(range(2002, 2024))).reshape(-1, 1)


# Dopasowanie regresji dla każdej jednostki
results = []
for _, row in df.iterrows():
    values = np.array(row[2:].astype(float)).reshape(-1, 1)
    values_dict = row.iloc[2:].to_dict()
    model = LinearRegression().fit(years, values)
    a = model.coef_[0][0]
    b = model.intercept_[0]
    results.append({
        "Kod": row["Kod"],
        "Nazwa": row["Nazwa"],
        "a": a,
        "b": b,
        "2025": model.predict([[2025]])[0][0],
        "values":  values_dict
    })

# Konwersja wyników do DataFrame
results_df = pd.DataFrame(results)
print(results_df.tail())

kody_nazwy = df[['Kod', 'Nazwa']].set_index('Kod').to_dict()['Nazwa']


#export do MongoDB
uri = os.environ['MONGO_FLASK']

#client = MongoClient(uri)
#db = client['db_Flask']

#collection_dane = db['dane']

#collection_dane.insert_many(results_df.to_dict('records'))


#collection = db['kody_nazwy']
#collection.insert_many(df[['Kod', 'Nazwa']].to_dict('records'))

print(results_df.tail())
print(df.tail())