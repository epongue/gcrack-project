markdown

# Aperçu du Projet

Dans ce dossier sont répertoriées toutes les données et les codes qui ont été utilisés dans la deuxième partie du rapport.

## Arborescence du Dossier

├── E2_s=0/

├── R2_beta_nonzerocoefs.py

├── README.md

├── RP_Lasso_parameters_KII.py

├── RP_Lasso_parameters_T2.py

├── T_KII_dW_tan-alpha2.py

├── tracé_KII_T.py

├── run_concave.py

├── run_convexe.py

├── run_droit.py

└── ResultsRegression/


### Fichiers de Données

- **E2_s=0/** : Dossier contenant les fichiers CSV avec les données de KI (facteur d'intensité de contrainte en mode I), KII (mode II) et T (contrainte T) pour différents angles et rayons, utilisées comme entrées pour les scripts d'analyse.
- **ResultsRegression/** : Ce dossier sera créé lors du lancement des scripts `RP_Lasso_parameters_KII.py` et `RP_Lasso_parameters_T2.py` pour stocker les coefficients des différents modèles ainsi que les métriques \(R^2\) et RRMSE pour chaque valeur de beta.

### Scripts Python

- **tracé_KII_T.py** : Génère un nuage de points représentant la relation entre KII adimensionnalisé et la contrainte T adimensionnée pour divers angles et rayons. Les points sont colorés selon l'angle, avec des marqueurs distincts pour les rayons, et une courbe pour la solution en milieu infini. Les points où KI < 0 sont mis en évidence avec des marqueurs creux noirs (à décommenter pour visualiser). C'est ce script qui nous permet d'obtenir la figure 6.1 dans la deuxième partie du rapport.

- **R2_beta_nonzerocoefs.py** : Évalue les performances d'un modèle de régression Lasso pour KII (ou T) en traçant le score \(R^2\) et le nombre de coefficients non nuls en fonction du paramètre de régularisation (beta), sur une échelle logarithmique. C'est ce code qui a permis de générer les figures 7.3 et 7.4 dans le rapport.

- **RP_Lasso_KII.py** : Effectue une régression polynomiale avec régularisation Lasso pour modéliser \(\hat{K}_{II}\) en fonction de l'angle et du rayon avec un polynôme de degré choisi. Les données sont transformées en caractéristiques polynomiales, standardisées, et les performances du modèle (R², RRMSE) sont évaluées pour différentes valeurs de beta. Les coefficients sont enregistrés dans des fichiers CSV. Dans le code, il y a un petit script (à décommenter) qui permet de vérifier l'overfitting du modèle pour la meilleure pénalisation beta choisie (figure 7.7 et 7.8 dans le rapport).

- **RP_Lasso_T.py** : Similaire à `RP_Lasso_parameters_KII.py`, mais modélise la contrainte \(\hat{T}\) (au lieu de \(\hat{K}_{II}\)).

- **T_KII_dW_tan-alpha.py** : Visualise en 3D les valeurs de T et KII adimensionnées obtenues par les simulations en fonction de \(\Delta W\) et de fonctions trigonométriques (\(\tan(\alpha)\) pour T, \(\sin(\alpha)\) pour KII). Les points où KI < 0 sont représentés par des marqueurs creux noirs (à décommenter).

- **T_KII_dW_tan-alpha2.py** : Visualise en 3D la superposition des valeurs de T et KII adimensionnées obtenues par les simulations aux valeurs des modèles de prédiction \(\hat{K}_{II}\) et \(\hat{T}\).

- **run_concave.py** : Script pour exécuter des simulations sur des géométries concaves (\(\Delta W\) négatif).

- **run_convexe.py** : Script pour exécuter des simulations sur des géométries convexes (\(\Delta W\) positif).

- **run_droit.py** : Script pour exécuter des simulations sur une géométrie droite (CCT classique).

### Autres Fichiers

- **makefile** : Pour exécuter les scripts de simulation `run_droit.py`, `run_concave.py`, `run_convexe.py`.
- **README.md** : Ce fichier, décrivant le contenu et l'objectif de ce dossier.

## Utilisation

1. Assurez-vous que les dépendances Python nécessaires (par exemple, pandas, numpy, matplotlib) sont installées.
2. Utilisez le makefile pour exécuter les scripts principaux (`run_concave.py`, `run_convexe.py`, `run_droit.py`) ou lancez-les manuellement.
3. Tous les scripts peuvent être lancés en validant dans un terminal ouvert dans le même dossier, le script suivant : python `nom_du_script.py`.
4. Consultez les fichiers de données pour prendre connaissance des données expérimentales.

## Prérequis

- **Python** 3.x
- **Bibliothèques** : itertools, scipy, pandas, numpy, matplotlib, openpyxl (pour les fichiers Excel), os, et utilisation de scikit-learn.
- **Outils** : make (pour utiliser le makefile)

