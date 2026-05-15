import streamlit as st
from core.gear import CATALOGUE
from core.weather import get_coordinates, get_meteo, weathercode_to_emoji
from core.recommender import recommend
from datetime import date, timedelta

st.set_page_config(page_title="VeloKit", page_icon="🚴", layout="wide")

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

# Titre Principal Centré
st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>🚴 Velo Kit 🚴</h1>", unsafe_allow_html=True)

# Explications
with st.expander("Comment ça marche ❓"):
    st.markdown("""
        Renseigne ta ville, la date et l'heure de départ — l'app récupère automatiquement 
        la météo. Coche ensuite le matos que t'as dans ton armoire, 
        règle ton profil thermique, ton intensité prévue et la durée de ta sortie.

        VeloKit te sort une liste d'équipements classés en :  
        🟢 La tenue de base pour cette sortie  
        🟠 Optionnel — selon ta sensibilité

        Les recommandations s'adaptent à la température ressentie, pas juste à la température réelle.
    """)

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
            help="Date de ta sortie",
            min_value=date.today(),
            max_value=date.today() + timedelta(days=7),
            value=date.today() + timedelta(days=1),
        )

    with col4:
        heure = st.slider(
            label="Heure de départ",
            max_value=24,
            value=10
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
            help="Durée de ta sortie",
            max_value=8,
            value=2
        )

    with col7:
        sensibilite = st.pills(
            label="Sensibilitée",
            help="Frileux ou chaudière ? Ajuste selon ton ressenti habituel sur le vélo",
            options=["🥶🥶", "🥶", "😎", "🔥", "🔥🔥"],
            default="😎"
        )


if ville_select:
    lat = ville_select["lat"]
    lon = ville_select["lon"]

    with st.container(border=True):
        meteo = get_meteo(lat, lon, date_depart, heure, duree)
        emoji_meteo = weathercode_to_emoji(meteo["weathercode"])
        
        _, col1, col2, col3, col4, col5 = st.columns([0.2,2,2,2,2,2])

        with col1:
            st.markdown(
                f"<div style='text-align: center; font-size: 120px'>{emoji_meteo}</div>",
                unsafe_allow_html=True
            )
        
        with col2:
            st.metric(
                label="Température",
                value=f"{meteo["temp_depart"]:.1f} °C"
            )
            st.metric(
                label="Vitesse du vent",
                value=f"{meteo["vent_vitesse"]:.0f} km/h"
            )

        with col3:
            st.metric(
                label="Température Ressentie",
                value=f"{meteo["temp_ressenti"]:.1f} °C"
            )
            st.metric(
                label="Direction du vent",
                value=meteo["vent_direction"]
            )

        with col4:
            st.metric(
                label="Température Ressentie Max",
                value=f"{meteo["temp_ressenti_max"]:.1f} °C"
            )
            st.metric(
                label="Taux d'Humidité",
                value=f"{meteo["humidite"]} %"
            )
        
        with col5:
            st.metric(
                label="Index UV",
                value=meteo["uv_index"]
            )
            st.metric(
                label="Probabilité de Pluie",
                value=f"{meteo["precipitation_proba"]} %"
            )


    with st.expander("Selectionne le matos dispo dans ton armoire", expanded=True):

        col1, col2, col3= st.columns([1,2,1])

        with col1:
            with st.container(border=True):
                with st.container(border=True):
                    st.markdown("<h4 style='text-align: center; margin-top: -8px; margin-bottom: -2px;'>Jambes</h4>", unsafe_allow_html=True)
                for item in CATALOGUE:
                    if item.partie_du_corps == "jambes":
                        item.disponible = st.checkbox(item.nom, value=item.disponible)
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
                    item.disponible = st.checkbox(item.nom, value=item.disponible)
            with col_torse2:
                for item in items_torse[moitie:]:
                    item.disponible = st.checkbox(item.nom, value=item.disponible)

        with col3:
            with st.container(border=True):
                with st.container(border=True):
                    st.markdown("<h4 style='text-align: center; margin-top: -8px; margin-bottom: -2px;'>Accessoires</h4>", unsafe_allow_html=True)
                for item in CATALOGUE:
                    if item.partie_du_corps == "extrémités":
                        item.disponible = st.checkbox(item.nom, value=item.disponible)


    with st.container(border=True):
        reco = recommend(meteo["temp_ressenti"], sensibilite, intensite, duree, CATALOGUE)

        col1, col2, col3= st.columns([1,1,1])
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