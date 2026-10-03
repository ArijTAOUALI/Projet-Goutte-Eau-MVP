import os
import sqlite3
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests


DATA_DIR = "data"
DATABASE_DIR = "database"

CSV_PATH = os.path.join(DATA_DIR, "donnees_meteo.csv")
DB_PATH = os.path.join(DATABASE_DIR, "meteo.db")


def create_folders():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(DATABASE_DIR, exist_ok=True)


def collect_from_api():
    """
    Collecte des données météo depuis une API publique.
    Région utilisée pour le MVP : Île-de-France / Paris.
    """

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "start_date": "2024-01-01",
        "end_date": "2024-03-31",
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "timezone": "Europe/Paris"
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()
    hourly = data["hourly"]

    df = pd.DataFrame({
        "date_heure": hourly["time"],
        "temperature": hourly["temperature_2m"],
        "humidite": hourly["relative_humidity_2m"],
        "precipitation": hourly["precipitation"],
        "vent": hourly["wind_speed_10m"],
    })

    df["region"] = "Île-de-France"
    return df


def create_demo_data():
    """
    Données de secours si l'API ne répond pas.
    Cela permet quand même de tester le MVP.
    """

    dates = pd.date_range(start="2024-01-01", periods=500, freq="h")

    df = pd.DataFrame({
        "date_heure": dates,
        "temperature": np.random.normal(12, 6, len(dates)).round(1),
        "humidite": np.random.randint(45, 100, len(dates)),
        "precipitation": np.random.choice([0, 0, 0, 0.2, 0.5, 1.2, 2.0], len(dates)),
        "vent": np.random.normal(15, 5, len(dates)).round(1),
        "region": "Île-de-France"
    })

    return df


def clean_data(df):
    """
    Nettoyage simple des données.
    """

    df = df.drop_duplicates()
    df = df.dropna()

    df["date_heure"] = pd.to_datetime(df["date_heure"])
    df["date_observation"] = df["date_heure"].dt.date
    df["heure_observation"] = df["date_heure"].dt.hour

    # Variable cible du modèle :
    # 1 = risque élevé de pluie
    # 0 = risque faible
    df["risque_pluie"] = np.where(
        (df["precipitation"] > 0.2) | (df["humidite"] > 80),
        1,
        0
    )

    df = df[
        [
            "date_observation",
            "heure_observation",
            "region",
            "temperature",
            "humidite",
            "precipitation",
            "vent",
            "risque_pluie"
        ]
    ]

    return df


def save_to_csv(df):
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")
    print(f"Fichier CSV créé : {CSV_PATH}")


def save_to_sqlite(df):
    connection = sqlite3.connect(DB_PATH)

    df.to_sql(
        "donnees_meteo",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()
    print(f"Base SQLite créée : {DB_PATH}")


def main():
    create_folders()

    try:
        print("Collecte des données depuis l'API...")
        df = collect_from_api()
    except Exception as error:
        print("Erreur API, création de données de démonstration.")
        print(error)
        df = create_demo_data()

    print("Nettoyage des données...")
    df_clean = clean_data(df)

    save_to_csv(df_clean)
    save_to_sqlite(df_clean)

    print("Collecte et stockage terminés.")
    print(df_clean.head())


if __name__ == "__main__":
    main()