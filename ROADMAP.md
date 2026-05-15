# 🚴 VeloKit — Roadmap

## ✅ Terminé

### Modules core
- `core/gear.py` — classe `GearItem` + `CATALOGUE` (18 items, plages `.0/.1` appliquées)
- `core/weather.py` — géocodage + API Open-Meteo + wrapper `get_meteo`
- `core/recommender.py` — logique de recommandation + offsets corrigés (sensibilité & intensité)

### app.py — UI
- Header + expander "Comment ça marche"
- Bloc localisation — saisie ville, géocodage, date, heure
- Bloc paramètres — intensité, durée, sensibilité
- Bloc météo — emoji géant + 8 métriques
- Bloc matos — checkboxes disponibilité par partie du corps

---

## 🔜 En cours

### app.py — Bloc résultats
- [ ] Affichage recommandations en 3 colonnes (Jambes / Torse / Accessoires)
- [ ] Code couleur 🟢 vert (plage principale) / 🟠 orange (plage étendue)

---

## 🐛 Bugs & fixes à traiter

| Priorité | Description |
|----------|-------------|
| 🔴 Urgent | Trou torse 8.1–12.0°C quand Maillot ML indisponible — pas de fallback |
| 🟠 Important | Veste pluie conditionnelle : apparaît seulement si `precipitation_proba > seuil` + toujours en complément d'autres items |
| 🟠 Important | Maillot UV conditionnel : apparaît seulement si `uv_index > seuil` + plage temp |
| 🟡 Mineur | Logique conditionnelle sous-maillots à affiner |
| ⚪ Edge case | Départ à 23h : l'API ne fetch pas les données du jour suivant |

---

## 🚀 Déploiement
- [ ] Push GitHub
- [ ] Déploiement Streamlit Cloud

---

## 💡 Évolutions futures
- Direction vent dominante sur la sortie
- Icônes météo dynamiques (weathercode)
- Flèches direction vent
- Toggle franchissement de col : si altitude col > seuil → coupe-vent obligatoire + gants si `humidite > seuil`
- Suggestion alternatives items en compétition
- Profil utilisateur persistant