import streamlit as st
from zoneinfo import ZoneInfo
from datetime import datetime


# ==========================================================
# APPLICATION : ANTICIPATION VLE 24 H
# ==========================================================
#
# OBJECTIF :
# Cette application permet de calculer la concentration maximale
# à ne pas dépasser jusqu'à la fin de la journée (24h00).
#
# Le calcul permet d'anticiper le respect d'une VLE journalière.
#
# L'utilisateur renseigne :
#   1. Le gaz concerné
#   2. Si la ligne a démarré en cours de journée
#   3. L'heure de démarrage si nécessaire
#   4. La moyenne actuelle mesurée
#
# L'application calcule ensuite :
#
#   → La concentration maximale à ne pas dépasser
#     jusqu'à 24h00.
#
# L'heure actuelle est récupérée automatiquement
# selon le fuseau horaire Europe/Paris.
#
# ==========================================================


# ----------------------------------------------------------
# CONFIGURATION DE LA PAGE
# ----------------------------------------------------------
#
# Cette fonction configure l'apparence générale
# de la page Streamlit.
#
# page_title :
#     Nom affiché dans l'onglet du navigateur.
#
# page_icon :
#     Logo utilisé comme icône de la page.
#
# layout :
#     "centered" permet de centrer l'application.
#
# ----------------------------------------------------------

st.set_page_config(
    page_title="Anticipation VLE 24 h",
    page_icon="logo.png",
    layout="centered"
)


# ----------------------------------------------------------
# EN-TÊTE DE L'APPLICATION
# ----------------------------------------------------------
#
# On crée deux colonnes :
#
#   - colonne de gauche : logo
#   - colonne de droite : titre
#
# Le ratio [1, 4] signifie que la deuxième colonne
# est environ quatre fois plus large que la première.
#
# ----------------------------------------------------------

col_logo, col_title = st.columns([1, 4])


# Affichage du logo

with col_logo:

    st.image(
        "logo.png",
        width=120
    )


# Affichage du titre

with col_title:

    st.markdown(
        "## Anticipation de dépassement VLE 24 h"
    )

    st.markdown(
        """
        <span style='font-size:14px;'>
        Application interne – FMI Process
        </span>
        """,
        unsafe_allow_html=True
    )


# Description de l'application

st.markdown(
    """
    Outil permettant de déterminer la concentration maximale
    à ne pas dépasser jusqu'à 24h00 afin de respecter
    la Valeur Limite d'Exposition (VLE).
    """
)


# Ligne de séparation visuelle

st.divider()


# ==========================================================
# BASE DE DONNÉES DES VLE
# ==========================================================
#
# Ce dictionnaire contient les VLE associées à chaque gaz.
#
# Exemple :
#
#     "CO": 50.0
#
# signifie que la VLE du CO est de 50 mg/Nm³.
#
# Pour ajouter un nouveau gaz, il suffit d'ajouter une ligne :
#
#     "Nouveau gaz": valeur
#
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


# ==========================================================
# CHOIX DU GAZ
# ==========================================================
#
# La fonction selectbox crée une liste déroulante.
#
# L'utilisateur choisit le gaz qu'il souhaite anticiper.
#
# La liste des choix est automatiquement créée à partir
# des clés du dictionnaire VLE_DATABASE.
#
# ----------------------------------------------------------

gaz = st.selectbox(

    "Choisissez le gaz à anticiper",

    list(VLE_DATABASE.keys())

)


# ----------------------------------------------------------
# RÉCUPÉRATION AUTOMATIQUE DE LA VLE
# ----------------------------------------------------------
#
# Exemple :
#
# Si l'utilisateur choisit "HCl" :
#
#     gaz = "HCl"
#
# alors :
#
#     VLE_24H = 8.0
#
# ----------------------------------------------------------

VLE_24H = VLE_DATABASE[gaz]


# Affichage de la VLE correspondante

st.info(

    f"VLE 24 h pour {gaz} : "
    f"**{VLE_24H} mg/Nm³**"

)


# ==========================================================
# RÉCUPÉRATION AUTOMATIQUE DE L'HEURE ACTUELLE
# ==========================================================
#
# L'heure actuelle est récupérée automatiquement.
#
# Il n'est pas possible de la modifier manuellement.
#
# ZoneInfo("Europe/Paris") permet d'utiliser l'heure
# française avec la gestion de l'heure d'été et d'hiver.
#
# ----------------------------------------------------------

now = datetime.now(

    ZoneInfo("Europe/Paris")

)


# Récupération de l'heure

heure = now.hour


# Récupération des minutes

minute = now.minute


