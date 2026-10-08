# The goal is to use the differential-reactor data to test a rate law and estimate the kinetic parameters.
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
rate_table = np.array([71, 71.3, 41.6, 19.7, 42, 17.1, 71.8, 142, 284, 47, 71.3, 117, 127, 131, 133, 41.8], dtype=float)
#Partial Pressures in atm
pT = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 1, 5, 10, 15, 20, 1], dtype=float)
pH = np.array([1, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1, 1, 1, 1, 1, 1], dtype=float)
pM = np.array([1, 4, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=float)
pB = np.array([0, 0, 1, 4, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=float)
# print('Number of experiments:', len(rate_table)) --> Number of experiments: 16
# Runs 7, 8, and 9 vary only hydrogen pressure.
# Runs 3, 4, and 6 vary benzene pressure at pT=pH=1 atm.
# Runs 12-15 vary toluene pressure.
# rate = k * pT * pH / (1 + KB * pB + KT * pT)
def rate(Pressures, k, KB, KT):
    pT, pH, pB = Pressures
    return k * pT * pH / (1 + KB * pB + KT * pT)
initial_guess = [1, 1, 1]
parameters, covariance = curve_fit(rate, (pT, pH, pB), rate_table, p0=initial_guess,bounds=(0,np.inf),maxfev=1000,)
k, KB, KT = parameters
predicted_rates = rate((pT, pH, pB), k, KB, KT)
# k = 144.76730766963834 
# KB = 1.390526397824852 
# KT = 1.0384105567258959 
Residuals = rate_table - predicted_rates
rmse= np.sqrt(np.mean(Residuals**2))
r_squared = 1 - (np.sum(Residuals**2) / np.sum((rate_table - np.mean(rate_table))**2))
# RMSE = 0.4514219906820465
# R^2 = 0.9999509157577747
comparison = np.column_stack((np.arange(1, 17), rate_table, predicted_rates, Residuals))

plt.figure(figsize=(6, 5))
plt.scatter(rate_table, predicted_rates, color='teal', edgecolor='black', label='16 experiments')
limit = max(rate_table.max(), predicted_rates.max()) * 1.05
plt.plot([0, limit], [0, limit], '--', color='gray', label='perfect prediction')
plt.xlabel('Observed rate (table units)')
plt.ylabel('Predicted rate (table units)')
plt.title('Nonlinear regression quality check')
plt.legend()
plt.grid(alpha=0.25)
plt.show()