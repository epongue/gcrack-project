import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

# Lire le fichier Excel des données expérimentales
df1 = pd.read_excel("Dimensions_eprouvettes.xlsx", sheet_name=0)  

angle = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]

# Initialisation des tableaux pour les forces et les FIC normalisés
K1 = np.zeros(17) 
K2 = np.zeros(17)
T = np.zeros(17)

Fc1 = np.zeros(17)

K1_normalised = np.zeros(17)
K2_normalised = np.zeros(17)
T_normalised = np.zeros(17)


V1 = np.zeros(17)
V2 = np.zeros(17)
Vt = np.zeros(17)

Fc2 = np.zeros(17)
FIC_normalise2 = np.zeros(17)
Gc = 380  
E = 2.893e9  
nu = 0.39  # Coefficient de Poisson
KIc = sqrt(E*Gc/(1-nu**2))  
thickness = 3e-3  # Épaisseur de l'éprouvette en mètres

a0 = ['2', '3', '4', '5', '6', '7', '8', '9', '10']

alpha = np.radians(angle)
print(alpha)


for j in range(len(a0)):

    a = int(a0[j])*1e-3

    for i in range(17):
        # Charger le fichier csv
        fichier_csv = f'influence_a_sur_FICs/a={a0[j]}mm/results_{angle[i]}.csv'
        df2 = pd.read_csv(fichier_csv)
        


        # Extraire la colonne voulue et calculer le maximum
        Fc1[i] = df2.iloc[:, 10].max()  
        K1[i] = df2.iloc[1, 11]  
        K2[i] = df2.iloc[1, 12]
        T[i] = df2.iloc[1, 13]



        width = df1.iloc[i, 3]
        stress = Fc1[i] / width
        
        K1_normalised[i] = K1[i] /(stress*sqrt(np.pi*a))  # Stocke la valeur dans le tableau
        K2_normalised[i] = K2[i] /(stress*sqrt(np.pi*a))  # Stocke la valeur dans le tableau
        T_normalised[i] = T[i] / stress 

    


    # Normalisation des valeurs théorique
    for i in range(17):
        V1[i] = (np.cos(alpha[i]))**2
        V2[i] = (np.sin(alpha[i]))*(np.cos(alpha[i]))
        Vt[i] = - np.cos(2*alpha[i])

    
    # Affichage des résultats
    fig = plt.figure()
    plt.scatter(angle, K1_normalised, label='K1 num', marker='o')
    plt.scatter(angle, K2_normalised, label='K2 num', marker='^')
    plt.plot(angle, V1, linestyle='--', color='blue', label=r'$\cos^2 \alpha$', linewidth=1)
    plt.plot(angle, V2, linestyle='-.', color='blue', label=r'$\cos \alpha  \sin \alpha$', linewidth=1)
    plt.xlabel('Angle (degrés)')
    plt.ylabel(r'$\frac{Ki}{\sigma_c \sqrt{\pi a_0}}$', fontsize=14)
    plt.title(f'FIC normalisé en fonction de l\'angle, a0 = {a0[j]}mm')
    plt.grid()
    plt.legend()
    plt.show()

    fig = plt.figure()
    plt.scatter(angle, T_normalised, label='T num', marker='o')
    plt.plot(angle, Vt, linestyle='--', color='blue', label=r'$ - \cos 2\alpha $', linewidth=1)
    plt.xlabel('Angle (degrés)')
    plt.ylabel(r'$\frac{T}{\sigma_c}$', fontsize=14)
    plt.title(f'T-stress normalisé en fonction de l\'angle, a0 = {a0[j]}mm')
    plt.grid()
    plt.legend()
    plt.show()


    