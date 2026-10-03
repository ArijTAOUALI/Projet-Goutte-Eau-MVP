# Projet Goutte d’Eau – MVP

## Objectif du projet

Ce MVP a pour objectif d’estimer le risque de pluie à partir de données météorologiques.

Le projet répond au besoin de France Météo de moderniser ses prévisions de pluie en utilisant des données météo, un modèle de Machine Learning, une API et une interface utilisateur simple.

Le périmètre du MVP est volontairement limité à une seule région afin de prouver la faisabilité technique de la solution.

## Fonctionnement global

La chaîne de fonctionnement est la suivante :

```text
Données météo → Nettoyage → SQLite → Modèle Machine Learning → FastAPI → Streamlit
```

## Technologies utilisées

- Python
- Pandas
- NumPy
- Requests
- SQLite
- Scikit-learn
- Joblib
- FastAPI
- Uvicorn
- Streamlit

## Structure du projet

```text
Projet-Goutte-Eau/
│
├── api/
│   └── main.py
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   └── donnees_meteo.csv
│
├── database/
│   └── meteo.db
│
├── model/
│   └── rain_model.pkl
│
├── scripts/
│   ├── collect_data.py
│   └── train_model.py
│
├── requirements.txt
└── README.md
```

## Installation

Installer les dépendances du projet :

```bash
python -m pip install -r requirements.txt
```

## Lancer le MVP

### 1. Collecter et préparer les données

```bash
python scripts/collect_data.py
```

Cette commande récupère les données météo, les nettoie et les stocke dans une base SQLite.

### 2. Entraîner le modèle

```bash
python scripts/train_model.py
```

Cette commande entraîne le modèle Random Forest et crée le fichier :

```text
model/rain_model.pkl
```

### 3. Lancer l’API FastAPI

```bash
python -m uvicorn api.main:app --reload
```

L’API est accessible à l’adresse :

```text
http://127.0.0.1:8000
```

Exemple de prédiction :

```text
http://127.0.0.1:8000/predict?heure=14&temperature=12&humidite=85&precipitation=0.5&vent=20
```

Exemple de réponse :

```json
{
  "risk": 0.72,
  "level": "élevé",
  "prediction": 1,
  "message": "Risque de pluie élevé"
}
```

### 4. Lancer l’interface Streamlit

Dans un deuxième terminal :

```bash
python -m streamlit run app/streamlit_app.py
```

L’interface est accessible à l’adresse :

```text
http://localhost:8501
```

## Modèle utilisé

Le modèle utilisé est un Random Forest.

Ce modèle est adapté au MVP car il fonctionne bien avec des données structurées, ne nécessite pas de Deep Learning et reste raisonnable en temps d’entraînement.

Le modèle utilise les variables suivantes :

- heure d’observation ;
- température ;
- humidité ;
- précipitations ;
- vent.

Il retourne un niveau de risque de pluie : faible, moyen ou élevé.

## Indicateurs qualité

Les indicateurs utilisés pour évaluer le modèle sont :

- accuracy ;
- précision ;
- recall ;
- F1-score ;
- matrice de confusion.

Ces indicateurs permettent de vérifier si le modèle est suffisamment fiable avant son utilisation dans l’API.

## Éco-responsabilité

Le MVP limite son impact environnemental grâce à plusieurs choix :

- utilisation d’un dataset limité à une seule région ;
- conservation uniquement des variables utiles ;
- utilisation d’un modèle Machine Learning classique ;
- absence de Deep Learning ;
- stockage dans SQLite, une base légère ;
- architecture simple et adaptée au périmètre du MVP.

## Limites du MVP

Le MVP présente certaines limites :

- il est limité à une seule région ;
- la prédiction reste une estimation ;
- le modèle dépend de la qualité des données disponibles ;
- l’interface Streamlit est une première version simple ;
- l’API reste volontairement limitée à une route principale.

## Pistes d’amélioration

Les évolutions possibles sont :

- ajouter plusieurs régions ;
- intégrer davantage de données météo ;
- utiliser des données issues de capteurs IoT ;
- améliorer le modèle avec plus d’historique ;
- ajouter une authentification à l’API ;
- déployer le MVP sur un hébergement responsable ;
- améliorer l’interface utilisateur.

## Conclusion

Ce MVP démontre une chaîne complète et fonctionnelle :

```text
Données météo → Nettoyage → SQLite → Modèle Machine Learning → FastAPI → Streamlit
```

Il permet de prouver la faisabilité technique du projet Goutte d’Eau en estimant un risque de pluie à partir de données météorologiques.