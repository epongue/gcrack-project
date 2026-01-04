import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def T_modele(alpha, delta_W): # N_degre = 3
    tan_alpha = np.tan(alpha)
    sin_alpha = np.sin(alpha)
    T = (
           
        -7.46e-01 * 1
        + 1.01e+00 * (sin_alpha * tan_alpha)
    )
    return T



# def T_modele(alpha, delta_W=None): # N_degre = 10
#     return (
#         -9.64e-01 * (np.cos(alpha)**2)
#         + 3.12e-01 * (np.cos(alpha)**4) * (np.tan(alpha)**5)
#         + 1.99e+00 * (np.cos(alpha)**5) * (np.tan(alpha)**5)
#     )


def KII_modele(alpha, delta_W):

    return (
        1.33e-02 * 1
        + 9.69e-01 * np.sin(alpha)
        - 1.03e-02 * delta_W
    )

#----------------------------------DEBUT--------------------------------------
""" Representation graphique de T et KII en fonction de dW et tan(alpha) """


# Chargement des données

KI_adim = np.zeros(18)
KII_adim = np.zeros(18)
T_adim = np.zeros(18)

KI_target = np.zeros(18*17)
# Données 3D
KI = np.zeros(18)
KII = np.zeros(18)
T = np.zeros(18)

KI_adim = np.zeros(18)
KII_adim = np.zeros(18)
T_adim = np.zeros(18)

KI_target = np.zeros(18*17)
KII_target = np.zeros(18*17)
T_target = np.zeros(18*17)

angle_input = np.zeros(18*17)
dW_input = np.zeros(18*17)



rayon_input = ["" for i in range(18*17)]


X = np.zeros((18*17, 2))

# Angles and radius

angle = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
rayon = ['r7', 'r6', 'r5', 'r4', 'r3', 'r2','r20', 'r19', 'r18', 'r17', 'r1', 'r14', 'r13', 'r12', 'r11', 'r10', 'r9', 'r8']
# r = ['-45.07', '-35.35', '-31.25', '-27.95', '-25.77', '-25', 'infini', '45.07', '55.9', '62.69', '79.06', '87.64', '100.12', '115.24']

dw = [-25, -19.45, -15.45, -12.5, -10.35, -7.57, -4.8, -3.5, -3.08, -2.74, 0, 2.75, 3.08, 3.5, 4.06, 4.81, 5.9, 7.57]

dw = np.array(dw)         # Conversion en tableau NumPy
dw_adim = dw / 3          # Opération vectorisée

a0 =[2.82e-3, 2.9e-3, 2.9e-3, 2.86e-3, 2.89e-3, 2.89e-3, 2.85e-3, 2.91e-3, 2.91e-3, 2.86e-3,
     2.91e-3, 2.91e-3, 2.84e-3, 2.87e-3, 2.87e-3, 2.85e-3, 2.87e-3]

M_angle = len(angle)  # number of angles
N_rayon = len(rayon)  # number of radius

for I, (i,j) in enumerate(itertools.product(range(M_angle), range(N_rayon))):

    # Extraction of csv files for various radius and angles
    fichier_csv = f'E2_s=0/angle_{angle[i]}/results_{rayon[j]}_{angle[i]}.csv'
    df = pd.read_csv(fichier_csv)

    # Extraction of KI, KII, and T
    KI = df.iloc[1, 11]
    KII = df.iloc[1, 12]
    T = df.iloc[1, 13]


    Keq = np.sqrt(KI**2 + KII**2)

    KI_target[I] = KI / Keq
    KII_target[I] = KII / Keq
    T_target[I] = T*np.sqrt(np.pi*a0[i]) / (Keq)
    
    angle_input[I] = angle[i]*np.pi/180  # Conversion en radians
    dW_input[I] = dw_adim[j]
    rayon_input[I] = rayon[j]

tan_alpha = np.tan(angle_input)  # Calcul de tan(alpha)
sin_alpha = np.sin(angle_input)
# Récupération des indices  des valeurs positves et négatives de KI_target
k1 = np.where(KI_target >= 0)[0] 
k2 = np.where(KI_target < 0)[0]


# Calcul de tan(alpha)
angle_k1 = angle_input[k1]  # On ne garde que les angles correspondants aux valeurs de KI_target positives
dW_k1 = dW_input[k1]  # On ne garde que les dW correspondants aux valeurs de KI_target positives

tan_alpha_k1 = np.tan(angle_k1)

# Calcul de T obtenue par le modèle
T_modèle = T_modele(angle_k1, dW_k1) 

# Calcul de KII obtenue par le modèle

KII_modèle = KII_modele(angle_k1, dW_k1) 



# Tracé  T
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Points normaux (positifs ou nuls) — pleins
sc1 = ax.scatter(dW_k1, tan_alpha_k1, T_target[k1],
                c=T_target[k1], cmap='cool', marker='o', vmin = -1, vmax = 5)

sc1 = ax.scatter(dW_k1, tan_alpha_k1, T_modèle, color = 'red', marker='o')

# # Points négatifs — creux (bordure colorée, intérieur blanc)
# sc2 = ax.scatter(dW_input[k2], tan_alpha[k2], T_target[k2],
#                  facecolors='none', edgecolors='black', marker='o')
# Étiquettes
ax.set_xlabel(r'$\widehat{\Delta W}$', fontsize = 16)
ax.set_ylabel(r'$\tan(\alpha)$', fontsize = 16)
ax.set_zlabel('T_adim', fontsize = 16)
ax.set_title('T_adim'+' en fonction de'+r' $\Delta W$'+' et'+r' $\tan(\alpha)$', fontsize=16)
ax.set_zlim(-2, 5)
fig.colorbar(sc1, ax=ax, label='T_adim')
plt.legend(fontsize=14)
plt.tight_layout()
plt.show()




# Tracé KII
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
# Points normaux (positifs ou nuls) — pleins
sc1 = ax.scatter(dW_k1, sin_alpha[k1], KII_target[k1],
                 c=KII_target[k1], cmap='cool', marker='o', vmin = 0, vmax = 1)

sc1 = ax.scatter(dW_k1, sin_alpha[k1], KII_modèle, color = 'red', marker='o')

# # Points négatifs — creux (bordure colorée, intérieur blanc)
# sc2 = ax.scatter(dW_input[k2], sin_alpha[k2], KII_target[k2],
#                  facecolors='none', edgecolors='black', marker='o')

# Étiquettes
ax.set_xlabel(r'$\widehat{\Delta W}$', fontsize=16)
ax.set_ylabel(r'$\sin(\alpha)$', fontsize=16)
ax.set_zlabel('KII_adim', fontsize=16)
ax.set_zlim(-1, 1)
ax.set_title(r'$K_{II}\_adim$'+' en fonction de'+r' $\Delta W$'+' et'+r' $\tan(\alpha)$', fontsize=16)
fig.colorbar(sc1, ax=ax, label='KII_adim')
plt.legend(fontsize=14)
plt.tight_layout()
plt.show()

