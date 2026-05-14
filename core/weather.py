"""Appels API météo et géocodage via Open-Meteo (gratuit, sans clé).

Fonctions exposées :
    get_coordinates    — recherche lat/lon d'une ville
    get_weather        — récupère les données horaires brutes
    build_weather_dict — transforme le JSON brut en dict propre
    degrees_to_direction — convertit un angle en point cardinal
    get_meteo          — wrapper tout-en-un pour app.py
"""

import requests
import streamlit as st


@st.cache_data
def get_coordinates(ville: str) -> list[dict]:
    """Recherche une ville via l'API geocoding Open-Meteo.

    Args:
        ville: Nom de la ville à rechercher.

    Returns:
        Liste de dicts avec les candidats trouvés (max 5), chacun contenant
        nom, lat, lon, pays, region. Retourne [] si aucun résultat.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": ville,
        "count": 5,
        "language": "fr",
        "format": "json"
    }
    response = requests.get(url=url, params=params).json()
    data = []
    if "results" in response:
        for entry in response["results"]:
            data.append({
                "nom": entry["name"],
                "lat": entry["latitude"],
                "lon": entry["longitude"],
                "pays": entry.get("country", ""),
                "region": entry.get("admin1", "")
            })
    return data


@st.cache_data
def get_weather(lat, lon, date):
    """Récupère les données météo horaires pour une journée via l'API Open-Meteo.

    Args:
        lat: Latitude du lieu.
        lon: Longitude du lieu.
        date: Date de la sortie au format "YYYY-MM-DD".

    Returns:
        JSON brut retourné par l'API (dict), à passer à build_weather_dict.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "temperature_2m", 
            "uv_index", 
            "relative_humidity_2m", 
            "apparent_temperature", 
            "wind_speed_10m", 
            "precipitation_probability", 
            "wind_direction_10m"
        ],
        "start_date": date,
        "end_date": date,
        "timezone": "auto"
    }
    response = requests.get(url=url, params=params).json()
    return response


def build_weather_dict(raw, date, heure_depart, duree):
    """Transforme le JSON brut Open-Meteo en dict propre pour l'application.

    Localise l'index de l'heure de départ dans la liste horaire, puis extrait
    les valeurs météo pertinentes pour cette heure et pour la durée de la sortie.

    Args:
        raw: JSON brut retourné par get_weather.
        date: Date de la sortie au format "YYYY-MM-DD".
        heure_depart: Heure de départ en entier (ex: 8 pour 08:00).
        duree: Durée de la sortie en heures (entier), utilisée pour calculer
               la température ressentie maximale sur la plage horaire.

    Returns:
        Dict avec les clés :
        - temp_depart (float)         : température réelle à l'heure de départ (°C)
        - temp_ressenti (float)       : température ressentie à l'heure de départ (°C)
        - temp_ressenti_max (float)   : température ressentie max sur la durée (°C)
        - vent_vitesse (float)        : vitesse du vent (km/h)
        - vent_direction (str)        : direction du vent en point cardinal (ex: "Ouest")
        - uv_index (float)            : index UV
        - humidite (int)              : humidité relative (%)
        - precipitation_proba (int)   : probabilité de précipitations (%)
    """
    heure_depart = f"{heure_depart:02d}"
    timestamp = date + "T" + heure_depart + ":00"
    time_list = raw["hourly"]["time"]

    try:
        index_depart = time_list.index(timestamp)
    except ValueError:
        return None
    
    weather_dict = {
        "temp_depart": raw["hourly"]["temperature_2m"][index_depart],
        "temp_ressenti": raw["hourly"]["apparent_temperature"][index_depart],
        "temp_ressenti_max": max(raw["hourly"]["apparent_temperature"][index_depart : index_depart + duree]),
        "vent_vitesse": max(raw["hourly"]["wind_speed_10m"][index_depart : index_depart + duree]),
        "vent_direction": degrees_to_direction(raw["hourly"]["wind_direction_10m"][index_depart]),
        "uv_index": max(raw["hourly"]["uv_index"][index_depart : index_depart + duree]),
        "humidite": max(raw["hourly"]["relative_humidity_2m"][index_depart : index_depart + duree]),
        "precipitation_proba": max(raw["hourly"]["precipitation_probability"][index_depart : index_depart + duree])
    }
    return weather_dict


def degrees_to_direction(degres):
    """Convertit un angle en degrés (0-360) en point cardinal. Ex: 270 → 'Ouest'."""
    directions = ["Nord", "Nord-Est", "Est", "Sud-Est", "Sud", "Sud-Ouest", "Ouest", "Nord-Ouest"]
    index = int((degres + 22.5) % 360 / 45)
    return directions[index]

def get_meteo(lat, lon, date, heure, duree):
    """Récupère et transforme les données météo en un seul appel.

    Wrapper qui enchaîne get_weather et build_weather_dict pour simplifier
    l'usage dans app.py.

    Args:
        lat: Latitude du lieu.
        lon: Longitude du lieu.
        date: Date de la sortie au format "YYYY-MM-DD".
        heure: Heure de départ en entier (ex: 8 pour 08:00).
        duree: Durée de la sortie en heures (entier).

    Returns:
        Dict météo propre (voir build_weather_dict), ou None si l'heure
        de départ est introuvable dans les données.
    """
    date = date.strftime("%Y-%m-%d")
    raw = get_weather(lat, lon, date)
    return build_weather_dict(raw, date, heure, duree)