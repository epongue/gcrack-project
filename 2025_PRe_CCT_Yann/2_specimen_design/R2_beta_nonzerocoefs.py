import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Choisir le paramètre à analyser
#param = 'T'  
param = 'KII'  

# Degré du polynôme, se rassurer de la bonne correspondance avec la régression
N_degree = 3

# modifier la valeur de beta après votre choix
beta = 0.008185  



# Charger les données depuis le fichier CSV
results = pd.read_csv(f'ResultsRegression/choix_beta_{param}_N={N_degree}.csv')


# Trier le DataFrame par Beta pour avoir des points bien ordonnés
results_df_sorted = results.sort_values(by='Beta')

# Chercher la valeur de R² pour le beta choisi
# (on prend la valeur la plus proche dans le tableau)
idx = (results_df_sorted['Beta'] - beta).abs().idxmin()
R2_beta = results_df_sorted.loc[idx, 'R2_Score']
Nbr_coef_non_nuls = results_df_sorted.loc[idx, 'Non_Zero_Coefficients']

fig, ax1 = plt.subplots(figsize=(8, 5))

# Axe Y gauche : R² (points bleus ronds)
color = 'tab:blue'
ax1.set_xlabel('Beta (paramètre de régularisation)',fontsize = 12)
ax1.set_ylabel(r'$R^2$',fontsize = 12)
# ax1.scatter(results_df_sorted['Beta'], results_df_sorted['RRMSE'], color= 'k', label='RRMSE', marker='o')
ax1.axvline(x=beta, color='gray', linestyle='--', linewidth=2, label=r'$\beta$'+ f' choisi = {beta}')
ax1.scatter(results_df_sorted['Beta'], results_df_sorted['R2_Score'], color='blue', 
label=r'$R^2$ '+ r'($\beta$)' + f' = {R2_beta : .3f}', marker='o')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xscale('log')
ax1.set_ylim(0, 1)
ax1.grid(True)
plt.legend(loc='upper right', fontsize = 12)
# Axe Y droit : Non_Zero_Coefficients (points rouges triangulaires)
ax2 = ax1.twinx()
color_coeff = 'tab:red'
ax2.set_ylabel('Nombre de coefficients non nuls (NCNN)', color=color_coeff,fontsize = 12)
ax2.scatter(results_df_sorted['Beta'], results_df_sorted['Non_Zero_Coefficients'], color=color_coeff, 
label='NCNN'+ r'($\beta$)' + f' = {Nbr_coef_non_nuls}', marker='^')
ax2.set_ylim(1, 24)
ax2.tick_params(axis='y', labelcolor=color_coeff)

# Titre du graphe
plt.title(f'R^2 et Nbre de coeffs non nuls en fonction de Beta ({param} - deg_polynôme = {N_degree})', fontsize = 14)

# plt.title(f' RRMSE et Nbre de coeffs non nuls en fonction de Beta ({param} - deg_polynôme = {N_degree})')
fig.tight_layout()
plt.legend(loc='lower left', fontsize = 12)
plt.grid(True)
plt.show()



