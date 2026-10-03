import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/predict"


st.set_page_config(
    page_title="Projet Goutte d'Eau",
    page_icon="🌧️",
    layout="centered"
)

st.title("🌧️ Projet Goutte d'Eau")
st.subheader("Estimation du risque de pluie")

st.write(
    "Cette interface permet de tester le MVP en envoyant des données météo "
    "à l'API FastAPI afin d'obtenir une estimation du risque de pluie."
)

st.markdown("---")

heure = st.slider("Heure de la journée", min_value=0, max_value=23, value=14)
temperature = st.number_input("Température en °C", value=12.0)
humidite = st.slider("Humidité en %", min_value=0, max_value=100, value=85)
precipitation = st.number_input("Précipitations observées en mm", value=0.5)
vent = st.number_input("Vitesse du vent en km/h", value=20.0)

if st.button("Obtenir la prévision"):
    params = {
        "heure": heure,
        "temperature": temperature,
        "humidite": humidite,
        "precipitation": precipitation,
        "vent": vent
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        result = response.json()

        st.success("Prévision obtenue avec succès")

        st.metric(
            label="Risque de pluie",
            value=f"{round(result['risk'] * 100)} %"
        )

        st.write(f"**Niveau de risque :** {result['level']}")
        st.write(f"**Message :** {result['message']}")

        if result["level"] == "élevé":
            st.warning("Risque élevé : vigilance recommandée.")
        elif result["level"] == "moyen":
            st.info("Risque moyen : à surveiller.")
        else:
            st.success("Risque faible.")

    except requests.exceptions.RequestException:
        st.error(
            "Impossible de contacter l'API. Vérifie que FastAPI est bien lancé."
        )