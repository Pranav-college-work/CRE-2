import numpy as np
from scipy.optimize import least_squares, brentq

# data - CO2 aur CH4 zeolite 13X par
T_vals = [298, 308, 323]
R = 8.314

CO2_298 = np.array([[0.0, 0.0], [0.00118, 1.147], [0.0061, 2.249], [0.02905, 3.659], [0.0861, 4.5], [0.16, 5.06], [0.31, 5.58], [0.525, 6.04], [1.015, 6.52], [1.015, 6.5], [1.445, 6.92], [1.935, 6.96], [2.28, 7.09], [2.66, 7.22], [3.2, 7.372]]).T
CO2_308 = np.array([[0.0, 0.0], [0.00126, 0.825], [0.00407, 1.458], [0.00905, 2.06], [0.01325, 2.4], [0.02007, 2.734], [0.04515, 3.38], [0.09503, 4.05], [0.16, 4.49], [0.22, 4.74], [0.28, 4.96], [0.37, 5.167], [0.485, 5.315], [0.57, 5.399], [0.7, 5.586], [0.875, 5.718], [0.875, 5.718], [1.015, 5.803], [1.2, 5.942], [1.505, 6.116], [1.83, 6.291], [2.235, 6.51], [2.5, 6.631], [2.86, 6.769], [3.065, 6.885], [3.065, 6.82], [3.365, 6.92]]).T
CO2_323 = np.array([[0.0, 0.0], [0.00106, 0.356], [0.00214, 0.529], [0.00501, 1.06], [0.00907, 1.43], [0.02423, 2.09], [0.0422, 2.49], [0.07503, 2.9], [0.145, 3.4], [0.27, 3.915], [0.39, 4.1], [0.545, 4.329], [0.705, 4.532], [0.85, 4.74], [1.01, 4.82], [1.175, 4.93], [1.455, 5.2], [1.72, 5.24], [2.125, 5.43], [2.695, 5.62], [3.395, 5.762]]).T

CH4_298 = np.array([[0.0, 0.0], [0.00405, 0.024], [0.01203, 0.089], [0.0191, 0.131], [0.05515, 0.326], [0.125, 0.712], [0.165, 0.877], [0.21, 1.12], [0.306, 1.474], [0.345, 1.617], [0.425, 1.83], [0.631, 2.357], [0.819, 2.726], [1.07, 3.06], [1.18, 3.26], [1.41, 3.53], [1.72, 3.834], [1.89, 3.991], [2.175, 4.198], [2.61, 4.506], [2.985, 4.75], [3.365, 4.987], [3.56, 5.103], [3.745, 5.191], [3.745, 5.191], [4.26, 5.469], [4.725, 5.719]]).T
CH4_308 = np.array([[0.0, 0.0], [0.00525, 0.022], [0.01115, 0.064], [0.0204, 0.109], [0.04007, 0.21], [0.08516, 0.415], [0.135, 0.623], [0.135, 0.632], [0.19, 0.823], [0.28, 1.133], [0.31, 1.232], [0.35, 1.36], [0.445, 1.618], [0.585, 1.931], [0.585, 1.932], [0.695, 2.154], [0.78, 2.342], [0.875, 2.466], [1.11, 2.792], [1.48, 3.201], [1.7, 3.409], [1.79, 3.48], [2.17, 3.781], [2.53, 4.038], [2.535, 4.034], [2.84, 4.236], [3.64, 4.702], [4.015, 4.884], [4.49, 5.127], [4.72, 5.234]]).T
CH4_323 = np.array([[0.0, 0.0], [0.00603, 0.017], [0.01215, 0.052], [0.022, 0.09], [0.03302, 0.14], [0.04612, 0.196], [0.05505, 0.227], [0.0801, 0.312], [0.115, 0.432], [0.165, 0.59], [0.24, 0.731], [0.34, 1.009], [0.34, 1.009], [0.4, 1.193], [0.51, 1.423], [0.505, 1.395], [0.635, 1.653], [0.78, 1.929], [0.865, 2.077], [0.955, 2.211], [1.185, 2.545], [1.495, 2.89], [1.695, 3.067], [1.86, 3.169], [2.425, 3.577], [2.57, 3.67], [3.015, 3.933], [3.425, 4.199], [3.425, 4.2], [3.67, 4.341], [4.18, 4.585], [4.445, 4.706], [4.745, 4.83]]).T

# toth model equation
def toth(p, qmax, K, n):
    Kp = K * p
    return qmax * Kp / (1 + Kp**n)**(1/n)