# ----------------------------------------------------------
# CONVERSION DE L'HEURE EN HEURE DÉCIMALE
# ----------------------------------------------------------
#
# Exemple :
#
# 14h30 devient :
#
#     14 + 30 / 60
#
#     = 14.5 heures
#
# Cette conversion facilite les calculs de durée.
#
# ----------------------------------------------------------

heure_actuelle = (

    heure
    +
    minute / 60

)


# Affichage de l'heure actuelle

st.success(

    f"Heure actuelle : "
    f"{heure:02d}:{minute:02d}"

)


# ==========================================================
# DÉMARRAGE DE LA LIGNE
# ==========================================================
#
# L'utilisateur indique si la ligne a démarré
# en cours de journée.
#
# Exemple :
#
#   Non :
#       La ligne fonctionnait déjà à 00h00.
#       Le calcul commence donc à 00h00.
#
#   Oui :
#       La ligne a démarré à une heure précise.
#       Le calcul commence à cette heure.
#
# ----------------------------------------------------------

demarrage_journee = st.checkbox(

    "La ligne a-t-elle démarré en cours de journée ?",

    value=False

)


# ==========================================================
# CAS 1 : LA LIGNE A DÉMARRÉ EN COURS DE JOURNÉE
# ==========================================================

if demarrage_journee:


    # Information affichée à l'utilisateur

    st.info(

        "Le calcul commencera à l'heure "
        "de démarrage de la ligne."

    )


    # Création de deux colonnes :
    #
    #   Colonne 1 : heure
    #   Colonne 2 : minute

    col1, col2 = st.columns(2)


    # ------------------------------------------------------
    # SAISIE DE L'HEURE DE DÉMARRAGE
    # ------------------------------------------------------

    with col1:

        heure_demarrage = st.number_input(

            "Heure de démarrage",

            min_value=0,

            max_value=23,

            value=8,

            step=1

        )


    # ------------------------------------------------------
    # SAISIE DE LA MINUTE DE DÉMARRAGE
    # ------------------------------------------------------

    with col2:

        minute_demarrage = st.number_input(

            "Minute de démarrage",

            min_value=0,

            max_value=59,

            value=0,

            step=1

        )


    # ------------------------------------------------------
    # CONVERSION DE L'HEURE DE DÉMARRAGE
    # ------------------------------------------------------
    #
    # Exemple :
    #
    #     08h30
    #
    # devient :
    #
    #     8 + 30 / 60
    #
    #     = 8.5 heures
    #
    # ------------------------------------------------------

    heure_debut = (

        heure_demarrage
        +
        minute_demarrage / 60

    )


# ==========================================================
# CAS 2 : LA LIGNE ÉTAIT DÉJÀ EN FONCTIONNEMENT À 00H00
# ==========================================================

else:


    # Information affichée à l'utilisateur

    st.info(

        "La ligne était déjà en fonctionnement à 00:00. "
        "Le calcul commencera depuis 00:00."

    )


    # Dans ce cas, le début de la période de calcul
    # est fixé à minuit.

    heure_debut = 0.0


# ==========================================================
# VÉRIFICATION DE LA COHÉRENCE DE L'HEURE
# ==========================================================
#
# Il est impossible que la ligne ait démarré
# dans le futur.
#
# Exemple interdit :
#
#     Heure actuelle : 14h00
#     Démarrage       : 16h00
#
# ----------------------------------------------------------

if heure_debut > heure_actuelle:


    st.error(

        "L'heure de démarrage ne peut pas être "
        "postérieure à l'heure actuelle."

    )


    # Arrêt du programme

    st.stop()


# ==========================================================
# SAISIE DE LA MOYENNE ACTUELLE
# ==========================================================
#
# L'utilisateur indique la moyenne mesurée jusqu'à présent.
#
# Exemple :
#
#     Heure actuelle : 14h00
#     Moyenne actuelle : 40 mg/Nm³
#
# Cette valeur représente la concentration moyenne
# sur la période déjà écoulée.
#
# ----------------------------------------------------------

C_moy_actuelle = st.number_input(

    "Entrez la moyenne actuelle mesurée (mg/Nm³)",

    min_value=0.0,

    value=40.0,

    step=0.1

)


# ==========================================================
# CALCUL DES DURÉES
# ==========================================================
#
# Heure de fin de la journée :
#
#     24h00
#
# ----------------------------------------------------------

heure_fin = 24.0


# ----------------------------------------------------------
# TEMPS ÉCOULÉ
# ----------------------------------------------------------
#
# Le temps écoulé correspond à :
#
#     Heure actuelle - Heure de début
#
# Exemple :
#
#     Début       : 08h00
#     Maintenant  : 14h00
#
#     Temps écoulé = 14 - 8 = 6 heures
#
# ----------------------------------------------------------

