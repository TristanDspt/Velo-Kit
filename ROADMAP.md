# 🚴 VeloKit — Roadmap

## ✅ Terminé

### Modules core
- `core/gear.py` — classe `GearItem` + `CATALOGUE` (18 items, plages `.0/.1` appliquées) + attribut `depends_on`
- `core/weather.py` — géocodage + API Open-Meteo + wrapper `get_meteo`
- `core/recommender.py` — logique de recommandation :
  - Offsets corrigés (sensibilité & intensité)
  - Fix offset durée : `<= 2h` → 0, `<= 4h` → -1, `> 4h` → -2
  - Système de dépendances (`depends_on`) — jambières, manchettes, gilet sans manches
  - Veste pluie conditionnelle : `precipitation_proba > 33%`
  - Maillot UV conditionnel : `uv_index > 8`
  - `temp_effective` retournée dans le dict de résultats
  - `meteo` passé en argument (extensible)
  - Seuils météo externalisés en constantes (`SEUIL_UV`, `SEUIL_PLUIE`)

### app.py — UI
- Header + expander "Comment ça marche"
- Bloc localisation — saisie ville, géocodage, date, heure
- Bloc paramètres — intensité, durée, sensibilité
- Bloc météo — emoji géant + 8 métriques
- Bloc matos — checkboxes dans un expander + "Tout sélectionner"
- Bloc résultats — 3 colonnes (Torse / Jambes / Accessoires), code couleur 🟢/🟠
- Page d'accueil "powered by Team Raclette" avant sélection ville
- Expander debug — catalogue avec plages + `temp_effective`
- Code commenté sur l'ensemble des fichiers

---

## 🚧 En beta (tourne mais logique à affiner)

- Bloc résultats — plages catalogue à calibrer avec retours utilisateurs
- Système de dépendances — cas jambières/cuissard long à affiner (V2)
- Trou torse 8.1–12.0°C quand Maillot ML indisponible — repoussé en V2

---

## 🐛 Bugs & fixes à traiter

| Priorité | Description |
|----------|-------------|
| 🟠 Important | Mise en forme conditionnelle métriques météo — alerte si vent (rafales) / UV / précip / temp > seuil |
| 🟠 Important | `is_recommend` — ajouter param pour chercher uniquement dans `vert` ou `orange` |
| 🟡 Mineur | Logique conditionnelle sous-maillots à affiner |
| ⚪ Edge case | Départ à 23h : l'API ne fetch pas les données du jour suivant |

---

## 🚀 Déploiement
- [x] Push GitHub
- [ ] Déploiement Streamlit Cloud

---

## 💡 Évolutions futures
- Affichage propre de `temp_effective` dans le bloc résultats
- Mise en forme conditionnelle des métriques météo
- Rafales de vent (`wind_gusts`) + précipitations en mm dans le fetch API
- Toggle franchissement de col : coupe-vent + gants si altitude > seuil et humidité > seuil
- Direction vent dominante sur la sortie
- Icônes flèches direction vent à la place des points cardinaux texte
- Icônes météo dynamiques
- Arbre de décision torse complet (V2)
- Suggestion d'alternative quand deux items sont en compétition
- Profil utilisateur persistant