def fit_toth(data_dict):
    P = [data_dict[T][0] for T in T_vals]
    Q = [data_dict[T][1] for T in T_vals]

    def res(x):
        qmax, n, Ks = x[0], x[1], x[2:]
        errors = []
        for i in range(len(T_vals)):
            errors.append(toth(P[i], qmax, Ks[i], n) - Q[i])
        return np.concatenate(errors)

    guess = [max(q.max() for q in Q) * 1.15, 0.7] + [5.0] * len(T_vals)
    sol = least_squares(res, guess, bounds=([0, 0.05] + [0]*len(T_vals), np.inf), xtol=1e-14, ftol=1e-14)

    qmax, n, Ks = sol.x[0], sol.x[1], sol.x[2:]
    return qmax, n, dict(zip(T_vals, Ks))

# multi site langmuir
def msl_solve_theta(p, K, a):
    p = np.atleast_1d(np.asarray(p, float))
    theta = np.zeros_like(p)
    for i, pi in enumerate(p):
        if pi > 0:
            theta[i] = brentq(lambda t: t - K * pi * (1 - t)**a, 0.0, 1 - 1e-14, xtol=1e-14)
    return theta

def msl(p, qmax, K, a):
    return qmax * msl_solve_theta(p, K, a)

def fit_msl(data_dict, qmax, K0):
    P = [data_dict[T][0][data_dict[T][0] > 0] for T in T_vals]
    TH = [data_dict[T][1][data_dict[T][0] > 0] / qmax for T in T_vals]

    def res(x):
        a, Ks = x[0], x[1:]
        errors = []
        for i in range(len(T_vals)):
            errors.append(np.log(TH[i] / (Ks[i] * (1 - TH[i])**a)) - np.log(P[i]))
        return np.concatenate(errors)

    best = None
    for a0 in [1.5, 2.5, 4.0, 6.0]:
        sol = least_squares(res, [a0] + [K0] * len(T_vals),
                           bounds=([1.0] + [1e-9]*len(T_vals), np.inf), xtol=1e-14, ftol=1e-14)
        if best is None or sol.cost < best.cost:
            best = sol

    a, Ks = best.x[0], best.x[1:]
    return a, dict(zip(T_vals, Ks))

# van't hoff
def vant_hoff_calc(Ks):
    T_arr = np.array(T_vals, float)
    inv_T = 1 / T_arr
    ln_K = np.log([Ks[T] for T in T_vals])
    m, c = np.polyfit(inv_T, ln_K, 1)
    dH = -m * R / 1000
    return dH

CO2_data = {298: CO2_298, 308: CO2_308, 323: CO2_323}
CH4_data = {298: CH4_298, 308: CH4_308, 323: CH4_323}

print("Toth Isotherm:")
co2_toth = fit_toth(CO2_data)
ch4_toth = fit_toth(CH4_data)

print(f"CO2 - qmax: {co2_toth[0]}, n: {co2_toth[1]}")
for T in T_vals:
    print(f"K_{T}: {co2_toth[2][T]}")
print(f"CH4 - qmax: {ch4_toth[0]}, n: {ch4_toth[1]}")
for T in T_vals:
    print(f"K_{T}: {ch4_toth[2][T]}")

print("\nMulti-site Langmuir:")
co2_msl = (co2_toth[0], *fit_msl(CO2_data, co2_toth[0], 100.0))
ch4_msl = (ch4_toth[0], *fit_msl(CH4_data, ch4_toth[0], 0.5))

print(f"CO2 - qmax: {co2_msl[0]} (fixed), a: {co2_msl[1]}")
for T in T_vals:
    print(f"K_{T}: {co2_msl[2][T]}")
print(f"CH4 - qmax: {ch4_msl[0]} (fixed), a: {ch4_msl[1]}")
for T in T_vals:
    print(f"K_{T}: {ch4_msl[2][T]}")

print("\nHeat of Adsorption (van't Hoff):")
co2_toth_dH = vant_hoff_calc(co2_toth[2])
co2_msl_dH = vant_hoff_calc(co2_msl[2])
ch4_toth_dH = vant_hoff_calc(ch4_toth[2])
ch4_msl_dH = vant_hoff_calc(ch4_msl[2])

print(f"CO2 Toth: {co2_toth_dH} kJ/mol")
print(f"CO2 Multi-site: {co2_msl_dH} kJ/mol")
print(f"CH4 Toth: {ch4_toth_dH} kJ/mol")
print(f"CH4 Multi-site: {ch4_msl_dH} kJ/mol")