t_ecoule = (

    heure_actuelle
    -
    heure_debut

)


# ----------------------------------------------------------
# TEMPS RESTANT
# ----------------------------------------------------------
#
# Le temps restant correspond à :
#
#     24h00 - Heure actuelle
#
# Exemple :
#
#     Heure actuelle : 14h00
#
#     Temps restant = 24 - 14 = 10 heures
#
# ----------------------------------------------------------

t_restant = (

    heure_fin
    -
    heure_actuelle

)


# ----------------------------------------------------------
# DURÉE TOTALE DE LA PÉRIODE
# ----------------------------------------------------------
#
# Exemple avec un démarrage à 08h00 :
#
#     Temps écoulé : 6 heures
#     Temps restant : 10 heures
#
#     Durée totale = 6 + 10
#                   = 16 heures
#
# ----------------------------------------------------------

duree_totale = (

    t_ecoule
    +
    t_restant

)


# ==========================================================
# CALCUL DE LA CONCENTRATION MAXIMALE À NE PAS DÉPASSER
# ==========================================================
#
# Objectif :
#
# Déterminer la concentration maximale qui peut être
# maintenue pendant le temps restant sans dépasser la VLE.
#
# Formule :
#
# C_max =
#
#     (VLE × durée totale
#      - moyenne actuelle × temps écoulé)
#
#     / temps restant
#
# ----------------------------------------------------------

if t_restant <= 0:


    # Si l'heure actuelle est 24h00 ou plus,
    # il n'y a plus de temps pour agir.

    st.error(

        "La journée est terminée : "
        "aucun temps restant."

    )


else:


    # ------------------------------------------------------
    # CALCUL DE LA CONCENTRATION MAXIMALE
    # ------------------------------------------------------

    C_max_autorisee = (

        (

            VLE_24H
            *
            duree_totale

        )

        -

        (

            C_moy_actuelle
            *
            t_ecoule

        )

    )

    /

    t_restant


    # ======================================================
    # AFFICHAGE DE LA PÉRIODE DE CALCUL
    # ======================================================

    st.divider()


    st.subheader(

        "Période prise en compte"

    )


    # Création de trois colonnes

    col1, col2, col3 = st.columns(3)


    # ------------------------------------------------------
    # AFFICHAGE DE L'HEURE DE DÉBUT
    # ------------------------------------------------------

    with col1:


        # Conversion de l'heure décimale
        # vers un affichage HH:MM

        heures_debut = int(

            heure_debut

        )


        minutes_debut = int(

            (heure_debut % 1) * 60

        )


        st.metric(

            "Début du calcul",

            f"{heures_debut:02d}:"
            f"{minutes_debut:02d}"

        )


    # ------------------------------------------------------
    # AFFICHAGE DU TEMPS ÉCOULÉ
    # ------------------------------------------------------

    with col2:


        st.metric(

            "Temps écoulé",

            f"{t_ecoule:.2f} h"

        )


    # ------------------------------------------------------
    # AFFICHAGE DU TEMPS RESTANT
    # ------------------------------------------------------

    with col3:


        st.metric(

            "Temps restant",

            f"{t_restant:.2f} h"

        )


    # ======================================================
    # AFFICHAGE DU RÉSULTAT PRINCIPAL
    # ======================================================

    st.divider()


    st.subheader(

        "Résultat"

    )


    # ------------------------------------------------------
    # CAS 1 : DÉPASSEMENT DÉJÀ INÉVITABLE
    # ------------------------------------------------------
    #
    # Si la concentration maximale calculée est négative
    # ou égale à zéro, cela signifie que la VLE est déjà
    # dépassée ou qu'il n'est plus possible de respecter
    # la limite avec le temps restant.
    #
    # ------------------------------------------------------

    if C_max_autorisee <= 0:


        st.error(

            "⚠️ Dépassement déjà inévitable "
            "sur la journée."

        )


    # ------------------------------------------------------
    # CAS 2 : UNE CONCENTRATION MAXIMALE EST POSSIBLE
    # ------------------------------------------------------

    else:


        # Affichage du résultat dans un cadre visible

        st.markdown(

            f"""

            <div style="
                background-color:#E8F4FD;
                color:#FF0000;
                padding:20px;
                border-radius:10px;
                font-size:26px;
                font-weight:bold;
                text-align:center;
            ">

            CONCENTRATION À NE PAS DÉPASSER

            <br><br>

            {C_max_autorisee:.2f} mg/Nm³

            <br><br>

            jusqu'à 24h00

            </div>

            """,

            unsafe_allow_html=True

        )
