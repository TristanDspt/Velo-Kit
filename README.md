# 🚴 VeloKit — Recommandateur de tenue cycliste

App web légère qui recommande le kit vestimentaire adapté à ta sortie vélo, selon la météo du moment et ton profil.

Accessible via un lien public, sans installation, sans compte.

---

## Demo

> _lien à ajouter après déploiement Streamlit Cloud_

---

## Fonctionnement

L'app récupère la météo via l'API [Open-Meteo](https://open-meteo.com/) (gratuite, sans clé) pour la date et l'heure de ta sortie.

Tu renseignes ensuite :
- Le matos que t'as dans ton armoire (checklist)
- Ton profil thermique (frileux ↔ j'ai chaud)
- L'intensité prévue (endurance / tempo / intensif)
- La durée prévue (< 1h30 / 1h30–3h / > 3h)
- La date et l'heure de départ

L'app affiche la météo prévue :
```
Départ : 8°C ressentie | Max sur la sortie : 14°C
Vent : 15 km/h Ouest | UV : 3 | Humidité : 72%
```

Et sort ses recommandations avec un code couleur :
- 🟢 **Indispensable**
- 🟠 **Optionnel**
- ⚫ **Inutile** (non affiché si tu ne l'as pas)

---

## Règles de recommandation

**Température effective = température ressentie + offset profil thermique (± 3°C)**

Les paramètres sont pris en compte dans cet ordre de priorité :

1. **Disponibilité** — un item non coché n'est jamais recommandé
2. **Intensité** — le paramètre le plus important : intensif = moins de couches
3. **Durée longue** — plus conservateur sur les extrémités
4. **Profil thermique** — décale la température effective de -3°C à +3°C

---

## Catalogue matos

| Item | Zone | Plage d'utilisation | Dispo par défaut |
|------|------|---------------------|-----------------|
| Cuissard long | Jambes | -5°C → 12°C | ✅ |
| Cuissard court | Jambes | 10°C → 35°C | ✅ |
| Jambières | Jambes | 5°C → 14°C | ☐ |
| Maillot manches longues | Torse | 8°C → 14°C | ☐ |
| Maillot manches courtes | Torse | 12°C → 35°C | ✅ |
| Veste hiver | Torse | -5°C → 8°C | ✅ |
| Veste pluie | Torse | 10°C → 35°C | ✅ |
| Gilet sans manches | Torse | 10°C → 14°C | ✅ |
| Manchettes | Torse | 10°C → 16°C | ☐ |
| Couvre-chaussures | Extrémités | -5°C → 5°C | ✅ |
| Couvre-orteils | Extrémités | 5°C → 8°C | ☐ |
| Gants hiver | Extrémités | -5°C → 6°C | ✅ |
| Gants légers | Extrémités | 6°C → 12°C | ☐ |
| Bonnet | Extrémités | -5°C → 5°C | ✅ |

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
│
├── core/
│   ├── weather.py          # Appel API Open-Meteo + géolocalisation
│   ├── recommender.py      # Logique de recommandation
│   └── gear.py             # Classe GearItem + catalogue du matos
│
├── requirements.txt
└── README.md
```

---

## Lancer le projet en local

```bash
# Cloner le repo
git clone https://github.com/ton-user/velo-kit.git
cd velo-kit

# Créer et activer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'app
streamlit run app.py
```

---

## Ce que l'app ne fait pas

- Pas de stockage de profil entre les sessions
- Pas d'authentification
- Pas de base de données

---

## Évolutions futures envisagées

- Suggestion d'alternative quand deux items sont en compétition (ex: cuissard long vs cuissard court à 11°C)
- Profil utilisateur persistant
- Support multi-activités (trail, route, gravel)
