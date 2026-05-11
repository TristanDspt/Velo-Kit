
class GearItem:
    """Représente un équipement cycliste avec ses conditions d'utilisation.

    Attributes:
        nom: Nom de l'équipement.
        partie_du_corps: Zone couverte — "jambes", "torse" ou "extrémités".
        temp_min: Température minimale d'utilisation (°C).
        temp_max: Température maximale d'utilisation (°C).
        disponible: True si l'utilisateur possède cet item (coché en début de session).
        groupe_exclusif: Groupes d'exclusivité mutuels — le recommender ne retient qu'un item par groupe.
    """

    def __init__(
        self,
        nom: str,
        partie_du_corps: str,
        temp_min: int,
        temp_max: int,
        disponible: bool = True,
        groupe_exclusif: list = [],
    ):
        self.nom = nom
        self.partie_du_corps = partie_du_corps
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.disponible = disponible
        self.groupe_exclusif = groupe_exclusif if groupe_exclusif is not None else []

    def __repr__(self) -> str:
        return (
            f"GearItem({self.nom}, {self.temp_min}°C / {self.temp_max}°C, "
            f"disponible: {self.disponible}, groupe: {self.groupe_exclusif})"
        )


# Items disponible=True : considérés comme basiques, cochés par défaut en début de session.
# Items disponible=False : équipement optionnel, l'utilisateur doit le cocher manuellement.
CATALOGUE = [
    GearItem("Cuissard long",           "jambes",       -5,  14, groupe_exclusif=["cuissard"]),
    GearItem("Cuissard court",          "jambes",       12,  35, groupe_exclusif=["cuissard"]),
    GearItem("Jambières",               "jambes",        5,  14, disponible=False),
    GearItem("Maillot manches longues", "torse",         8,  14, disponible=False, groupe_exclusif=["maillot", "manchettes"]),
    GearItem("Maillot manches courtes", "torse",        12,  35, groupe_exclusif=["maillot"]),
    GearItem("Veste hiver",             "torse",        -5,  10, groupe_exclusif=["veste"]),
    GearItem("Veste pluie",             "torse",        10,  35, groupe_exclusif=["veste"]),
    GearItem("Gilet sans manches",      "torse",        10,  14),
    GearItem("Manchettes",              "torse",        10,  16, disponible=False, groupe_exclusif=["manchettes"]),
    GearItem("Couvre-chaussures",       "extrémités",   -5,   8),
    GearItem("Couvre-orteils",          "extrémités",    8,  12, disponible=False),
    GearItem("Gants hiver",             "extrémités",   -5,   8, groupe_exclusif=["gants"]),
    GearItem("Gants légers",            "extrémités",    6,  14, disponible=False, groupe_exclusif=["gants"]),
    GearItem("Bonnet",                  "extrémités",   -5,   5),
]
