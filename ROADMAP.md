# 🚴 VeloKit — Roadmap

## ✅ Terminé

### Modules core
- `core/gear.py` — classe `GearItem` + `CATALOGUE` (18 items, plages `.0/.1` appliquées) + attribut `depends_on`
- `core/weather.py` — géocodage + API Open-Meteo + wrapper `get_meteo`
- `core/recommender.py` — logique de recommandation :
  - Offsets corrigés (sensibilité & intensité)
  - Fix offset durée : `< 2h` → `<= 2h`
  - Système de dépendances (`depends_on`) — jambières, manchettes, gilet sans manches
  - `temp_effective` retournée dans le dict de résultats
  - `meteo` passé en argument pour conditions météo futures

### app.py — UI
- Header + expander "Comment ça marche"
- Bloc localisation — saisie ville, géocodage, date, heure
- Bloc paramètres — intensité, durée, sensibilité
- Bloc météo — emoji géant + 8 métriques
- Bloc matos — checkboxes dans un expander
- Expander debug — catalogue avec plages + `temp_effective`

---

## 🚧 En beta (tourne mais logique à affiner)

- Bloc résultats — 3 colonnes (Jambes / Torse / Accessoires), code couleur 🟢/🟠
- Système de dépendances — fonctionne mais plages catalogue à calibrer

---

## 🐛 Bugs & fixes à traiter

| Priorité | Description |
|----------|-------------|
| 🔴 Urgent | Trou torse 8.1–12.0°C quand Maillot ML indisponible — pas de fallback |
| 🟠 Important | Veste pluie conditionnelle : apparaît seulement si `precipitation_proba > seuil` + toujours en complément d'autres items |
| 🟠 Important | Maillot UV conditionnel : apparaît seulement si `uv_index > seuil` + plage temp |
| 🟠 Important | Mise en forme conditionnelle métriques météo — alerte si vent / UV / précip / temp > seuil |
| 🟡 Mineur | Logique conditionnelle sous-maillots à affiner |
| ⚪ Edge case | Départ à 23h : l'API ne fetch pas les données du jour suivant |

---

## 🚀 Déploiement
- [ ] Push GitHub
- [ ] Déploiement Streamlit Cloud

---

## 💡 Évolutions futures
- Affichage de la température effective dans le bloc résultats
- Mise en forme conditionnelle des métriques météo (alertes vent / UV / pluie)
- Toggle franchissement de col : coupe-vent + gants si altitude > seuil et humidité > seuil
- Direction vent dominante sur la sortie
- Icônes météo dynamiques
- Suggestion d'alternative quand deux items sont en compétition
- Profil utilisateur persistant