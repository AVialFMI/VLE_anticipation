import streamlit as st

from datetime import datetime
from zoneinfo import ZoneInfo


# ==========================================================
# APPLICATION : ANTICIPATION VLE 24 H
# ==========================================================
#
# Auteur : AV (FMI Process)
# Date : 10/02/2025
#
# OBJECTIF
# --------
# Cette application permet de déterminer la concentration
# maximale à ne pas dépasser jusqu'à 24h00 afin de respecter
# une Valeur Limite d'Exposition (VLE).
#
#
# FONCTIONNEMENT
# --------------
# L'utilisateur renseigne :
#
# 1. Le gaz concerné.
#
# 2. Si la ligne a démarré en cours de journée.
#
# 3. L'heure de démarrage si nécessaire.
#
# 4. La moyenne actuelle mesurée.
#
#
# L'application calcule ensuite :
#
#     La concentration maximale à ne pas dépasser
#     jusqu'à la fin de la journée.
#
#
# L'heure actuelle est récupérée automatiquement avec le
# fuseau horaire Europe/Paris.
#
# ==========================================================


# ==========================================================
# CONFIGURATION DE LA PAGE
# ==========================================================
#
# Cette fonction configure l'apparence générale de la page.
#
# page_title :
#     Titre affiché dans l'onglet du navigateur.
#
# page_icon :
#     Icône de l'application.
#
# layout :
#     "centered" centre l'application sur la page.
#
# ==========================================================

st.set_page_config(
    page_title="Anticipation VLE 24 h",
    page_icon="logo.png",
    layout="centered",
)


# ==========================================================
# EN-TÊTE DE L'APPLICATION
# ==========================================================
#
# Création de deux colonnes :
#
#     Colonne 1 : logo
#     Colonne 2 : titre et description
#
# Le ratio [1, 4] donne plus de largeur au titre.
#
# ==========================================================

col_logo, col_title = st.columns([1, 4])


with col_logo:
    st.image(
        "logo.png",
        width=120,
    )


with col_title:
    st.markdown(
        "## Anticipation de dépassement VLE 24 h"
    )

    st.markdown(
        """
        <span style="font-size:14px;">
        Application interne – FMI Process
        </span>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    Outil permettant de déterminer la concentration maximale
    à ne pas dépasser jusqu'à minuit afin de respecter une
    Valeur Limite d'Emission Journalière (VLEJ).
    """
)


st.divider()


# ==========================================================
# BASE DE DONNÉES DES VLE
# ==========================================================
#
# Le dictionnaire ci-dessous contient les VLE associées
# aux différents gaz.
#
# Exemple :
#
#     "CO": 50.0
#
# signifie que la VLE du CO est de 50 mg/Nm³.
#
# Pour ajouter un nouveau gaz :
#
#     "Nouveau gaz": valeur,
#
# ==========================================================

VLE_DATABASE = {
    "CO": 50.0,
    "COT": 10.0,
    "NOx": 150.0,
    "SO2": 40.0,
    "HCl": 8.0,
    "HF": 1.0,
    "Poussières": 5.0,
    "Mercure": 20.0,
}


# ==========================================================
# SÉLECTION DU GAZ
# ==========================================================
#
# Création d'une liste déroulante.
#
# L'utilisateur sélectionne le gaz qu'il souhaite anticiper.
#
# ==========================================================

gaz = st.selectbox(
    "Choisissez le gaz à anticiper",
    list(VLE_DATABASE.keys()),
)


# ==========================================================
# RÉCUPÉRATION DE LA VLE
# ==========================================================
#
# Le programme récupère automatiquement la VLE correspondant
# au gaz sélectionné.
#
# Exemple :
#
#     gaz = "HCl"
#
# alors :
#
#     VLE_24H = 8.0
#
# ==========================================================

VLE_24H = VLE_DATABASE[gaz]


st.info(
    f"VLE 24 h pour {gaz} : "
    f"**{VLE_24H} mg/Nm³**"
)


# ==========================================================
# RÉCUPÉRATION DE L'HEURE ACTUELLE
# ==========================================================
#
# L'heure est récupérée automatiquement.
#
# L'utilisateur ne peut pas la modifier.
#
# ZoneInfo("Europe/Paris") permet d'utiliser l'heure
# française avec la gestion de l'heure d'été et d'hiver.
#
# ==========================================================

