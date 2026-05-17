# 🚴 VeloKit — Recommandateur de tenue cycliste

App web légère qui recommande le kit vestimentaire adapté à ta sortie vélo, selon la météo du moment et ton profil.

Accessible via un lien public, sans installation, sans compte.

---

## Demo

[🚴 VeloKit](https://velokit.streamlit.app)

---

## Fonctionnement

L'app récupère la météo via l'API [Open-Meteo](https://open-meteo.com/) (gratuite, sans clé) pour la date et l'heure de ta sortie.

Tu renseignes ensuite :
- Le matos que t'as dans ton armoire (checklist)
- Ton profil thermique (frileux ↔ j'ai chaud)
- L'intensité prévue (endurance / tempo / intensif)
- La durée prévue
- La date et l'heure de départ

L'app affiche la météo prévue et sort ses recommandations avec un code couleur :
- 🟢 **Indispensable**
- 🟠 **Optionnel**

---

## Règles de recommandation

**Température effective = température ressentie + offset profil thermique + offset intensité + offset durée**

Les paramètres sont pris en compte dans cet ordre :

1. **Disponibilité** — un item non coché n'est jamais recommandé
2. **Intensité** — intensif = tu génères plus de chaleur = moins de couches
3. **Durée** — sortie longue par temps froid = plus conservateur (offset actif uniquement si `temp < 8°C`)
4. **Profil thermique** — décale la température effective de -2°C à +2°C

Certains items ont des **dépendances** — ils n'apparaissent que si un autre item est recommandé, et héritent de sa couleur (vert/orange) :
- Jambières → uniquement avec cuissard court
- Manchettes → uniquement avec maillot manches courtes
- Gilet sans manches → uniquement avec maillot manches courtes
- Sous-maillots → toujours affichés en orange (optionnels par définition)

Certains items sont **conditionnels à la météo** :
- Veste pluie → uniquement si précipitations >= 1.5mm sur la durée de la sortie
- Maillot UV → uniquement si index UV >= 8

**Fallback maillot** : si le maillot manches longues est indisponible ou hors plage (et hors conditions hivernales), le maillot manches courtes est automatiquement recommandé en vert.

---

## Catalogue matos

| Item | Zone | Plage d'utilisation | Dispo par défaut |
|------|------|---------------------|-----------------|
| Cuissard long | Jambes | -10°C → 10°C | ✅ |
| Cuissard court | Jambes | 10.1°C → 40°C | ✅ |
| Jambières | Jambes | 8°C → 14°C | ☐ |
| Maillot manches longues | Torse | 8.1°C → 12°C | ☐ |
| Maillot manches courtes | Torse | 12.1°C → 40°C | ✅ |
| Veste hiver | Torse | -10°C → 8°C | ✅ |
| Veste pluie | Torse | 8°C → 40°C | ✅ |
| Maillot UV | Torse | 25°C → 40°C | ☐ |
| Sous maillot hiver | Torse | -10°C → 6°C | ✅ |
| Sous maillot mi-saison | Torse | 6.1°C → 12°C | ☐ |
| Sous maillot été | Torse | 12.1°C → 40°C | ☐ |
| Gilet sans manches | Torse | 10°C → 14°C | ✅ |
| Manchettes | Torse | 10°C → 16°C | ☐ |
| Couvre-chaussures | Extrémités | -10°C → 5°C | ✅ |
| Couvre-orteils | Extrémités | 5.1°C → 8°C | ☐ |
| Gants hiver | Extrémités | -10°C → 6°C | ✅ |
| Gants légers | Extrémités | 6.1°C → 12°C | ☐ |
| Bonnet | Extrémités | -10°C → 5°C | ☐ |

---

## Stack technique

- [Python 3.x](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — UI + déploiement
- [requests](https://requests.readthedocs.io/) — appels API météo
- [Open-Meteo](https://open-meteo.com/) — météo gratuite sans clé

---

## Structure du projet

```
velo_kit/
│
├── app.py                  # Point d'entrée Streamlit, UI principale
├── assets/
│   └── logo_team_raclette_final.png
│
├── core/
│   ├── weather.py          # Appel API Open-Meteo + géolocalisation
│   ├── recommender.py      # Logique de recommandation
│   ├── gear.py             # Classe GearItem + catalogue du matos
│   └── ui.py               # Fonctions HTML mise en forme conditionnelle météo
│
├── .streamlit/
│   └── config.toml         # Thème dark
├── requirements.txt
├── ROADMAP.md
└── README.md
```

---

## Lancer le projet en local

```bash
# Cloner le repo
git clone https://github.com/TristanDspt/Velo-Kit.git
cd Velo-Kit

# Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'app
streamlit run app.py
```

---

## Ce que l'app ne fait pas (pour l'instant)

- Pas de stockage de profil entre les sessions
- Pas d'authentification
- Pas de base de données

---

## Version beta

L'app est en cours de calibration — les plages de température du catalogue sont affinées progressivement avec les retours utilisateurs. Un expander "Debug / Catalogue" est disponible pour visualiser les plages et la température effective calculée.