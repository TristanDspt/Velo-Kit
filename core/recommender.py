"""Logique de recommandation vestimentaire pour cyclistes.

Calcule une température effective à partir des paramètres de session (météo,
profil thermique, intensité, durée), puis classe chaque item du catalogue en
vert (indispensable), orange (optionnel) ou absent (inutile/non disponible).
"""

from core.gear import CATALOGUE, GearItem
import streamlit as st
OFFSET_ORANGE = 2

# Offset profil thermique — frileux = température effective plus basse, chaudière = plus haute
OFFSET_SENSIBILITE = {
    "🥶🥶": -2,
    "🥶": -1,
    "😎": 0,
    "🔥": 1,
    "🔥🔥": 2
}

# Réduction de la température effective selon l'intensité de l'effort
OFFSET_INTENSITE = {
    "Endurance": 0,
    "Tempo": 1,
    "Intensif": 2
}


def recommend(apparent_temp, sensibilite, intensite, duree, catalogue):
    """Recommande les équipements adaptés à la session.

    La température effective est calculée ainsi :
        temp_effective = apparent_temp + OFFSET_SENSIBILITE[sensibilite] + OFFSET_INTENSITE[intensite] + offset_duree

    Où offset_duree vaut 0 si duree < 2h, 1 si duree <= 4h, 2 au-delà
    (sorties longues = plus conservateur sur les extrémités).

    Chaque item disponible du catalogue est classé :
    - vert   : temp_effective dans [temp_min, temp_max] de l'item → indispensable
    - orange : temp_effective dans [temp_min - OFFSET_ORANGE, temp_max + OFFSET_ORANGE] → optionnel
    - absent du résultat : inutile ou non disponible

    Args:
        apparent_temp: Température ressentie à l'heure de départ (°C), issue de la météo.
        sensibilite: Profil thermique — clé de OFFSET_SENSIBILITE (ex: "🥶🥶", "😎", "🔥🔥").
        intensite: Niveau d'effort — "Endurance", "Tempo" ou "Intensif".
        duree: Durée de la sortie en heures (entier ou float).
        catalogue: Liste de GearItem à évaluer.

    Returns:
        Dict avec deux clés :
        - "vert"   : list[GearItem] — équipements indispensables
        - "orange" : list[GearItem] — équipements optionnels
    """
    if duree <= 2:
        offset = 0
    elif duree <= 4:
        offset = 1
    else:
        offset = 2
    
    temp_effective = apparent_temp + OFFSET_SENSIBILITE[sensibilite] + OFFSET_INTENSITE[intensite] + offset
    st.write(f"temp_effective: {temp_effective}")

    vert = []
    orange = []

    for item in catalogue:
        if item.disponible:
            if item.temp_min <= temp_effective <= item.temp_max:
                vert.append(item)
            elif item.temp_min - OFFSET_ORANGE <= temp_effective <= item.temp_max + OFFSET_ORANGE:
                orange.append(item)
    
    return {"vert": vert, "orange": orange}