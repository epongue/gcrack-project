import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, MaxAbsScaler
from sklearn.linear_model import Lasso
import numpy as np
import pandas as pd
import itertools
from sklearn.model_selection import train_test_split
import os

#----------------------------------DEBUT-------------------------------------------------------------------


# Chargement des données

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

angle_train = np.zeros(190)
dW_train = np.zeros(190)

angle_test = np.zeros(48)
dW_test = np.zeros(48)

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
    


    Keq = np.sqrt(KI**2 + KII**2)

    KI_target[I] = KI / Keq
    KII_target[I] = KII / Keq    
    
    angle_input[I] = angle[i]*np.pi/180  # Conversion en radians
    dW_input[I] = dw_adim[j]
    rayon_input[I] = rayon[j]


#pour ne garder que les indices des composantes de KI_target positives
k = np.where(KI_target >= 0)[0] 


# --------------------Polynomial Regression------------------------
N_degree = 3  #degree du polynôme
beta = np.logspace(-4, 0, 70)  

#création du dosssier où stocker les données
folder_name = 'ResultsRegression'
os.makedirs(f'{folder_name}/coef_poly_KII_N={N_degree}', exist_ok=True)

#data
angle_input = angle_input[k]
angle_data = np.sin(angle_input)
dW_data = dW_input[k]
X = np.column_stack((angle_data, dW_data))
y = KII_target[k]  # KII


# Polynomial features 
poly = PolynomialFeatures(degree = N_degree, include_bias = True)
X_poly = poly.fit_transform(X)


# Standardisation of features
# scaler = StandardScaler()
scaler = MaxAbsScaler()
X_poly_scaled = scaler.fit_transform(X_poly)
scales = scaler.scale_
# means = scaler.mean_

# Set train/test split 
X_train, X_test, y_train, y_true = train_test_split(X_poly_scaled, y, test_size=0.2, random_state=42) # for KII

# initialization of arrays for results
results_table = pd.DataFrame(columns=['Beta', 'R2_Score', 'Non_Zero_Coefficients', 'RRMSE'])

for i in range(len(beta)) :

    # Lasso regression 
    model = Lasso(alpha = beta[i], fit_intercept=False, random_state = 42)
    model.fit(X_train, y_train)

    # chosen beta  
    print(f"\n Paramètre beta pour la prédiction de KII: {beta[i]}") 

    # model coefficients
    coefficients = model.coef_ / scales
    # coefficients[0] -= sum(model.coef_ * means / scales)
    intercept = model.intercept_



    # Displaying the coefficients with feature namesNbre de paramètre
    feature_names = poly.get_feature_names_out(input_features=[r'\sin(\alpha)', r'\Delta W'])
    # Coefficients DataFrame for KII
    coefficients_df = pd.DataFrame({
        'Monôme': feature_names,
        'Coefficient': model.coef_,
        'intercept': model.intercept_
    })

    print(coefficients_df)

    print(r"KII(\alpha, \Delta W) = ", end="")
    for coeff, name in zip(coefficients, feature_names):
        if coeff != 0:
            print(f"{coeff:.2e}" + r"\times" + f"{name}", end=" + ")
    print("\n") 


    # Performance evaluation
    r2_score_test = model.score(X_test, y_true)
    print(f"\nScore R² pour la prédiction de KII : {r2_score_test:.3f}")

    # Count non-zero coeffficients
    non_zero_coef = np.sum(coefficients != 0)

    # for model verification
    y_pred = model.predict(X_test)

    e = np.linalg.norm(y_pred - y_true) / np.linalg.norm(y_true)

    # performance evaluation
    print(f"\n RRMSE pour la prédiction de KII : {e:.3f}"+"\n --------FIN--------")

    # add results to the table
    results_table.loc[i] = [beta[i], r2_score_test, non_zero_coef, e]

    # Save coefficients to CSV


    coefficients_df.to_csv(f'{folder_name}/coef_poly_KII_N={N_degree}/coefs_beta={beta[i]:.5f}_r2={r2_score_test:.3f} .csv', index=False)

    # -------------------- Affichage ------------------------#
    y_pred = model.predict(X_test)

    # # model verification for KII prediction for a given beta
    # fig, ax = plt.subplots(figsize=(8, 4))
    # ax.scatter(y_true, y_pred, label="prédictions", marker='x')   
    # ax.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', label='y = x')
    # ax.set_title(f"Prédictions (beta = {beta[i]}) vs Vraies", fontsize = 16)
    # ax.set_xlabel("KII_test adim", fontsize = 16)
    # ax.set_ylabel("KII_prédit adim", fontsize = 16)
    # ax.axis('equal')
    # ax.legend(fontsize = 16)
    # plt.grid(True)
    # plt.tight_layout()
    # plt.show()

# save results to CSV
results_table.to_csv(f"{folder_name}/choix_beta_KII_N={N_degree}.csv", index=False) 