now = datetime.now(
    ZoneInfo("Europe/Paris")
)


# Récupération de l'heure actuelle.

heure = now.hour


# Récupération des minutes actuelles.

minute = now.minute


# ==========================================================
# CONVERSION DE L'HEURE EN HEURE DÉCIMALE
# ==========================================================
#
# Les calculs de durée sont plus simples avec une heure
# décimale.
#
# Exemple :
#
#     14h30
#
# devient :
#
#     14 + 30 / 60 = 14.5 heures
#
# ==========================================================

heure_actuelle = heure + minute / 60


st.success(
    f"Heure actuelle : {heure:02d}:{minute:02d}"
)


# ==========================================================
# DÉTERMINATION DU DÉBUT DE LA PÉRIODE DE CALCUL
# ==========================================================
#
# L'utilisateur indique si la ligne a démarré en cours
# de journée.
#
# Deux situations sont possibles.
#
#
# CAS 1
# -----
# La ligne n'a pas démarré en cours de journée.
#
# Le calcul commence à :
#
#     00h00
#
#
# CAS 2
# -----
# La ligne a démarré en cours de journée.
#
# Le calcul commence à l'heure de démarrage saisie.
#
# ==========================================================

demarrage_journee = st.checkbox(
    "La ligne a-t-elle démarré en cours de journée ?",
    value=False,
)


# ==========================================================
# CAS 1 : DÉMARRAGE EN COURS DE JOURNÉE
# ==========================================================

