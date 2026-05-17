"""Fonctions HTML de mise en forme conditionnelle des métriques météo.

Chaque fonction retourne un bloc HTML <div> prêt à être passé à st.markdown(unsafe_allow_html=True).
La couleur du texte change selon des seuils propres à chaque métrique.
"""


def color_temp(label, value):
    """Retourne un bloc HTML avec la température colorée selon l'intensité du froid/chaud.

    Args:
        label: Libellé affiché au-dessus de la valeur.
        value: Température en °C (float).

    Returns:
        Chaîne HTML à passer à st.markdown(unsafe_allow_html=True).
    """
    if value < 8:
        color = "#4a9eff"
    elif value < 25:
        color = "inherit"
    elif value < 30:
        color = "#ff8c00"
    else:
        color = "#ff4444"
    
    return f"""
    <div style='margin-top: -5px; margin-bottom: 10px'>
        <span style='font-size: 0.9em; opacity: 0.6;'>{label}</span><br>
        <span style='font-size: 2.2em; color: {color};'>{value:.1f} °C</span>
    </div>
    """

def color_vent(label, value):
    """Retourne un bloc HTML avec la vitesse du vent colorée selon l'intensité.

    Args:
        label: Libellé affiché au-dessus de la valeur.
        value: Vitesse du vent en km/h (float).

    Returns:
        Chaîne HTML à passer à st.markdown(unsafe_allow_html=True).
    """
    if value < 20:
        color = "inherit"
    elif value < 30:
        color = "#ffb300"
    elif value < 40:
        color = "#ff8c00"
    else:
        color = "#ff4444"
    
    return f"""
    <div style='margin-top: -5px; margin-bottom: 10px'>
        <span style='font-size: 0.9em; opacity: 0.6;'>{label}</span><br>
        <span style='font-size: 2.2em; color: {color};'>{value:.0f} km/h</span>
    </div>
    """

def color_rafale(label, value):
    """Retourne un bloc HTML avec la vitesse des rafales colorée selon l'intensité.

    Args:
        label: Libellé affiché au-dessus de la valeur.
        value: Vitesse des rafales en km/h (float).

    Returns:
        Chaîne HTML à passer à st.markdown(unsafe_allow_html=True).
    """
    if value < 30:
        color = "inherit"
    elif value < 40:
        color = "#ffb300"
    elif value < 50:
        color = "#ff8c00"
    else:
        color = "#ff4444"
    
    return f"""
    <div style='margin-top: -5px; margin-bottom: 10px'>
        <span style='font-size: 0.9em; opacity: 0.6;'>{label}</span><br>
        <span style='font-size: 2.2em; color: {color};'>{value:.0f} km/h</span>
    </div>
    """

def color_uv(label, value):
    """Retourne un bloc HTML avec l'index UV coloré selon le niveau d'exposition.

    Args:
        label: Libellé affiché au-dessus de la valeur.
        value: Index UV (float).

    Returns:
        Chaîne HTML à passer à st.markdown(unsafe_allow_html=True).
    """
    if value < 7:
        color = "inherit"
    elif value < 8:
        color = "#ff8c00"
    else:
        color = "#ff4444"
    
    return f"""
    <div style='margin-top: -5px; margin-bottom: 10px'>
        <span style='font-size: 0.9em; opacity: 0.6;'>{label}</span><br>
        <span style='font-size: 2.2em; color: {color};'>{value:.1f}</span>
    </div>
    """

def color_pluie(label, value):
    """Retourne un bloc HTML avec le cumul de pluie coloré selon la quantité.

    Args:
        label: Libellé affiché au-dessus de la valeur.
        value: Cumul de précipitations en mm (float).

    Returns:
        Chaîne HTML à passer à st.markdown(unsafe_allow_html=True).
    """
    if value < 1.5:
        color = "inherit"
    elif value < 3:
        color = "#ffb300"
    elif value < 5:
        color = "#ff8c00"
    else:
        color = "#ff4444"
    
    return f"""
    <div style='margin-top: -5px; margin-bottom: 10px'>
        <span style='font-size: 0.9em; opacity: 0.6;' title="Cumul sur la durée de la sortie">{label}</span><br>
        <span style='font-size: 2.2em; color: {color};'>{value:.1f} mm</span>
    </div>
    """

def no_color(label, value, fmt=None, unite=""):
    """Retourne un bloc HTML sans mise en forme conditionnelle (couleur neutre).

    Args:
        label: Libellé affiché au-dessus de la valeur.
        value: Valeur à afficher (str, int ou float).
        fmt: Format optionnel à appliquer à la valeur (ex: ".1f"). Ignoré si None.
        unite: Unité affichée après la valeur (ex: "%"). Vide par défaut.

    Returns:
        Chaîne HTML à passer à st.markdown(unsafe_allow_html=True).
    """
    color = "inherit"
    formatted = f"{value:{fmt}}" if fmt else str(value)
    return f"""
    <div style='margin-top: -5px; margin-bottom: 10px'>
        <span style='font-size: 0.9em; opacity: 0.6;'>{label}</span><br>
        <span style='font-size: 2.2em; color: {color};'>{formatted} {unite}</span>
    </div>
    """
