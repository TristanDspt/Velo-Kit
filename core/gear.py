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
        temp_min: float,
        temp_max: float,
        disponible: bool = True,
        depends_on: str = None,
    ):
        self.nom = nom
        self.partie_du_corps = partie_du_corps
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.disponible = disponible
        self.depends_on = depends_on

    def __repr__(self) -> str:
        return (
            f"GearItem({self.nom}, {self.temp_min}°C / {self.temp_max}°C, disponible: {self.disponible})"
        )


# Items disponible=True : considérés comme basiques, cochés par défaut en début de session.
# Items disponible=False : équipement optionnel, l'utilisateur doit le cocher manuellement.
CATALOGUE = [
    GearItem("Cuissard long",           "jambes",       -10.0,  10.0),
    GearItem("Cuissard court",          "jambes",        10.1,  40.0),
    GearItem("Jambières",               "jambes",         8.0,   14.0, disponible=False, depends_on="Cuissard court"),
    GearItem("Maillot manches longues", "torse",          8.1,   12.0, disponible=False),
    GearItem("Maillot manches courtes", "torse",         12.1,  40.0),
    GearItem("Veste hiver",             "torse",        -10.0,   8.0),
    GearItem("Veste pluie",             "torse",          8.0,  40.0),
    GearItem("Maillot UV",              "torse",         25.0,   40.0, disponible=False),
    GearItem("Sous maillot hiver",      "torse",        -10.0,   6.0),
    GearItem("Sous maillot mi-saison",  "torse",          6.1,   12.0, disponible=False),
    GearItem("Sous maillot ete",        "torse",         12.1,   40.0, disponible=False),
    GearItem("Gilet sans manches",      "torse",         10.0,   14.0, depends_on="Maillot manches courtes"),
    GearItem("Manchettes",              "torse",         10.0,   16.0, disponible=False, depends_on="Maillot manches courtes"),
    GearItem("Couvre-chaussures",       "extrémités",   -10.0,   5.0),
    GearItem("Couvre-orteils",          "extrémités",     5.1,    8.0, disponible=False),
    GearItem("Gants hiver",             "extrémités",   -10.0,   6.0),
    GearItem("Gants légers",            "extrémités",     6.1,   12.0, disponible=False),
    GearItem("Bonnet",                  "extrémités",   -10.0,    5.0, disponible=False),
]
