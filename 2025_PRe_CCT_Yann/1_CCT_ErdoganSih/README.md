# Répertoire de Scripts et Données

Ce répertoire contient les scripts et données utilisés dans la première partie du rapport pour l'analyse et comparaisons de trajectoires de fissure expérimentales aux simulations numériques.

## Arborescence du Dossier

├── Comparaison_résultats.py
├── dimensions.csv
├── Dimensions_eprouvettes.xlsx
├── Exp_path_transformed
├── influence_a_sur_FICs
├── influence_T-stress
├── lefm_data.csv
├── makefile
├── README.md
├── run_droit.py
├── specimen_data
├── stress_normalised.py
├── test_de_convergence
├── Tracé des SIFs.py
├── Tracé_SIFs_influence_a.py
└── transformation_geométrique.py


### Fichiers de Données

- **dimensions.csv** : Contient la largeur et l'épaisseur expérimentaux de chaque éprouvette.
- **Dimensions_eprouvettes.xlsx** : Fichier Excel détaillant les dimensions en pixel des éprouvettes prises dans chaque image.
- **lefm_data.csv** : Contient toutes les FICs obtenues par DIC.
- **specimen_data/** : Dossier contenant les points des trajectoires expérimentales en pixel de chaque spécimen.

### Scripts Python

- **transformation_geométrique.py** : Récupère, réoriente et remet à l'échelle tous les points des trajectoires expérimentales, puis les superpose aux trajectoires numériques pour comparaison.
- **Comparaison_résultats.py** : N'affiche que 4 à 5 angles pour la comparaison des trajectoires, utilisé dans la sous-section 4.3 du rapport.
- **stress_normalised.py** : Affiche la contrainte à la rupture normalisée expérimentale (avant la propagation) et la compare à la contrainte à la rupture normalisée numérique pour différentes valeurs de s. Permet d'obtenir la figure 4.11 dans le rapport.
- **Tracé des SIFs.py** : Affiche les FICs expérimentaux, numériques et théoriques. Utilisé pour obtenir la figure 4.4 dans le rapport.
- **Tracé_SIFs_influence_a.py** : Visualise l'influence du paramètre a sur les SIFs.
- **run_droit.py** : Script pour exécuter des simulations sur une géométrie droite (CCT classique).

### Dossiers de stockage des données

- **Exp_path_transformed/** : Contient les points des trajectoires expérimentales de chaque éprouvette suite à la transformation effectuée dans le script `transformation_geométrique.py`.
- **influence_a_sur_FICs/** : Contient les résultats des simulations pour différentes valeurs de a.
- **influence_T-stress/** : Contient les résultats des simulations pour différentes valeurs de s.
- **test_de_convergence/** : Contient les résultats des simulations pour différentes précisions du maillage au sein de l'éprouvette (contrôlée par h) et au voisinage de la pointe de fissure (contrôlée par hmin).

### Autres Fichiers

- **makefile** : Pour exécuter le script de simuulation `run_droit.py`.
- **README.md** : Ce fichier, décrivant le contenu et l'objectif du projet.

## Utilisation

1. Assurez-vous que les dépendances Python nécessaires (par exemple, pandas, numpy, matplotlib) sont installées.
2. Utilisez le makefile pour exécuter les scripts principaux (`run_concave.py`, `run_convexe.py`, `run_droit.py`) ou lancez-les manuellement.
3. Les résultats des simulations pour obtenir les différentes courbes sont stockés dans les dossiers `influence_T-stress/`, `influence_a_sur_FICs/`, `test_de_convergence/`.
4. Tous les scripts peuvent être lancés en validant dans un terminal ouvert dans le même dossier : python nom\_du\_script.py.
5. Consultez les fichiers de données (`dimensions.csv`, `lefm_data.csv`) pour prendre connaissance des données expérimentales.

## Prérequis

- **Python** 3.x
- **Bibliothèques** : scipy, pandas, numpy, matplotlib, openpyxl (pour les fichiers Excel), os
- **Outils** : make (pour utiliser le makefile)

