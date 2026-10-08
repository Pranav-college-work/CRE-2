import numpy as np
from scipy.optimize import least_squares

# carbon aur silica ka data
p_carbon = np.array([15.7, 44.0, 54.2, 84.0, 107.0, 139.0, 177.0, 215.5, 278.0, 331.5, 429.5, 536.0, 585.7, 640.7, 680.2])
q_carbon = np.array([0.791, 1.141, 1.223, 1.416, 1.532, 1.646, 1.769, 1.872, 2.006, 2.105, 2.254, 2.373, 2.454, 2.479, 2.51])

p_silica = np.array([11.1, 25.0, 43.5, 71.4, 100.0, 158.9, 227.5, 304.2, 387.0, 468.0, 569.0, 677.8, 775.0])
q_silica = np.array([0.0564, 0.1252, 0.198, 0.2986, 0.385, 0.5441, 0.702, 0.843, 1.01, 1.138, 1.288, 1.434, 1.562])

# langmuir equation
def langmuir(p, qmax, K):
    return qmax * K * p / (1 + K * p)

# goodness of fit calculate
def calc_gof(q_exp, q_calc):
    res = q_calc - q_exp
    sse = np.sum(res**2)
    sst = np.sum((q_exp - np.mean(q_exp))**2)
    r2 = 1 - (sse / sst)
    rmse = np.sqrt(sse / len(q_exp))

    # aard sirf non-zero points ke liye
    err_rel = np.abs(res[q_exp > 0] / q_exp[q_exp > 0])
    aard = 100 * np.mean(err_rel)

    return {'SSE': sse, 'R2': r2, 'RMSE': rmse, 'AARD_%': aard}

# fitting function
def fit_lang(p, q):
    # linear guess from p/q vs p
    pq = p / q
    m, c = np.polyfit(p, pq, 1)

    qmax_guess = 1 / m
    K_guess = m / c

    # least squares fit
    def res(x):
        return langmuir(p, x[0], x[1]) - q

    sol = least_squares(res, [qmax_guess, K_guess], bounds=(0, np.inf))
    return sol.x

# carbon fit
params_c = fit_lang(p_carbon, q_carbon)
q_calc_c = langmuir(p_carbon, params_c[0], params_c[1])
gof_c = calc_gof(q_carbon, q_calc_c)

print("Activated Carbon (CO2 at 25°C)")
print(f"qmax = {params_c[0]} mmol/g")
print(f"K = {params_c[1]} 1/mmHg")
print(f"R² = {gof_c['R2']}")
print(f"AARD = {gof_c['AARD_%']}%\n")

# silica fit
params_s = fit_lang(p_silica, q_silica)
q_calc_s = langmuir(p_silica, params_s[0], params_s[1])
gof_s = calc_gof(q_silica, q_calc_s)

print("Silica Gel (CO2 at 25°C)")
print(f"qmax = {params_s[0]} mmol/g")
print(f"K = {params_s[1]} 1/mmHg")
print(f"R² = {gof_s['R2']}")
print(f"AARD = {gof_s['AARD_%']}%")
