import streamlit as st
from datetime import datetime 

# ==========================================================
# APPLICATION : ANTICIPATION VLE 24H
# Auteur : AV (FMI Process)
# Date : 10/02/2025
#
# OBJECTIF :
# Permettre aux exploitants d’anticiper un dépassement
# de Valeur Limite d’Exposition (VLE) journalière
# en ajustant la concentration de fonctionnement
# jusqu’à la fin de la journée.
#
# UTILISATION :
# Outil destiné aux sites d’incinération.
# Applicable aux gaz réglementés.
# Développé avec Streamlit pour mise à disposition web
# via GitHub / Streamlit Cloud.
# ==========================================================


# ----------------------------------------------------------
# CONFIGURATION DE LA PAGE
# ----------------------------------------------------------
st.set_page_config(
    page_title="Anticipation VLE 24 h",
    page_icon="logo.png",
    layout="centered"
)

# ----------------------------------------------------------
# EN-TÊTE AVEC LOGO EN HAUT À GAUCHE
# ----------------------------------------------------------
col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.image("logo.png", width=120)

with col_title:
    st.markdown("## Anticipation de dépassement VLE 24 h")
    st.markdown(
        "<span style='font-size:14px;'>Application interne – FMI Process</span>",
        unsafe_allow_html=True
    )

st.markdown(
    """
    Outil d'aide au réglage de la concentration de fonctionnement
    afin de respecter une Valeur Limite d'Exposition (VLE) journalière.
    """
)

st.divider()


# ----------------------------------------------------------
# BASE DE DONNÉES DES VLE (mg/m³)
# ----------------------------------------------------------
# Dictionnaire contenant les VLE 24h réglementaires.
# Ces valeurs peuvent être mises à jour selon évolution
# réglementaire (Code du Travail, arrêtés ICPE, etc.).
# ----------------------------------------------------------

VLE_DATABASE = {
    "CO": 50.0,
    "COT": 10.0,
    "NOx": 150.0,
    "SO2": 40.0,
    "HCl": 8.0,
    "HF": 1.0,
    "Poussières": 5.0,
    "Mercure": 20.0
}


# ----------------------------------------------------------
# SÉLECTION DU GAZ
# ----------------------------------------------------------
gaz = st.selectbox(
    "Choisissez le gaz à anticiper",
    list(VLE_DATABASE.keys())
)

# Récupération automatique de la VLE associée
VLE_24H = VLE_DATABASE[gaz]

st.info(f"VLE 24 h pour {gaz} : **{VLE_24H} mg/Nm³**")


# ----------------------------------------------------------
# SAISIE DE L'HEURE ACTUELLE
# ----------------------------------------------------------
# L’heure est saisie en format HH / MM
# puis convertie en heure décimale pour les calculs.
# ----------------------------------------------------------

choix = st.radio(
    "Choisir l'heure :",
    ["Heure actuelle", "Régler manuellement"]
)

if choix == "Heure actuelle":
    now = datetime.now(ZoneInfo("Paris"))
    heure = now.hour
    minute = now.minute
    st.success(f"Heure sélectionnée : {heure:02d}:{minute:02d}")

else:
    col1, col2 = st.columns(2)

    with col1:
        heure = st.number_input(
            "Heure",
            min_value=0,
            max_value=23,
            value=14,
            step=1
        )

    with col2:
        minute = st.number_input(
            "Minute",
            min_value=0,
            max_value=59,
            value=0,
            step=1
        )

# Conversion en heure décimale
heure_actuelle = heure + minute / 60


# ----------------------------------------------------------
# SAISIE DE LA MOYENNE ACTUELLE
# ----------------------------------------------------------
# Concentration moyenne mesurée depuis 0h00
# jusqu'à l'heure actuelle.
# ----------------------------------------------------------

C_moy_actuelle = st.number_input(
    "Entrez la moyenne journalière actuelle (mg/Nm³)",
    min_value=0.0,
    value=40.0,
    step=0.1
)

st.divider()


