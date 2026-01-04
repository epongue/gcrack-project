import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
#----pour tracer le

# Lire le fichier Excel des données expérimentales
df = pd.read_csv('lefm_data.csv')
df1 = pd.read_excel("Dimensions_eprouvettes.xlsx", sheet_name=0)  


# Expérimental
FIC_normalise_exp = np.zeros(17)
stress_exp = np.zeros(17)

stress_exp = df.iloc[:, 1]*1e6  # contrainte à la rupture en Pa


cas = ['0', '10da']
angle = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]

# Numérique
Fc2 = np.zeros(17)
FIC_normalise2 = np.zeros(17)

Fc3 = np.zeros(17)
FIC_normalise3 = np.zeros(17)

Fc4 = np.zeros(17)
FIC_normalise4 = np.zeros(17)

Fc5 = np.zeros(17)
FIC_normalise5 = np.zeros(17)

# Données matériaux
Gc = 380  # Valeur de Gc en kJ/m^2
E = 2.893e9  # Module d'élasticité en Pa
nu = 0.39  # Coefficient de Poisson
KIc = sqrt(E*Gc/(1-nu**2))  # Valeur de KIc en MPa.m^0.5
thickness = 3e-3  # Épaisseur de l'éprouvette en mètres

folder = 'influence_T-stress'


for i in range(17):


    width = df1.iloc[i, 3]
    a0 = df1.iloc[i, 18]  # Longueur initiale de la fissure en mètres

    #-----------Expérimental----------------------------
    FIC_normalise_exp[i] = stress_exp[i] * sqrt(np.pi * a0) / KIc

    #----------------s = 0---------------------------
    # Charger le fichier csv
    df2 = pd.read_csv(f'{folder}/Resultats_s=0/results_{angle[i]}.csv')

    # Extraire la colonne voulue et calculer le maximum
    Fc2[i] = df2.iloc[1, 10]

    stress = Fc2[i] / width
  
    FIC_normalise2[i] = stress * sqrt(np.pi * a0) / KIc  # Stocke la valeur dans le tableau

    #----------------s = 0.5da---------------------------
    # Charger le fichier csv
    df3 = pd.read_csv(f'{folder}/Resultats_s=0.5da/results_{angle[i]}.csv')

    # Extraire la colonne voulue et calculer le maximum
    Fc3[i] = df3.iloc[1, 10]

    stress = Fc3[i] / width
    FIC_normalise3[i] = stress * sqrt(np.pi * a0) / KIc  # Stocke la valeur dans le tableau

    #----------------s = 2da---------------------------
    # Charger le fichier csv
    df4 = pd.read_csv(f'{folder}/Resultats_s=2da/results_{angle[i]}.csv')

    # Extraire la colonne voulue et calculer le maximum
    Fc4[i] = df4.iloc[1, 10]

    stress = Fc4[i] / width

    FIC_normalise4[i] = stress * sqrt(np.pi * a0) / KIc  # Stocke la valeur dans le tableau

    #----------------s = 10da---------------------------
    # Charger le fichier csv
    df5 = pd.read_csv(f'{folder}/Resultats_s=10da/results_{angle[i]}.csv')

    # Extraire la colonne voulue et calculer le maximum
    Fc5[i] = df5.iloc[1, 10]

    stress = Fc5[i] / width

    FIC_normalise5[i] = stress * sqrt(np.pi * a0) / KIc  # Stocke la valeur dans le tableau



# Affichage des résultats
plt.scatter(angle, FIC_normalise2, label='s= 0', marker='o')
plt.scatter(angle, FIC_normalise3, label='s= 5e-3 = 0.5da', marker='^')
plt.scatter(angle, FIC_normalise4, label='s= 2da', marker='v')
plt.scatter(angle, FIC_normalise5, label='s= 10da', marker='*')
plt.scatter(angle, FIC_normalise_exp, label='Expérimental', marker='s',facecolor='none', edgecolors='k')
plt.xlabel('Angle (degrés)')
plt.ylabel(r'stress $\frac{\sigma_c \cdot \sqrt{\pi \cdot a_0}}{K_{Ic}}$', fontsize=12)
plt.title('stress normalisé en fonction de l\'angle')
plt.grid()
plt.legend()
plt.show()

