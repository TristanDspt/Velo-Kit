"""Logique de recommandation vestimentaire pour cyclistes.

Calcule une température effective à partir des paramètres de session (météo,
profil thermique, intensité, durée), puis classe chaque item du catalogue en
vert (indispensable), orange (optionnel) ou absent (inutile/non disponible).
"""

from core.gear import CATALOGUE, GearItem

OFFSET_ORANGE = 2

# Offset profil thermique — frileux = température effective plus basse (plus de couches),
# chaudière = température effective plus haute (moins de couches)
OFFSET_SENSIBILITE = {
    "🥶🥶": -2,
    "🥶": -1,
    "😎": 0,
    "🔥": 1,
    "🔥🔥": 2
}

# Offset intensité — plus l'effort est intense, plus on génère de chaleur,
# donc la température effective augmente et on recommande moins de couches
OFFSET_INTENSITE = {
    "Endurance": 0,
    "Tempo": 1,
    "Intensif": 2
}

# Seuils conditionnels météo
SEUIL_UV = 8           # Index UV au-delà duquel le Maillot UV est recommandé
SEUIL_PLUIE = 1.5      # Quantité de pluie en mm au-delà de laquelle la Veste pluie est recommandée


def recommend(meteo, sensibilite, intensite, duree, catalogue):
    """Recommande les équipements adaptés à la session.

    La température effective est calculée ainsi :
        temp_effective = meteo["temp_ressenti"]
                       + OFFSET_SENSIBILITE[sensibilite]
                       + OFFSET_INTENSITE[intensite]
                       + offset_duree

    Où offset_duree est conditionné par la température effective (actif uniquement si temp <= 8°C) :
    - Si temp <= 5°C : offset = -1 si duree > 2h, -2 si duree > 4h
    - Si temp <= 8°C : offset = -1 si duree > 3h, -2 si duree > 6h
    (sorties longues par temps froid = plus conservateur, température effective abaissée)

    Chaque item disponible du catalogue est classé :
    - vert   : temp_effective dans [temp_min, temp_max] de l'item → indispensable
    - orange : temp_effective dans [temp_min - OFFSET_ORANGE, temp_max + OFFSET_ORANGE] → optionnel
    - absent : inutile ou non disponible

    Après classification, deux passes de nettoyage sont appliquées :
    - Dépendances (depends_on) : un item est retiré si son item parent n'est pas recommandé
    - Conditions météo : Maillot UV retiré si uv_index < SEUIL_UV,
                         Veste pluie retirée si precipitation_mm < SEUIL_PLUIE

    Args:
        meteo: Dict météo retourné par get_meteo() — doit contenir au minimum
               "temp_ressenti", "uv_index" et "precipitation_mm".
        sensibilite: Profil thermique — clé de OFFSET_SENSIBILITE (ex: "🥶🥶", "😎", "🔥🔥").
        intensite: Niveau d'effort — "Endurance", "Tempo" ou "Intensif".
        duree: Durée de la sortie en heures (entier ou float).
        catalogue: Liste de GearItem à évaluer.

    Returns:
        Dict avec trois clés :
        - "vert"           : list[GearItem] — équipements indispensables
        - "orange"         : list[GearItem] — équipements optionnels
        - "temp_effective" : float — température effective calculée avec les paramètres utilisateur
    """
    temp_effective = meteo["temp_ressenti"] + OFFSET_SENSIBILITE[sensibilite] + OFFSET_INTENSITE[intensite]

    offset = 0
    if temp_effective <= 8:
        if temp_effective <= 5:
            seuil_bas, seuil_haut = 2, 4
        else:
            seuil_bas, seuil_haut = 3, 6

        if duree <= seuil_bas:
            offset = 0
        elif seuil_bas < duree <= seuil_haut:
            offset = -1
        else:
            offset = -2

    temp_effective += offset

    vert = []
    orange = []

    for item in catalogue:
        if item.disponible:
            if item.temp_min <= temp_effective <= item.temp_max:
                vert.append(item)
            elif item.temp_min - OFFSET_ORANGE <= temp_effective <= item.temp_max + OFFSET_ORANGE:
                orange.append(item)

    # "Trou" si absence de maillot ML
    mc = next((i for i in catalogue if i.nom == "Maillot manches courtes"), None)
    if not is_recommend("Maillot manches longues", vert, orange) and not is_recommend("Veste hiver", vert, []):
        if mc in orange:
            orange.remove(mc)
        if mc and mc.disponible and mc not in vert:
            vert.append(mc)

    # Passe de nettoyage — dépendances et conditions météo
    for item in catalogue:
        # Vérifie les dépendances entre items (et que l'item enfant suive le parent)
        if item.depends_on:
            dependance = is_recommend(item.depends_on, vert, orange)
            if not dependance:
                if item in vert:
                    vert.remove(item)
                elif item in orange:
                    orange.remove(item)
            if dependance == "vert" and item in orange:
                vert.append(item)
                orange.remove(item)
            if dependance == "orange" and item in vert:
                orange.append(item)
                vert.remove(item)

        # Maillot UV — uniquement si index UV suffisant
        if not meteo["uv_index"] >= SEUIL_UV:
            if item in vert and item.nom == "Maillot UV":
                vert.remove(item)
            elif item in orange and item.nom == "Maillot UV":
                orange.remove(item)

        # Veste pluie — uniquement si probabilité de pluie suffisante
        if not meteo["precipitation_mm"] >= SEUIL_PLUIE:
            if item in vert and item.nom == "Veste pluie":
                vert.remove(item)
            elif item in orange and item.nom == "Veste pluie":
                orange.remove(item)

        if "Sous maillot" in item.nom:
            if item in vert:
                vert.remove(item)
                orange.append(item)


    return {"vert": vert, "orange": orange, "temp_effective": temp_effective}


def is_recommend(nom: str, vert: list, orange: list):
    """Vérifie si un item est présent dans les listes de recommandations.

    Args:
        nom: Nom de l'item à rechercher.
        vert: Liste des items indispensables.
        orange: Liste des items optionnels.

    Returns:
        "vert" si l'item est dans vert, "orange" s'il est dans orange, None sinon.
    """
    for item in vert:
        if item.nom == nom:
            return "vert"
    for item in orange:
        if item.nom == nom:
            return "orange"
    return None