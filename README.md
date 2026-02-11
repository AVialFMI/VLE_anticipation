 # Présentation

Cet outil web permet d’anticiper un dépassement de Valeur Limite d’Exposition (VLE) sur 24 heures à partir de données opérationnelles en temps réel.

Il s’adresse aux :

* Exploitants
* Responsables d’exploitation
* Adjoint d'exploitation

L’objectif est de fournir un outil simple, rapide et fiable d’aide à la décision afin de maintenir la conformité réglementaire sur les VLE jours

# Utilisation
L’application permet de :

* Sélectionner une substance (VLE intégrée)
* Saisir l’heure actuelle
* Renseigner la concentration moyenne mesurée
* Ajuster la concentration de fonctionnement prévue
* Visualiser instantanément :

  * la moyenne 24 h estimée
  * le pourcentage de la VLE
  * la concentration maximale autorisée jusqu'à la fin de journée
  * le statut de conformité

# Méthodologie de calcul

La moyenne journalière est calculée selon une moyenne pondérée sur 24 heures

# Hypothèses de calcul

* Période de référence : 0h00 → 24h00
* Concentration constante sur la période restante
* Moyenne actuelle calculée uniquement sur le temps écoulé
* Absence de pondération multi-substances (outil mono-composé)

# Fonctionnalités clés

✔ Interface web accessible sans installation
✔ Sélection sécurisée de la substance (VLE pré-enregistrée)
✔ Réglage fin de la concentration (pas configurable)
✔ Indicateur visuel de conformité :

| Statut         | Signification    |
| -------------- | ---------------- |
| 🟢 Conforme    | < 80 % de la VLE |
| 🟠 Alerte      | 80–100 %         |
| 🔴 Dépassement | > 100 %          |







# VLE_anticipation
Outil d'anticipation de dépasssement de VLE
