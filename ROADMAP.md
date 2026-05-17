# 🚴 VeloKit — Roadmap

## ✅ Terminé

### Modules core
- `core/gear.py` — classe `GearItem` + `CATALOGUE` (18 items, plages `.0/.1` appliquées) + attribut `depends_on`
- `core/weather.py` — géocodage + API Open-Meteo + wrapper `get_meteo` + rafales + précipitations mm
- `core/recommender.py` — logique de recommandation :
  - Offsets corrigés (sensibilité & intensité)
  - Offset durée conditionné à la température effective (actif uniquement si `temp < 8°C`)
  - Système de dépendances (`depends_on`) — jambières, manchettes, gilet, sous-maillots
  - Héritage de couleur parent→enfant (vert/orange)
  - Fallback MC si ML indisponible ou hors plage (hors conditions hivernales)
  - Sous-maillots forcés en orange (jamais indispensables)
  - Veste pluie conditionnelle : `precipitation_mm >= 1.5`
  - Maillot UV conditionnel : `uv_index >= 8`
  - `temp_effective` retournée dans le dict de résultats
  - `meteo` passé en argument (extensible)
  - Seuils météo externalisés en constantes (`SEUIL_UV`, `SEUIL_PLUIE`)
- `core/ui.py` — fonctions HTML de mise en forme conditionnelle des métriques météo

### app.py — UI
- Header + expander "Comment ça marche"
- Bloc localisation — saisie ville, géocodage, date, heure
- Bloc paramètres — intensité, durée, sensibilité
- Bloc météo — emoji géant + 10 métriques en HTML avec mise en forme conditionnelle (temp, vent, rafales, UV, pluie)
- Bloc matos — checkboxes dans un expander + "Tout sélectionner" + session_state
- Bloc résultats — 3 colonnes (Torse / Jambes / Accessoires), code couleur 🟢/🟠
- Page d'accueil "powered by Team Raclette" avant sélection ville
- Expander debug — catalogue avec plages + `temp_effective`

---

## 🐛 Bugs connus

| Priorité | Description |
|----------|-------------|
| ⚪ Edge case | Départ à 23h : l'API ne fetch pas les données du jour suivant |

---

## 🚀 Déploiement
- [x] Push GitHub
- [x] Déploiement Streamlit Cloud — https://velo-kit.streamlit.app

---

## 💡 Évolutions futures (dans l'ordre de priorité)
- Prise en compte de `temp_ressenti_max` pour les sorties longues (données déjà disponibles)
- Refactor `recommend()` — découper en sous-fonctions (calcul temp, classification, nettoyage)
- Refactor `CATALOGUE` — dict `{nom: GearItem}` pour accès direct par clé
- Toggle franchissement de col : gants obligatoires si altitude > seuil
- Flèches direction vent à la place des points cardinaux texte
- Icônes météo dynamiques (weathercode)
- Arbre de décision torse complet (V2)
- Suggestion d'alternative quand deux items sont en compétition
- Profil utilisateur persistant