import streamlit as st

st.set_page_config(
    page_title="Anticipation VLE 24 h",
    layout="centered"
)

st.title("Anticipation de dépassement VLE 24 h")

st.markdown(
    "Outil d'aide au réglage de la concentration de fonctionnement "
    "pour respecter une VLE journalière."
)

st.divider()

# -----------------------------
# VALEURS VLE 
# -----------------------------
VLE_DATABASE = {
    "CO" : 50.0,
    "COT" : 10.0,
    "NOx" : 150.0,
    "SO2" : 40.0,
    "HCl" : 8.0,
    "HF" : 1.0,
    "Poussières" : 5.0,
    "Mercure" : 20.0
}
                 

# -----------------------------
# CHOIX DU GAZ A ANTICIPER
# -----------------------------
gaz = st.selectbox(
    "Choisissez le gaz",
    list(VLE_DATABASE.keys())
)

VLE_24H = VLE_DATABASE[gaz]

st.info(f"VLE 24 h pour {gaz} : **{VLE_24H} mg/m³**")

# -----------------------------
# HEURE ACTUELLE 
# -----------------------------
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

# -----------------------------
# CONCENTRATION ACTUELLE 
# -----------------------------
C_moy_actuelle = st.number_input(
    "Concentration moyenne actuelle (mg/m³)",
    min_value=0.0,
    value=40.0,
    step=1.0
)

st.divider()

# -----------------------------
# JAUGE / RÉGLAGE UTILISATEUR
# -----------------------------
C_future = st.slider(
    "Concentration de fonctionnement jusqu'à la fin de la journée (mg/m³)",
    min_value=0.0,
    max_value=200.0,
    value=40.0,
    step=0.01
)

# -----------------------------
# CALCULS
# -----------------------------
heure_debut = 0.0
heure_fin = 24.0

t_ecoule = heure_actuelle - heure_debut
t_restant = heure_fin - heure_actuelle

if t_restant <= 0:
    st.error("La journée est terminée : aucun temps restant.")
else:
    moyenne_finale = (
        C_moy_actuelle * t_ecoule +
        C_future * t_restant
    ) / 24

    st.divider()

    st.subheader("Résultats")

    st.metric(
        label="Concentration réglée",
        value=f"{C_future:.1f} mg/m³"
    )

    st.metric(
        label="Moyenne journalière estimée (24 h)",
        value=f"{moyenne_finale:.1f} mg/m³"
    )

    taux = moyenne_finale / VLE_24H if VLE_24H > 0 else 0

    if moyenne_finale > VLE_24H:
        st.error(
            f"⚠ Dépassement de la VLE 24 h ({taux*100:.0f} %)"
        )
    elif taux >= 0.8:
        st.warning(
            f"🟠 Proche de la limite ({taux*100:.0f} % de la VLE)"
        )
    else:
        st.success(
            f"✔ Conforme ({taux*100:.0f} % de la VLE)"
        )

    # -----------------------------
    # INFO UTILE EN PLUS
    # -----------------------------
    C_max_autorisee = (
        VLE_24H * 24 - C_moy_actuelle * t_ecoule
    ) / t_restant

    st.info(
        f"Concentration maximale autorisée jusqu'à la fin de la journée : "
        f"{max(0, C_max_autorisee):.1f} mg/m³"
    )