# ----------------------------------------------------------
# Entrée de la concentration à l'instant t ou simulation d'une concentration
# ----------------------------------------------------------
# Permet à l’exploitant de simuler la concentration
# de fonctionnement jusqu’à 24h00.
# Réglage fin à 0.01 mg/m³.
# ----------------------------------------------------------

# --- Définir une valeur par défaut dans session_state si nécessaire ---
if "C_future" not in st.session_state:
    st.session_state.C_future = 40.0

# --- Fonction de mise à jour ---
def update_slider():
    st.session_state.C_future_slider = st.session_state.C_future_input

def update_input():
    st.session_state.C_future_input = st.session_state.C_future_slider

col1, col2 = st.columns(2)

with col1:
    # --- Input numérique ---
    C_future_input = st.number_input(
        "Entrer la concentration actuelle (mg/Nm³)",
        min_value=0.0,
        max_value=300.0,
        value=st.session_state.C_future,
        step=0.01,
        key="C_future_input",
        on_change=update_slider
    )

with col2:
    # --- Slider ---
    C_future_slider = st.slider(
        "Ou ajuster la concentration via jauge (mg/Nm³)",
        min_value=0.0,
        max_value=300.0,
        value=st.session_state.C_future,
        step=0.01,
        key="C_future_slider",
        on_change=update_input
    )

# --- Valeur finale utilisée dans les calculs ---
C_future = st.session_state.C_future_input

# ----------------------------------------------------------
# CALCULS
# ----------------------------------------------------------
heure_debut = 0.0
heure_fin = 24.0

t_ecoule = heure_actuelle - heure_debut
t_restant = heure_fin - heure_actuelle


# ----------------------------------------------------------
# GESTION CAS LIMITE : FIN DE JOURNÉE
# ----------------------------------------------------------
if t_restant <= 0:
    st.error("La journée est terminée : aucun temps restant pour ajustement.")
else:

    # ------------------------------------------------------
    # CALCUL MOYENNE 24H ESTIMÉE
    # Formule :
    # (C_moy * t_ecoulé + C_future * t_restant) / 24
    # ------------------------------------------------------
    moyenne_finale = (
        C_moy_actuelle * t_ecoule +
        C_future * t_restant
    ) / 24

    st.divider()
    st.subheader("Résultats")

    st.metric(
        label="Concentration actuelle",
        value=f"{C_future:.2f} mg/m³"
    )

    st.metric(
        label="Moyenne journalière estimée (24 h)",
        value=f"{moyenne_finale:.2f} mg/Nm³"
    )

    # ------------------------------------------------------
    # ÉVALUATION DU TAUX PAR RAPPORT À LA VLE
    # ------------------------------------------------------
    taux = moyenne_finale / VLE_24H if VLE_24H > 0 else 0

    if moyenne_finale > VLE_24H:
        st.error(f"🔴 Dépassement de la VLE ({taux*100:.0f} %)")
    elif taux >= 0.8:
        st.warning(f"🟠 Proche de la limite ({taux*100:.0f} % de la VLE)")
    else:
        st.success(f"🟢 Conforme ({taux*100:.0f} % de la VLE)")

    # ------------------------------------------------------
    # CALCUL DE LA CONCENTRATION MAXIMALE AUTORISÉE
    # ------------------------------------------------------
    C_max_autorisee = (
        (VLE_24H * 24) - (C_moy_actuelle * t_ecoule)
    ) / t_restant

    # Gestion cas dépassement déjà inévitable
    if C_max_autorisee <= 0:
        st.error("Dépassement déjà inévitable sur la journée.")
    else:
        st.markdown(
    f"""
    <div style="
        background-color:#E8F4FD;
        color:#FF0000;
        padding:15px;
        border-radius:10px;
        font-size:22px;
        font-weight:bold;
        text-align:center;
    ">
    Concentration maximale autorisée jusqu'à 24h00 : 
    {C_max_autorisee:.2f} mg/Nm³
    </div>
    """,
    unsafe_allow_html=True
    )




