"""Tutorial 2 - non-linear regression for Q2 and Q3. Writes tut2_results.json."""
import json
import numpy as np
from scipy.optimize import least_squares, brentq
from tut2_data import CARBON, SILICA, CH4, CO2

R = 8.314  # J/mol/K


def stats(q, qh, npar):
    res = q - qh
    sse = float(res @ res)
    sst = float(((q - q.mean()) ** 2).sum())
    n = len(q)
    return dict(SSE=sse, R2=1 - sse / sst, RMSE=float(np.sqrt(sse / n)),
                AARD=float(100 * np.mean(np.abs(res[q > 0] / q[q > 0]))), Npts=n, npar=npar)


# ---------------- Q2: single-site Langmuir ----------------
def langmuir(p, qmax, K):
    return qmax * K * p / (1 + K * p)


def fit_langmuir(data):
    p = np.array([d[0] for d in data]); q = np.array([d[1] for d in data])
    # linearised p/q = 1/(qmax*K) + p/qmax  -> initial guess
    A = np.vstack([np.ones_like(p), p]).T
    c = np.linalg.lstsq(A, p / q, rcond=None)[0]
    x0 = [1 / c[1], c[1] / c[0]]
    sol = least_squares(lambda x: langmuir(p, *x) - q, x0, bounds=([0, 0], [np.inf, np.inf]))
    qmax, K = sol.x
    return dict(qmax=float(qmax), K=float(K), lin_qmax=float(x0[0]), lin_K=float(x0[1]),
                **stats(q, langmuir(p, qmax, K), 2))


# ---------------- Q3: Toth ----------------
def toth(p, qmax, K, n):
    Kp = K * p
    return qmax * Kp / (1 + Kp ** n) ** (1 / n)


def fit_toth(temps, sets):
    """Global fit: qmax, n shared; K_i per temperature."""
    P = [np.array([d[0] for d in sets[T]]) for T in temps]
    Q = [np.array([d[1] for d in sets[T]]) for T in temps]
    qm0 = max(q.max() for q in Q) * 1.15

    def resid(x):
        qmax, n = x[0], x[1]
        return np.concatenate([toth(P[i], qmax, x[2 + i], n) - Q[i] for i in range(len(temps))])

    x0 = [qm0, 0.7] + [5.0] * len(temps)
    lo = [0, 0.05] + [0] * len(temps)
    sol = least_squares(resid, x0, bounds=(lo, np.inf), xtol=1e-14, ftol=1e-14)
    qmax, n = sol.x[0], sol.x[1]
    Ks = [float(v) for v in sol.x[2:]]
    qall = np.concatenate(Q)
    qhat = np.concatenate([toth(P[i], qmax, Ks[i], n) for i in range(len(temps))])
    per = {int(T): stats(Q[i], toth(P[i], qmax, Ks[i], n), 0) for i, T in enumerate(temps)}
    return dict(qmax=float(qmax), n=float(n), K={int(T): Ks[i] for i, T in enumerate(temps)},
                per_T=per, **stats(qall, qhat, 2 + len(temps)))


# ---------------- Q3: multi-site Langmuir (implicit) ----------------
def msl_theta(p, K, a):
    """Solve theta = K p (1-theta)^a for theta in [0,1)."""
    out = np.empty_like(p, dtype=float)
    for i, pi in enumerate(np.atleast_1d(p)):
        if pi <= 0:
            out[i] = 0.0
            continue
        f = lambda t: t - K * pi * (1 - t) ** a
        out[i] = brentq(f, 0.0, 1.0 - 1e-14, xtol=1e-14, rtol=8.9e-16)
    return out


def msl(p, qmax, K, a):
    return qmax * msl_theta(p, K, a)


def fit_msl(temps, sets, qmax_fixed, K0=5.0):
    """Multi-site Langmuir, global fit: a shared, K_i per temperature, qmax fixed.

    Two modelling choices, both needed to make this fit well posed:

    1. qmax and a are strongly correlated - the pair is only weakly identified by
       isotherm data alone and an unconstrained Solver run drifts to unphysically
       large a.  qmax is therefore fixed at the saturation capacity from the Toth
       fit (the same pair must saturate at the same loading) and only a and the
       three K_i are regressed.
    2. The model is implicit in q, so it is regressed in the pressure direction:
       with theta = q_exp/qmax known, p_calc = theta / (K (1-theta)^a) is explicit,
       and we minimise sum (ln p_calc - ln p_exp)^2.  This is exactly what the
       Excel sheet does.  (A q-direction fit, solving the implicit equation
       numerically, gives the same a and K to within ~1%.)
    """
    qmax = float(qmax_fixed)
    P = [np.array([d[0] for d in sets[T]])[1:] for T in temps]   # drop the p=0 point
    Q = [np.array([d[1] for d in sets[T]])[1:] for T in temps]
    TH = [q / qmax for q in Q]

    def resid(x):
        a = x[0]
        return np.concatenate([np.log(TH[i] / (x[1 + i] * (1 - TH[i]) ** a)) - np.log(P[i])
                               for i in range(len(temps))])

    best = None
    for a0 in (1.5, 2.5, 4.0, 6.0):
        try:
            sol = least_squares(resid, [a0] + [K0] * len(temps),
                                bounds=([1.0] + [1e-9] * len(temps), np.inf),
                                xtol=1e-14, ftol=1e-14)
        except Exception:
            continue
        if best is None or sol.cost < best.cost:
            best = sol
    a = float(best.x[0])
    Ks = [float(v) for v in best.x[1:]]
    # goodness of fit reported in the q direction, for comparison with Toth
    Pf = [np.array([d[0] for d in sets[T]]) for T in temps]
    Qf = [np.array([d[1] for d in sets[T]]) for T in temps]
    qall = np.concatenate(Qf)
    qhat = np.concatenate([msl(Pf[i], qmax, Ks[i], a) for i in range(len(temps))])
    per = {int(T): stats(Qf[i], msl(Pf[i], qmax, Ks[i], a), 0) for i, T in enumerate(temps)}
    return dict(qmax=qmax, a=a, K={int(T): Ks[i] for i, T in enumerate(temps)},
                per_T=per, **stats(qall, qhat, 1 + len(temps)))


# ---------------- van 't Hoff ----------------
def vant_hoff(Kdict):
    T = np.array(sorted(Kdict), dtype=float)
    K = np.array([Kdict[int(t)] for t in T])
    x, y = 1 / T, np.log(K)
    m, c = np.polyfit(x, y, 1)
    yh = m * x + c
    r2 = 1 - ((y - yh) ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return dict(slope=float(m), intercept=float(c), R2=float(r2),
                dH_kJ=float(-m * R / 1000), K0=float(np.exp(c)),
                invT=[float(v) for v in x], lnK=[float(v) for v in y])


if __name__ == "__main__":
    Ts = [298, 308, 323]
    out = {
        "Q2": {"carbon": fit_langmuir(CARBON), "silica": fit_langmuir(SILICA)},
        "Q3": {},
    }
    for name, sets in (("CO2", CO2), ("CH4", CH4)):
        t = fit_toth(Ts, sets)
        m = fit_msl(Ts, sets, t["qmax"], K0=100.0 if name == "CO2" else 0.5)
        out["Q3"][name] = {
            "toth": t, "msl": m,
            "vanthoff_toth": vant_hoff(t["K"]),
            "vanthoff_msl": vant_hoff(m["K"]),
        }
    with open("tut2_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
