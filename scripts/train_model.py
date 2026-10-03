import os
import sqlite3

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split


DB_PATH = "database/meteo.db"
MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "rain_model.pkl")


def load_data():
    connection = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM donnees_meteo", connection)
    connection.close()
    return df


def train_model(df):
    # Variables utilisées pour prédire le risque de pluie
    X = df[
        [
            "heure_observation",
            "temperature",
            "humidite",
            "precipitation",
            "vent"
        ]
    ]

    # Variable cible : 0 = risque faible, 1 = risque élevé
    y = df["risque_pluie"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=6
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Évaluation du modèle :")
    print("Accuracy :", round(accuracy_score(y_test, y_pred), 3))
    print("Précision :", round(precision_score(y_test, y_pred), 3))
    print("Recall :", round(recall_score(y_test, y_pred), 3))
    print("F1-score :", round(f1_score(y_test, y_pred), 3))
    print("Matrice de confusion :")
    print(confusion_matrix(y_test, y_pred))

    return model


def save_model(model):
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Modèle sauvegardé : {MODEL_PATH}")


def main():
    print("Chargement des données...")
    df = load_data()

    print("Entraînement du modèle...")
    model = train_model(df)

    save_model(model)

    print("Entraînement terminé.")


if __name__ == "__main__":
    main()