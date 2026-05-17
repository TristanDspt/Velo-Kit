
def color_temp(label, value):
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
    color = "inherit"
    formatted = f"{value:{fmt}}" if fmt else str(value)
    return f"""
    <div style='margin-top: -5px; margin-bottom: 10px'>
        <span style='font-size: 0.9em; opacity: 0.6;'>{label}</span><br>
        <span style='font-size: 2.2em; color: {color};'>{formatted} {unite}</span>
    </div>
    """
