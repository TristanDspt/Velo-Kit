import streamlit as st
from core.gear import CATALOGUE
from core.weather import get_coordinates, get_weather, build_weather_dict
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

with st.container(border=True):

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
            label="Heure",
            help="Ton heure de départ",
            max_value=24,
            value=10
        )

with st.container(border=True):
    
    col1, col2, col3 = st.columns(3)

    with col1:
        duree = st.pills(
            label="Intensité",
            help="Court < 2h, Moyen 2h -> 4h, Long > 4h\nRetire 1° en moyen et 2° pour le long"
        )

    with col2:
        intensite = st.pills(
            label="Durée"
        )

lat = ville_select["lat"]
lon = ville_select["lon"]