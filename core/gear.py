"""Modèle de données et catalogue des équipements cyclistes.

Ce module est le seul endroit du projet à utiliser de la POO.
Tout le reste (météo, recommandation, UI) s'appuie sur des fonctions.
"""


class GearItem:
    """Représente un équipement cycliste avec ses conditions d'utilisation.

    Attributes:
        nom: Nom de l'équipement.
        partie_du_corps: Zone couverte — "jambes", "torse" ou "extrémités".
        temp_min: Température minimale d'utilisation (°C).
        temp_max: Température maximale d'utilisation (°C).
        disponible: True si l'utilisateur possède cet item (coché en début de session).
    """

    def __init__(
        self,
        nom: str,
        partie_du_corps: str,
        temp_min: int,
        temp_max: int,
        disponible: bool = True,
    ):
        self.nom = nom
        self.partie_du_corps = partie_du_corps
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.disponible = disponible

    def __repr__(self) -> str:
        return (
            f"GearItem({self.nom}, {self.temp_min}°C / {self.temp_max}°C, disponible: {self.disponible})"
        )


# Items disponible=True : considérés comme basiques, cochés par défaut en début de session.
# Items disponible=False : équipement optionnel, l'utilisateur doit le cocher manuellement.
CATALOGUE = [
    GearItem("Cuissard long",           "jambes",       -5,  10),
    GearItem("Cuissard court",          "jambes",       11,  35),
    GearItem("Jambières",               "jambes",        5,   14, disponible=False),
    GearItem("Maillot manches longues", "torse",         8,   12, disponible=False),
    GearItem("Maillot manches courtes", "torse",        13,  35),
    GearItem("Veste hiver",             "torse",        -5,   8),
    GearItem("Veste pluie",             "torse",        10,  35),
    GearItem("Sous maillot hiver",      "torse",        -5,   5),
    GearItem("Sous maillot mi-saison",  "torse",         6,   12, disponible=False),
    GearItem("Sous maillot ete",        "torse",        13,   35, disponible=False),
    GearItem("Gilet sans manches",      "torse",        10,  14),
    GearItem("Manchettes",              "torse",        10,   16, disponible=False),
    GearItem("Couvre-chaussures",       "extrémités",   -5,   5),
    GearItem("Couvre-orteils",          "extrémités",    5,    8, disponible=False),
    GearItem("Gants hiver",             "extrémités",   -5,   5),
    GearItem("Gants légers",            "extrémités",    6,   12, disponible=False),
    GearItem("Bonnet",                  "extrémités",   -5,    5, disponible=False),
]
