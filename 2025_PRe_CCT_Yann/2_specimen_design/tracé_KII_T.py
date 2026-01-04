import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# --- Paramètres ---
angle = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
rayon = ['r7', 'r6', 'r5', 'r4', 'r3', 'r2','r20', 'r19', 'r18', 'r17', 'r1', 'r14', 'r13', 'r12', 'r11', 'r10', 'r9', 'r8']
dw = np.array([-25, -19.45, -15.45, -12.5, -10.35, -7.57, -4.8, -3.5, -3.08, -2.74, 0, 2.75, 3.08, 3.5, 4.06, 4.81, 5.9, 7.57])
dw_adim = dw / 3

a0 = [2.82e-3, 2.9e-3, 2.9e-3, 2.86e-3, 2.89e-3, 2.89e-3, 2.85e-3, 2.91e-3, 2.91e-3, 2.86e-3,
      2.91e-3, 2.91e-3, 2.84e-3, 2.87e-3, 2.87e-3, 2.85e-3, 2.87e-3]

M_angle = len(angle)
N_rayon = len(rayon)

# --- Matrices résultats ---
KI_matx  = np.zeros((N_rayon, M_angle))
KII_matx = np.zeros((N_rayon, M_angle))
T_matx   = np.zeros((N_rayon, M_angle))

# --- Extraction des données ---
for i in range(M_angle):
    KI = np.zeros(N_rayon)
    KII = np.zeros(N_rayon)
    T = np.zeros(N_rayon)

    for j in range(N_rayon):
        fichier_csv = f'E2_s=0/angle_{angle[i]}/results_{rayon[j]}_{angle[i]}.csv'
        df = pd.read_csv(fichier_csv)

        KI[j]  = df.iloc[1, 11]
        KII[j] = df.iloc[1, 12]
        T[j]   = df.iloc[1, 13]

        Keq = np.sqrt(KI[j]**2 + KII[j]**2)

        KI_matx[j, i]  = KI[j]  / Keq
        KII_matx[j, i] = KII[j] / Keq
        T_matx[j, i]   = T[j] * np.sqrt(np.pi * a0[i]) / Keq


# --- Courbe milieu infini ---
alpha = np.radians(angle)
KII_infini_adim = np.sin(alpha)
T_infini_adim   = np.cos(alpha) * (np.tan(alpha)**2 - 1)

# --- Figure ---
fig, ax = plt.subplots(figsize=(7, 7))

# Colormap et markers
cmap = cm.get_cmap('cool')
norm = plt.Normalize(vmin=min(angle), vmax=max(angle))
markers = ['X', '^', 's', 'd', 'x', 'v', '*', '<', 'p', 'o', '8', '>', 'D', 'P', 'H', 'h', '+', '.']

# Points où KI < 0
negatifs = np.argwhere(KI_matx < 0)

# --- Tracé des points ---
for j in range(N_rayon):
    mask = KI_matx[j, :] >= 0  # Garde uniquement KI >= 0
    ax.scatter(
        T_matx[j, mask], KII_matx[j, mask],
        marker=markers[j],
        c=np.array(angle)[mask],  # garder cohérence avec les couleurs
        cmap=cmap, norm=norm,
        edgecolors='face',
        s=50, alpha=0.8,
        label=f'dW_adim = {dw_adim[j]:.2f} mm' if j in [0, N_rayon - 1] else None
    )

# ScalarMappable pour la colorbar
sm = cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])  # nécessaire pour matplotlib < 3.6



# # Marqueurs creux pour KI < 0
# for j, i in negatifs:
#     ax.scatter(
#         T_matx[j, i], KII_matx[j, i],
#         marker=markers[j % len(markers)],
#         facecolors='none',
#         edgecolors='k',
#         linewidths=1.2,
#         s=60,
#         zorder=5
#     )


# Courbe milieu infini
ax.plot(
    T_infini_adim, KII_infini_adim,
    linestyle='--', linewidth=2, color='k',
    label='Milieu infini'
)

# Légende et colorbar
ax.legend(ncol=2, bbox_to_anchor=(1.0,0), loc='lower right')
cbar = fig.colorbar(sm, ax=ax, pad=0.02)
cbar.set_label('Angle (°)', fontsize=20)

# --- Légende unique ---
handles, labels = ax.get_legend_handles_labels()
unique = dict(zip(labels, handles))
ax.legend(unique.values(), unique.keys())

# --- Flèches verticales ---
ax.annotate('', xy=(0.2, 0.4), xytext=(0.2, 0.3),
            arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=1.8))
ax.annotate('', xy=(-0.9, 0.7), xytext=(-0.9, 0.8),
            arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=1.8))

# --- Axes ---
ax.set_xlabel('T_adim', fontsize=20)
ax.set_ylabel('KII_adim', fontsize=20)
plt.title("Distribution des KII et T selon les rayons et angles", fontsize=20)
plt.legend(fontsize=20)
plt.show()
