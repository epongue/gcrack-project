import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from math import cos, sin

# Lire le fichier Excel des données expérimentales
df1 = pd.read_excel("Dimensions_eprouvettes.xlsx", sheet_name=0)  

angle = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]

# Initialisation des tableaux pour les forces et les FIC normalisés
K1 = np.zeros(17) 
K2 = np.zeros(17)

K1_exp_l = np.zeros(17)
K1_exp_r = np.zeros(17) 
K2_exp_l = np.zeros(17)
K2_exp_r = np.zeros(17)

Fc1 = np.zeros(17)

K1_normalise = np.zeros(17)
K2_normalise = np.zeros(17)
K1_exp_normalise_l = np.zeros(17)
K1_exp_normalise_r = np.zeros(17)
K2_exp_normalise_l = np.zeros(17)
K2_exp_normalise_r = np.zeros(17)
V1 = np.zeros(17)
V2 = np.zeros(17)

Fc2 = np.zeros(17)
FIC_normalise2 = np.zeros(17)
Gc = 380  # Valeur de Gc en J/m^2
E = 2.893e9  # Module d'élasticité en Pa
nu = 0.39  # Coefficient de Poisson
KIc = sqrt(E*Gc/(1-nu**2))  # Valeur de KIc en Pa.m^0.5
thickness = 3e-3  # Épaisseur de l'éprouvette en mètres

for i in range(17):
    # Charger le fichier csv
    fichier_csv = f'influence_T-stress/Resultats_s=0/results_{angle[i]}.csv'
    df2 = pd.read_csv(fichier_csv)
    


    # Extraire la colonne voulue et calculer le maximum
    Fc1[i] = df2.iloc[:, 10].max()  
    K1[i]= df2.iloc[1, 11]  
    K2[i] = df2.iloc[1, 12]



    width = df1.iloc[i, 3]
    stress = Fc1[i] / width
    a0 = df1.iloc[i, 18]  # Longueur initiale de la fissure en mètres
    K1_normalise[i] = K1[i] /(stress*sqrt(np.pi*a0))  # Stocke la valeur dans le tableau
    K2_normalise[i] = K2[i] /(stress*sqrt(np.pi*a0))  # Stocke la valeur dans le tableau

fichier_csv2 = f'lefm_data.csv'
df3 = pd.read_csv(fichier_csv2)

# Extraire les valeurs expérimentales de K1 et K2
K1_exp_l = df3.iloc[:, 3]
K1_exp_r = df3.iloc[:, 4]
K2_exp_l = df3.iloc[:, 5]
K2_exp_r = df3.iloc[:, 6]
# Normalisation des valeurs expérimentales
for i in range(17):
    width = df1.iloc[i, 3]
    stress = df3.iloc[i, 1] 
    a0 = df1.iloc[i, 18]  # Longueur initiale de la fissure en mètres
    K1_exp_normalise_l[i] = K1_exp_l[i] /(stress*sqrt(np.pi*a0))  # Stocke la valeur dans le tableau
    K1_exp_normalise_r[i] = K1_exp_r[i] /(stress*sqrt(np.pi*a0))  # Stocke la valeur dans le tableau
    K2_exp_normalise_l[i] = K2_exp_l[i] /(stress*sqrt(np.pi*a0))  # Stocke la valeur dans le tableau
    K2_exp_normalise_r[i] = K2_exp_r[i] /(stress*sqrt(np.pi*a0))  # Stocke la valeur dans le tableau
    V1[i] = (cos(np.radians(angle[i])))**2
    V2[i] = (sin(np.radians(angle[i])))*(cos(np.radians(angle[i])))


# Affichage des résultats
plt.scatter(angle, K1_normalise, label='K1 num', marker='o')
plt.scatter(angle, K2_normalise, label='K2 num', marker='^')
plt.scatter(angle, K1_exp_normalise_l, label='K1 exp', marker='s', facecolor='none', edgecolors='k')
plt.scatter(angle, K1_exp_normalise_r, label=None, marker='s', facecolor='none', edgecolors='k')
plt.scatter(angle, K2_exp_normalise_l, label='K2 exp', marker='v', facecolor='none', edgecolors='k')
plt.scatter(angle, K2_exp_normalise_r, label=None, marker='v', facecolor='none', edgecolors='k')
plt.plot(angle, V1, linestyle='--', color='blue', label=r'$cos^2 \alpha$', linewidth=1)
plt.plot(angle, V2, linestyle='-.', color='blue', label=r'$cos \alpha  sin \alpha$', linewidth=1)
plt.xlabel('Angle (degrés)')
plt.ylabel(r'$\frac{Ki}{\sigma_c \sqrt{\pi a_0}}$', fontsize=14)
plt.title('FIC normalisé en fonction de l\'angle')
plt.grid()
plt.legend()
plt.show()
