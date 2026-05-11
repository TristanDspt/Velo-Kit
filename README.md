# 🚴 VeloKit — Recommandateur de tenue cycliste

App web légère qui recommande le kit vestimentaire adapté à ta sortie vélo, selon la météo du moment et ton profil.

Accessible via un lien public, sans installation, sans compte.

---

## Demo

> _lien à ajouter après déploiement Streamlit Cloud_

---

## Fonctionnement

Au lancement, l'app récupère automatiquement la météo locale (température + vent) via l'API [Open-Meteo](https://open-meteo.com/), gratuite et sans clé.

Tu renseignes ensuite :
- Le matos que t'as dans ton armoire (checklist)
- Ton profil thermique (frileux ↔ j'ai chaud)
- L'intensité prévue (endurance / tempo / intensif)
- La durée prévue (< 1h30 / 1h30–3h / > 3h)
- Un toggle pluie si la météo auto ne suffit pas

L'app sort ses recommandations avec un code couleur :
- 🟢 **Indispensable**
- 🟠 **Optionnel**
- ⚫ **Inutile** (non affiché si tu ne l'as pas)

---

## Règles de recommandation

Les paramètres sont pris en compte dans cet ordre de priorité :

1. **Disponibilité** — un item non coché n'est jamais recommandé
2. **Intensité** — le paramètre le plus important : intensif = moins de couches
3. **Vent fort** — protection des extrémités même à bonne température
4. **Durée longue** — plus conservateur sur les extrémités
5. **Profil thermique** — décale les seuils de température (± quelques degrés)

---

## Catalogue matos

| Item | Zone | Plage d'utilisation |
|------|------|-------------------|
| Cuissard long | Jambes | -5°C → 14°C |
| Cuissard court | Jambes | 12°C → 35°C |
| Jambières | Jambes | 5°C → 14°C |
| Maillot manches longues | Torse | 8°C → 14°C |
| Maillot manches courtes | Torse | 12°C → 35°C |
| Veste hiver | Torse | -5°C → 10°C |
| Veste pluie | Torse | 10°C → 35°C |
| Gilet sans manches | Torse | 10°C → 14°C |
| Manchettes | Torse | 10°C → 16°C |
| Couvre-chaussures | Extrémités | -5°C → 8°C |
| Couvre-orteils | Extrémités | 8°C → 12°C |
| Gants hiver | Extrémités | -5°C → 8°C |
| Gants légers | Extrémités | 6°C → 14°C |
| Bonnet | Extrémités | -5°C → 5°C |

Les items en **gras** sont cochés par défaut (considérés comme basiques) :
**Cuissard long, Cuissard court, Maillot manches courtes, Veste hiver, Veste pluie, Gilet sans manches, Couvre-chaussures, Gants hiver, Bonnet**

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
├── CLAUDE.md               # Contexte projet pour l'assistant IA
└── README.md
```

---

## Lancer le projet en local

```bash
# Cloner le repo
git clone https://github.com/ton-user/velo_kit.git
cd velo_kit

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

- Suggestion d'alternative quand deux items sont en compétition (ex: cuissard long vs cuissard court à 13°C)
- Profil utilisateur persistant
- Support multi-activités (trail, route, gravel)