if demarrage_journee:

    st.info(
        "Le calcul commencera à l'heure de démarrage "
        "de la ligne."
    )


    # ------------------------------------------------------
    # SAISIE DE L'HEURE DE DÉMARRAGE
    # ------------------------------------------------------
    #
    # Deux champs sont utilisés :
    #
    #     Heure
    #     Minute
    #
    # Exemple :
    #
    #     08h30
    #
    # ------------------------------------------------------

    col_heure, col_minute = st.columns(2)


    with col_heure:

        heure_demarrage = st.number_input(
            "Heure de démarrage",
            min_value=0,
            max_value=23,
            value=8,
            step=1,
        )


    with col_minute:

        minute_demarrage = st.number_input(
            "Minute de démarrage",
            min_value=0,
            max_value=59,
            value=0,
            step=1,
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
    #     8 + 30 / 60 = 8.5 heures
    #
    # ------------------------------------------------------

    heure_debut = (
        heure_demarrage
        + minute_demarrage / 60
    )


# ==========================================================
# CAS 2 : LA LIGNE FONCTIONNAIT DÉJÀ À 00H00
# ==========================================================

else:

    st.info(
        "La ligne était déjà en fonctionnement à 00h00. "
        "Le calcul commencera depuis 00h00."
    )


    # Le début de la période de calcul est fixé à minuit.

    heure_debut = 0.0


# ==========================================================
# VÉRIFICATION DE L'HEURE DE DÉMARRAGE
# ==========================================================
#
# L'heure de démarrage ne peut pas être dans le futur.
#
# Exemple interdit :
#
#     Heure actuelle : 14h00
#     Démarrage       : 16h00
#
# ==========================================================

if heure_debut > heure_actuelle:

    st.error(
        "L'heure de démarrage ne peut pas être "
        "postérieure à l'heure actuelle."
    )


    # Arrêt du programme.

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
# ==========================================================

C_moy_actuelle = st.number_input(
    "Entrez la moyenne actuelle mesurée (mg/Nm³)",
    min_value=0.0,
    value=40.0,
    step=0.1,
)


st.divider()


# ==========================================================
# CALCUL DES DURÉES
# ==========================================================
#
# La journée se termine à 24h00.
#
# ==========================================================

heure_fin = 24.0


# ----------------------------------------------------------
# TEMPS ÉCOULÉ
# ----------------------------------------------------------
#
# Formule :
#
#     Temps écoulé =
#     Heure actuelle - Heure de début
#
# Exemple :
#
#     Début : 08h00
#     Maintenant : 14h00
#
#     Temps écoulé = 14 - 8
#                   = 6 heures
#
# ----------------------------------------------------------

t_ecoule = heure_actuelle - heure_debut


# ----------------------------------------------------------
# TEMPS RESTANT
# ----------------------------------------------------------
#
# Formule :
#
#     Temps restant =
#     24 - Heure actuelle
#
# Exemple :
#
#     Heure actuelle : 14h00
#
#     Temps restant = 24 - 14
#                    = 10 heures
#
# ----------------------------------------------------------

t_restant = heure_fin - heure_actuelle


# ----------------------------------------------------------
# DURÉE TOTALE DE LA PÉRIODE
# ----------------------------------------------------------
#
# La période totale correspond à :
#
#     Temps écoulé + Temps restant
#
# Exemple :
#
#     Début : 08h00
#     Heure actuelle : 14h00
#
#     Temps écoulé : 6 h
#     Temps restant : 10 h
#
#     Durée totale : 16 h
#
# ----------------------------------------------------------

duree_totale = t_ecoule + t_restant


# ==========================================================
# VÉRIFICATION DU TEMPS RESTANT
# ==========================================================
#
# Si la journée est terminée, il n'est plus possible
# d'effectuer un ajustement jusqu'à 24h00.
#
# ==========================================================

if t_restant <= 0:

    st.error(
        "La journée est terminée : "
        "aucun temps restant."
    )

    st.stop()


# ==========================================================
# CALCUL DE LA CONCENTRATION MAXIMALE AUTORISÉE
# ==========================================================
#
# Le programme cherche la concentration maximale que l'on
# peut maintenir pendant le temps restant sans dépasser
# la VLE en fin de période.
#
# Formule :
#
#     C_max =
#
#     (
#         VLE × durée totale
#         - moyenne actuelle × temps écoulé
#     )
#
#     / temps restant
#
# ==========================================================

C_max_autorisee = (
    VLE_24H * duree_totale
    - C_moy_actuelle * t_ecoule
) / t_restant


# ==========================================================
# AFFICHAGE DE LA PÉRIODE DE CALCUL
# ==========================================================

st.subheader(
    "Période prise en compte"
)


# Création de trois colonnes pour afficher
# les informations principales.

col_debut, col_ecoule, col_restant = st.columns(3)


# ----------------------------------------------------------
# AFFICHAGE DE L'HEURE DE DÉBUT
# ----------------------------------------------------------

with col_debut:

    heures_debut = int(heure_debut)

    minutes_debut = int(
        (heure_debut % 1) * 60
    )

    st.metric(
        "Début du calcul",
        f"{heures_debut:02d}:{minutes_debut:02d}",
    )


# ----------------------------------------------------------
# AFFICHAGE DU TEMPS ÉCOULÉ
# ----------------------------------------------------------

with col_ecoule:

    st.metric(
        "Temps écoulé",
        f"{t_ecoule:.2f} h",
    )


# ----------------------------------------------------------
# AFFICHAGE DU TEMPS RESTANT
# ----------------------------------------------------------

with col_restant:

    st.metric(
        "Temps restant",
        f"{t_restant:.2f} h",
    )


st.divider()


# ==========================================================
# AFFICHAGE DU RÉSULTAT
# ==========================================================

st.subheader(
    "Résultat"
)


# ==========================================================
# CAS 1 : DÉPASSEMENT DÉJÀ INÉVITABLE
# ==========================================================
#
# Si la concentration maximale calculée est inférieure
# ou égale à zéro, la VLE ne peut plus être respectée
# avec les données saisies.
#
# ==========================================================

if C_max_autorisee <= 0:

    st.error(
        "⚠️ Dépassement déjà inévitable "
        "sur la journée."
    )


# ==========================================================
# CAS 2 : CONCENTRATION MAXIMALE DISPONIBLE
# ==========================================================

else:

    st.markdown(
        f"""
        <div style="
            background-color: #E8F4FD;
            color: #FF0000;
            padding: 20px;
            border-radius: 10px;
            font-size: 26px;
            font-weight: bold;
            text-align: center;
        ">

        CONCENTRATION À NE PAS DÉPASSER POUR RESPECT VLE JOUR
        <br><br>
        {C_max_autorisee:.2f} mg/Nm³
        <br><br>
        jusqu'à minuit
        </div>
        """,
        unsafe_allow_html=True,
    )
