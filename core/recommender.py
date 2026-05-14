"""Logique de recommandation vestimentaire pour cyclistes.

Calcule une température effective à partir des paramètres de session (météo,
profil thermique, intensité, durée), puis classe chaque item du catalogue en
vert (indispensable), orange (optionnel) ou absent (inutile/non disponible).
"""

from core.gear import CATALOGUE, GearItem

OFFSET_ORANGE = 3

# Offset profil thermique — frileux = température effective plus haute, chaudière = plus basse
OFFSET_SENSIBILITE = {
    "🥶🥶": 3,
    "🥶": 2,
    "😎": 0,
    "🔥": -2,
    "🔥🔥": -3
}

# Réduction de la température effective selon l'intensité de l'effort
OFFSET_INTENSITE = {
    "Endurance": 0,
    "Tempo": -1.5,
    "Intensif": -3
}

# Augmentation de la température effective selon la durée (sorties longues = plus conservateur)
OFFSET_DUREE = {
    "Court": 0,       # < 2h
    "Moyen": 1,       # 2h-4h
    "Long": 2         # > 4h
}


def recommend(apparent_temp, slider, intensite, duree, catalogue):
    """Recommande les équipements adaptés à la session.

    La température effective est calculée ainsi :
        temp_effective = apparent_temp + slider + OFFSET_INTENSITE[intensite] + OFFSET_DUREE[duree]

    Chaque item disponible du catalogue est classé :
    - vert   : temp_effective dans [temp_min, temp_max] de l'item → indispensable
    - orange : temp_effective dans [temp_min - OFFSET_ORANGE, temp_max + OFFSET_ORANGE] → optionnel
    - absent du résultat : inutile ou non disponible

    Args:
        apparent_temp: Température ressentie à l'heure de départ (°C), issue de la météo.
        slider: Offset du profil thermique, entre -3 (j'ai chaud) et +3 (frileux).
        intensite: Niveau d'effort — "Endurance", "Tempo" ou "Intensif".
        duree: Durée de la sortie — "Court", "Moyen" ou "Long".
        catalogue: Liste de GearItem à évaluer.

    Returns:
        Dict avec deux clés :
        - "vert"   : list[GearItem] — équipements indispensables
        - "orange" : list[GearItem] — équipements optionnels
    """

    temp_effective = apparent_temp + slider + OFFSET_INTENSITE[intensite] + OFFSET_DUREE[duree]

    vert = []
    orange = []

    for item in catalogue:
        if item.disponible:
            if item.temp_min <= temp_effective <= item.temp_max:
                vert.append(item)
            elif item.temp_min - OFFSET_ORANGE <= temp_effective <= item.temp_max + OFFSET_ORANGE:
                orange.append(item)
    
    return {"vert": vert, "orange": orange}