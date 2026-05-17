import streamlit as st
from core.gear import CATALOGUE
from core.weather import get_coordinates, get_meteo, weathercode_to_emoji
from core.recommender import recommend
from core import ui
from datetime import date, timedelta

# Initialisation session_state — une seule fois par session utilisateur
# Evite de muter les objets du CATALOGUE qui sont partagés entre sessions sur Streamlit Cloud
if "disponibilite" not in st.session_state:
    st.session_state["disponibilite"] = {item.nom: item.disponible for item in CATALOGUE}

# --- Configuration de la page ---
st.set_page_config(page_title="VeloKit", page_icon="🚴", layout="wide")

# CSS global — centrage des blocs horizontaux et des radio buttons
st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] {
        align-items: center;
        justify-content: center;
    }
    div.stRadio > div {
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center; margin-top: -80px; margin-bottom: 10px;'>🚴 Velo Kit 🚴</h1>", unsafe_allow_html=True)

# --- Explications ---
with st.expander("Comment ça marche ❓"):
    st.markdown("""
        Renseigne ta ville, la date et l heure de départ — l'app récupère automatiquement 
        la météo. Coche ensuite le matos que t'as dans ton armoire, 
        règle ton profil thermique, ton intensité prévue et la durée de ta sortie.

        VeloKit te sort une liste d'équipements classés en :  
        🟢 La tenue de base pour cette sortie  
        🟠 Optionnel — selon ta sensibilité

        Les recommandations s'adaptent à la température ressentie, pas à la température réelle.
    """)

# --- Bloc saisie : localisation, date, heure, paramètres de sortie ---
with st.expander("Détails de ta sortie", expanded=True):

    col1, _, col2, _, col3, _, col4 = st.columns([1.2,0.2,2,0.2,2,0.4,2.5])

    with col1:
        ville_saisie = st.text_input(
            label="Ville",
            help="Saisis le nom de ta ville"
        )
        ville = get_coordinates(ville_saisie)

    with col2:
        ville_select = st.selectbox(
            label="Choix",
            help="Choisis ta ville dans la liste",
            options=ville,
            format_func=lambda x: f"{x['nom']}, {x['region']}, {x['pays']}"
        )

    with col3:
        date_depart = st.date_input(
            label="Date",
            min_value=date.today(),
            max_value=date.today() + timedelta(days=7),
            value=date.today() + timedelta(days=1),
        )

    with col4:
        heure = st.slider(
            label="Heure de départ",
            max_value=24,
            value=9
        )

    _, col5, _, col6, _, col7, _ = st.columns([1,2,1,2,1,2,1])

    with col5:
        intensite = st.pills(
            label="Intensité",
            options=["Endurance", "Tempo", "Intensif"],
            default="Endurance"
        )

    with col6:
        duree = st.slider(
            label="Durée",
            max_value=8,
            value=2
        )

    with col7:
        sensibilite = st.pills(
            label="Sensibilitée",
            help="Ajoute ou retire 1°, 2°",
            options=["🥶🥶", "🥶", "😎", "🔥", "🔥🔥"],
            default="😎"
        )


if ville_select:
    lat = ville_select["lat"]
    lon = ville_select["lon"]

    # --- Bloc météo ---
    with st.container(border=True):
        meteo = get_meteo(lat, lon, date_depart, heure, duree)
        emoji_meteo = weathercode_to_emoji(meteo["weathercode"])

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            st.markdown(
                f"<div style='text-align: center; font-size: 110px'>{emoji_meteo}</div>",
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(ui.color_temp("Température", meteo['temp_depart']), unsafe_allow_html=True)
            st.markdown(ui.color_vent("Vitesse du vent", meteo['vent_vitesse']), unsafe_allow_html=True)

        with col3:
            st.markdown(ui.color_temp("Température Ressentie", meteo['temp_ressenti']), unsafe_allow_html=True)
            st.markdown(ui.color_rafale("Rafales", meteo['rafales']), unsafe_allow_html=True)

        with col4:
            st.markdown(ui.color_temp("Température Ressentie Max", meteo['temp_ressenti_max']), unsafe_allow_html=True)
            st.markdown(ui.no_color("Direction du vent", meteo['vent_direction']), unsafe_allow_html=True)

        with col5:
            st.markdown(ui.color_uv("Index UV", meteo['uv_index']), unsafe_allow_html=True)
            st.markdown(ui.color_pluie("Quantité de pluie", meteo['precipitation_mm']), unsafe_allow_html=True)

        with col6:
            st.markdown(ui.no_color("Taux d'Humidité", meteo['humidite'], unite="%"), unsafe_allow_html=True)
            st.markdown(ui.no_color("Probabilité de Pluie", meteo['precipitation_proba'], unite="%"), unsafe_allow_html=True)

    # --- Bloc matos — sélection via session_state, jamais via item.disponible ---
    with st.expander("Selectionne le matos dispo dans ton armoire", expanded=True):
        tout_selectionner = st.checkbox("Tout sélectionner")
        col1, col2, col3 = st.columns([1,2,1])

        with col1:
            with st.container(border=True):
                with st.container(border=True):
                    st.markdown("<h4 style='text-align: center; margin-top: -8px; margin-bottom: -2px;'>Jambes</h4>", unsafe_allow_html=True)
                for item in CATALOGUE:
                    if item.partie_du_corps == "jambes":
                        st.session_state["disponibilite"][item.nom] = st.checkbox(
                            item.nom,
                            value=True if tout_selectionner else st.session_state["disponibilite"][item.nom]
                        )
                st.write("")
                st.write("")
                st.write("")
                st.write("")
                st.write("")

        with col2:
            with st.container(border=True):
                with st.container(border=True):
                    st.markdown("<h4 style='text-align: center; margin-top: -8px; margin-bottom: -2px;'>Torse</h4>", unsafe_allow_html=True)
                col_torse1, col_torse2 = st.columns(2)
                items_torse = [item for item in CATALOGUE if item.partie_du_corps == "torse"]
                moitie = len(items_torse) // 2
            with col_torse1:
                for item in items_torse[:moitie]:
                    st.session_state["disponibilite"][item.nom] = st.checkbox(
                        item.nom,
                        value=True if tout_selectionner else st.session_state["disponibilite"][item.nom]
                    )
            with col_torse2:
                for item in items_torse[moitie:]:
                    st.session_state["disponibilite"][item.nom] = st.checkbox(
                        item.nom,
                        value=True if tout_selectionner else st.session_state["disponibilite"][item.nom]
                    )

        with col3:
            with st.container(border=True):
                with st.container(border=True):
                    st.markdown("<h4 style='text-align: center; margin-top: -8px; margin-bottom: -2px;'>Accessoires</h4>", unsafe_allow_html=True)
                for item in CATALOGUE:
                    if item.partie_du_corps == "extrémités":
                        st.session_state["disponibilite"][item.nom] = st.checkbox(
                            item.nom,
                            value=True if tout_selectionner else st.session_state["disponibilite"][item.nom]
                        )

    # Synchronisation session_state -> CATALOGUE avant appel à recommend()
    for item in CATALOGUE:
        item.disponible = st.session_state["disponibilite"][item.nom]

    # --- Bloc résultats — recommandations en 3 colonnes ---
    with st.container(border=True):
        reco = recommend(meteo, sensibilite, intensite, duree, CATALOGUE)

        col1, col2, col3 = st.columns([1,1,1])

        with col1:
            with st.container(border=True):
                with st.container(border=True):
                    st.markdown("<h4 style='text-align: center; margin-top: -8px; margin-bottom: -2px;'>Torse</h4>", unsafe_allow_html=True)
                item_vert_torse = [item for item in reco["vert"] if item.partie_du_corps == "torse"]
                item_orange_torse = [item for item in reco["orange"] if item.partie_du_corps == "torse"]
                for item in item_vert_torse:
                    st.markdown(f"<p style='padding-left: 40px;'>🟢 {item.nom}</p>", unsafe_allow_html=True)
                for item in item_orange_torse:
                    st.markdown(f"<p style='padding-left: 40px;'>🟠 {item.nom}</p>", unsafe_allow_html=True)

        with col2:
            with st.container(border=True):
                with st.container(border=True):
                    st.markdown("<h4 style='text-align: center; margin-top: -8px; margin-bottom: -2px;'>Jambes</h4>", unsafe_allow_html=True)
                item_vert_jambes = [item for item in reco["vert"] if item.partie_du_corps == "jambes"]
                item_orange_jambes = [item for item in reco["orange"] if item.partie_du_corps == "jambes"]
                for item in item_vert_jambes:
                    st.markdown(f"<p style='padding-left: 40px;'>🟢 {item.nom}</p>", unsafe_allow_html=True)
                for item in item_orange_jambes:
                    st.markdown(f"<p style='padding-left: 40px;'>🟠 {item.nom}</p>", unsafe_allow_html=True)

        with col3:
            with st.container(border=True):
                with st.container(border=True):
                    st.markdown("<h4 style='text-align: center; margin-top: -8px; margin-bottom: -2px;'>Accessoires</h4>", unsafe_allow_html=True)
                item_vert_extre = [item for item in reco["vert"] if item.partie_du_corps == "extrémités"]
                item_orange_extre = [item for item in reco["orange"] if item.partie_du_corps == "extrémités"]
                for item in item_vert_extre:
                    st.markdown(f"<p style='padding-left: 40px;'>🟢 {item.nom}</p>", unsafe_allow_html=True)
                for item in item_orange_extre:
                    st.markdown(f"<p style='padding-left: 40px;'>🟠 {item.nom}</p>", unsafe_allow_html=True)

    # --- Expander debug — catalogue complet + température effective (beta) ---
    with st.expander("Debug / Catalogue"):
        st.write(f"Température ressentie avec tes paramètres: {reco['temp_effective']:.1f} °C")
        col1, col2, col3 = st.columns([1,2,1])

        with col1:
            with st.container(border=True):
                for item in CATALOGUE:
                    if item.partie_du_corps == "jambes":
                        st.write(f"{item.nom} : {item.temp_min} °C, {item.temp_max} °C")

        with col2:
            with st.container(border=True):
                col_torse1, col_torse2 = st.columns(2)
                items_torse = [item for item in CATALOGUE if item.partie_du_corps == "torse"]
                moitie = len(items_torse) // 2
            with col_torse1:
                for item in items_torse[:moitie]:
                    st.write(f"{item.nom} : {item.temp_min} °C, {item.temp_max} °C")
            with col_torse2:
                for item in items_torse[moitie:]:
                    st.write(f"{item.nom} : {item.temp_min} °C, {item.temp_max} °C")

        with col3:
            with st.container(border=True):
                for item in CATALOGUE:
                    if item.partie_du_corps == "extrémités":
                        st.write(f"{item.nom} : {item.temp_min} °C, {item.temp_max} °C")

# --- Page d accueil — affichée tant qu aucune ville n est sélectionnée ---
else:
    _, col, _ = st.columns(3)
    with col:
        st.markdown("<h3 style='text-align: center; margin-top: 50px; margin-bottom: 10px;'>powered by Team Raclette</h3>", unsafe_allow_html=True)
        st.image("assets/logo_team_raclette_final.png", width='stretch')