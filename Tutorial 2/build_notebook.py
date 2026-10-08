"""Builds Tutorial2_Q2_Q3_Solutions.ipynb - self-contained notebook for Q2 and Q3."""
import nbformat as nbf
from tut2_data import CARBON, SILICA, CH4, CO2

nb = nbf.v4.new_notebook()
C, M = [], []


def md(s):
    C.append(nbf.v4.new_markdown_cell(s.strip("\n")))


def code(s):
    C.append(nbf.v4.new_code_cell(s.strip("\n")))


md(r"""
# Tutorial 2 — CL24303 (CRE-II), MO2026
## Q2 & Q3 — Adsorption isotherm regression

| | |
|---|---|
| **Q2** | Langmuir isotherm for CO₂ on activated carbon and silica gel at 25 °C |
| **Q3** | Tóth and multi-site Langmuir isotherms for CO₂ and CH₄ on zeolite 13X at 298/308/323 K, then Δ*H*<sub>ads</sub> from a van 't Hoff plot |

Everything is non-linear least squares — the same objective Excel's Solver minimises,
here handed to `scipy.optimize.least_squares` (Trust-Region-Reflective), which is the
same class of gradient method as Solver's GRG Nonlinear.

Run top to bottom. Only `numpy`, `scipy`, `pandas` and `matplotlib` are needed.
""")

code("""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import least_squares, brentq

plt.rcParams.update({'figure.dpi': 110, 'font.size': 10, 'axes.grid': True,
                     'grid.alpha': 0.3, 'axes.spines.top': False, 'axes.spines.right': False})
R = 8.314  # J mol^-1 K^-1
np.set_printoptions(suppress=True)
""")

md(r"""
### A single goodness-of-fit helper

$$\mathrm{SSE}=\sum_i (q_{\text{calc},i}-q_{\exp,i})^2,\qquad
R^2 = 1-\frac{\mathrm{SSE}}{\mathrm{SST}},\qquad
\mathrm{AARD}=\frac{100}{N}\sum_i\left|\frac{q_{\text{calc},i}-q_{\exp,i}}{q_{\exp,i}}\right|$$
""")

code("""
def gof(q_exp, q_calc, npar=0):
    \"\"\"Goodness of fit. Relative error skips q_exp = 0 points.\"\"\"
    q_exp, q_calc = np.asarray(q_exp, float), np.asarray(q_calc, float)
    res = q_calc - q_exp
    sse = float(res @ res)
    nz = q_exp > 0
    return {'SSE': sse,
            'R2': 1 - sse / float(((q_exp - q_exp.mean())**2).sum()),
            'RMSE': float(np.sqrt(sse / q_exp.size)),
            'AARD_%': float(100 * np.mean(np.abs(res[nz] / q_exp[nz])))}
""")

# ------------------------------------------------------------------ Q2
md(r"""
---
# Q2 — Langmuir isotherm

$$\theta=\frac{q}{q_{max}}=\frac{Kp}{1+Kp}\qquad\Longrightarrow\qquad q=\frac{q_{max}Kp}{1+Kp}$$

Two parameters, $q_{max}$ and $K$, fitted by minimising SSE in $q$.

**Initial guess** comes from the linearised form $\dfrac{p}{q}=\dfrac{1}{q_{max}K}+\dfrac{p}{q_{max}}$,
so a straight line of $p/q$ vs $p$ gives $q_{max}=1/\text{slope}$ and $K=\text{slope}/\text{intercept}$.
The linearisation is only a *starting point* — it weights the low-pressure points wrongly,
so the final answer is the non-linear fit.
""")

code("""
# CO2 adsorption at 25 C, JACS (1950) 72(3) 1153-1157.  p [mmHg], q [mmol/g]
carbon = np.array(__CARBON__).T
silica = np.array(__SILICA__).T
p_c, q_c = carbon
p_s, q_s = silica
print(f'activated carbon: {p_c.size} points,  silica: {p_s.size} points')
""".replace("__CARBON__", repr([list(t) for t in CARBON]))
   .replace("__SILICA__", repr([list(t) for t in SILICA])))

code("""
def langmuir(p, qmax, K):
    return qmax * K * p / (1 + K * p)

def fit_langmuir(p, q):
    # linear guess:  p/q = 1/(qmax*K) + p/qmax
    slope, intercept = np.polyfit(p, p / q, 1)
    guess = [1 / slope, slope / intercept]
    sol = least_squares(lambda x: langmuir(p, *x) - q, guess, bounds=(0, np.inf))
    return sol.x, guess

rows = []
fits = {}
for name, (p, q) in {'Activated carbon': (p_c, q_c), 'Silica gel': (p_s, q_s)}.items():
    (qmax, K), guess = fit_langmuir(p, q)
    fits[name] = (qmax, K)
    rows.append({'adsorbent': name, 'qmax [mmol/g]': qmax, 'K [1/mmHg]': K,
                 'qmax linear guess': guess[0], 'K linear guess': guess[1],
                 **gof(q, langmuir(p, qmax, K), 2)})

q2 = pd.DataFrame(rows).set_index('adsorbent')
q2.round(6)
""")

code("""
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
for a, (name, (p, q)) in zip(ax, {'Activated carbon': (p_c, q_c), 'Silica gel': (p_s, q_s)}.items()):
    qmax, K = fits[name]
    pp = np.linspace(0, p.max() * 1.05, 400)
    a.plot(p, q, 'o', ms=5, mfc='none', label='experimental')
    a.plot(pp, langmuir(pp, qmax, K), '-', lw=1.8,
           label=f'Langmuir\\n$q_{{max}}$={qmax:.3f}, $K$={K:.5f}')
    a.axhline(qmax, ls=':', c='0.5', lw=1)
    a.set(xlabel='p  [mmHg]', ylabel='q  [mmol/g]', title=f'CO$_2$ on {name} (25 °C)')
    a.legend(fontsize=8, loc='lower right')
fig.tight_layout()
""")

code("""
# residual plot - shows *where* the model fails
fig, ax = plt.subplots(1, 2, figsize=(10, 3), sharey=False)
for a, (name, (p, q)) in zip(ax, {'Activated carbon': (p_c, q_c), 'Silica gel': (p_s, q_s)}.items()):
    qmax, K = fits[name]
    a.stem(p, langmuir(p, qmax, K) - q, basefmt=' ')
    a.axhline(0, c='k', lw=0.8)
    a.set(xlabel='p [mmHg]', ylabel='$q_{calc}-q_{exp}$', title=name)
fig.tight_layout()
""")

md(r"""
**Reading the Q2 result**

* **Silica gel** — $R^2\approx0.998$ and residuals scattered about zero: Langmuir is a
  genuinely good description. $Kp\ll1$ over the whole range, so the isotherm is still
  almost in its linear (Henry) region and $q_{max}$ is an extrapolation.
* **Activated carbon** — $R^2\approx0.948$ and the residuals are *systematic* (S-shaped,
  not random). Langmuir assumes one energetically uniform site type; activated carbon has a
  broad distribution of pore sizes and binding energies, so the real isotherm rises faster at
  low $p$ and flatter at high $p$ than any single-site Langmuir can. A heterogeneous form
  (Tóth, Freundlich, Sips) is required — which is exactly the motivation for Q3.
* Carbon binds CO₂ an order of magnitude more strongly ($K\approx0.0145$ vs
  $0.00137$ mmHg⁻¹) — at 100 mmHg the carbon is already ~59 % covered while the silica is
  only ~12 %.
""")

# ------------------------------------------------------------------ Q3
md(r"""
---
# Q3 — Tóth and multi-site Langmuir on zeolite 13X

$$\textbf{Tóth:}\quad \frac{q}{q_{max}}=\frac{Kp}{\left[1+(Kp)^{n}\right]^{1/n}}
\qquad\qquad
\textbf{Multi-site Langmuir:}\quad \frac{q}{q_{max}}=Kp\left(1-\frac{q}{q_{max}}\right)^{a}$$

Both reduce to Langmuir at $n=1$ / $a=1$. Tóth's $n$ measures surface *heterogeneity*
($n<1$); the multi-site $a$ is the number of adsorption sites one molecule occupies.

**Fitting strategy.** $q_{max}$, $n$ and $a$ describe the *adsorbent–adsorbate pair* and are
taken temperature-independent, while $K$ carries all the temperature dependence
($K=K_0e^{-\Delta H_{ads}/RT}$). So the three isotherms of one gas are fitted
**simultaneously** with shared $q_{max}, n$ (or $a$) and one $K$ per temperature —
5 parameters against ~60–90 points. Fitting each temperature independently would let
$q_{max}$ drift with $T$ and make the van 't Hoff plot meaningless.
""")

CH4_R = repr({k: [list(t) for t in v] for k, v in CH4.items()})
CO2_R = repr({k: [list(t) for t in v] for k, v in CO2.items()})

code("""
# J. Chem. Eng. Data 2004, 49, 1095-1101.  P [MPa], q [mol/kg]
T_list = [298, 308, 323]
CH4 = {T: np.array(v).T for T, v in __CH4__.items()}
CO2 = {T: np.array(v).T for T, v in __CO2__.items()}
gases = {'CO2': CO2, 'CH4': CH4}
for g, s in gases.items():
    print(g, {T: s[T].shape[1] for T in T_list})
""".replace("__CH4__", CH4_R).replace("__CO2__", CO2_R))

md("## Q3a — Tóth isotherm")

code("""
def toth(p, qmax, K, n):
    Kp = K * p
    return qmax * Kp / (1 + Kp**n)**(1 / n)

def fit_toth(sets):
    \"\"\"Simultaneous fit over all T:  x = [qmax, n, K_298, K_308, K_323].\"\"\"
    P = [sets[T][0] for T in T_list]
    Q = [sets[T][1] for T in T_list]

    def residual(x):
        qmax, n, Ks = x[0], x[1], x[2:]
        return np.concatenate([toth(P[i], qmax, Ks[i], n) - Q[i] for i in range(len(T_list))])

    guess = [max(q.max() for q in Q) * 1.15, 0.7] + [5.0] * len(T_list)
    lower = [0.0, 0.05] + [0.0] * len(T_list)
    sol = least_squares(residual, guess, bounds=(lower, np.inf), xtol=1e-14, ftol=1e-14)
    qmax, n, Ks = sol.x[0], sol.x[1], sol.x[2:]
    return qmax, n, dict(zip(T_list, Ks))

toth_par = {g: fit_toth(s) for g, s in gases.items()}
for g, (qmax, n, Ks) in toth_par.items():
    print(f'{g}:  qmax = {qmax:7.4f} mol/kg   n = {n:6.4f}   ' +
          '   '.join(f'K{T} = {Ks[T]:9.4f}' for T in T_list))
""")

md(r"""
## Q3b — Multi-site Langmuir

Two things make this model awkward, and both need a deliberate choice.

**1. It is implicit in $q$.** $\theta=Kp(1-\theta)^{a}$ cannot be rearranged for $\theta$.
Two ways out:

* solve $\theta-Kp(1-\theta)^a=0$ numerically for every point (Brent's method — done below
  for plotting and for the $R^2$), or
* note that $\theta_{\exp}=q_{\exp}/q_{max}$ is *known*, so
  $p_{calc}=\theta/[K(1-\theta)^{a}]$ is **explicit** — and regress in the pressure
  direction, minimising $\sum(\ln p_{calc}-\ln p_{\exp})^2$.

The second is what the Excel sheet does (plain cell formulas, no iteration), so it is used
here too. The two routes agree on $a$ and $K$ to within ~1 %.

**2. $q_{max}$ and $a$ are strongly correlated.** Data alone barely distinguish
"few sites, weakly held" from "many sites, strongly held" — turned loose, Solver walks $a$
off to 20+ with an equally unphysical $q_{max}$. So $q_{max}$ is **fixed at the Tóth
saturation capacity**: the same gas on the same zeolite must saturate at the same loading,
whichever equation is used to describe the approach to saturation. Only $a$ and the three
$K$ are regressed.
""")

code("""
def msl_theta(p, K, a):
    \"\"\"Solve theta = K p (1-theta)^a  for theta in [0,1), point by point.\"\"\"
    p = np.atleast_1d(np.asarray(p, float))
    out = np.zeros_like(p)
    for i, pi in enumerate(p):
        if pi > 0:
            out[i] = brentq(lambda t: t - K * pi * (1 - t)**a, 0.0, 1 - 1e-14, xtol=1e-14)
    return out

def msl(p, qmax, K, a):
    return qmax * msl_theta(p, K, a)

def fit_msl(sets, qmax, K0):
    \"\"\"Fit a and K_i in the pressure direction. qmax fixed; p = 0 dropped (ln 0).\"\"\"
    P = [sets[T][0][sets[T][0] > 0] for T in T_list]
    TH = [sets[T][1][sets[T][0] > 0] / qmax for T in T_list]

    def residual(x):
        a, Ks = x[0], x[1:]
        return np.concatenate([np.log(TH[i] / (Ks[i] * (1 - TH[i])**a)) - np.log(P[i])
                               for i in range(len(T_list))])

    best = None
    for a0 in (1.5, 2.5, 4.0, 6.0):            # multistart - the objective is not convex
        sol = least_squares(residual, [a0] + [K0] * len(T_list),
                            bounds=([1.0] + [1e-9] * len(T_list), np.inf),
                            xtol=1e-14, ftol=1e-14)
        if best is None or sol.cost < best.cost:
            best = sol
    return best.x[0], dict(zip(T_list, best.x[1:]))

msl_par = {}
for g, s in gases.items():
    qmax = toth_par[g][0]                       # fixed from the Toth fit
    a, Ks = fit_msl(s, qmax, K0=100.0 if g == 'CO2' else 0.5)
    msl_par[g] = (qmax, a, Ks)
    print(f'{g}:  qmax = {qmax:7.4f} mol/kg (fixed)   a = {a:6.4f}   ' +
          '   '.join(f'K{T} = {Ks[T]:9.4f}' for T in T_list))
""")

code("""
# goodness of fit of both models, in q, per temperature and overall
rows = []
for g, s in gases.items():
    qmT, n, KT = toth_par[g]
    qmM, a, KM = msl_par[g]
    for model, fn, pars in (('Toth', lambda p, T: toth(p, qmT, KT[T], n), None),
                            ('multi-site Langmuir', lambda p, T: msl(p, qmM, KM[T], a), None)):
        qe = np.concatenate([s[T][1] for T in T_list])
        qc = np.concatenate([fn(s[T][0], T) for T in T_list])
        r = {'gas': g, 'model': model, 'N': qe.size, **gof(qe, qc)}
        for T in T_list:
            r[f'R2 {T}K'] = gof(s[T][1], fn(s[T][0], T))['R2']
        rows.append(r)
pd.DataFrame(rows).set_index(['gas', 'model']).round(5)
""")

code("""
fig, axes = plt.subplots(2, 2, figsize=(10.5, 7))
colors = {298: 'tab:blue', 308: 'tab:orange', 323: 'tab:green'}
for row, g in enumerate(['CO2', 'CH4']):
    s = gases[g]
    qmT, n, KT = toth_par[g]
    qmM, a, KM = msl_par[g]
    for col, (lbl, fn) in enumerate([('Tóth', lambda p, T: toth(p, qmT, KT[T], n)),
                                     ('multi-site Langmuir', lambda p, T: msl(p, qmM, KM[T], a))]):
        ax = axes[row, col]
        for T in T_list:
            p, q = s[T]
            pp = np.linspace(1e-4, p.max() * 1.02, 300)
            ax.plot(p, q, 'o', ms=4.5, mfc='none', color=colors[T], label=f'{T} K')
            ax.plot(pp, fn(pp, T), '-', lw=1.6, color=colors[T])
        ax.set(xlabel='P [MPa]', ylabel='q [mol/kg]',
               title=f'{"CO$_2$" if g=="CO2" else "CH$_4$"} on 13X — {lbl}')
        ax.legend(fontsize=8)
fig.tight_layout()
""")

code("""
# log-pressure view: the low-pressure (Henry) region is where the models differ most
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.8))
for ax, g in zip(axes, ['CO2', 'CH4']):
    s = gases[g]
    qmT, n, KT = toth_par[g]
    qmM, a, KM = msl_par[g]
    for T in T_list:
        p, q = s[T]
        m = p > 0
        pp = np.logspace(np.log10(p[m].min()), np.log10(p.max()), 300)
        ax.semilogx(p[m], q[m], 'o', ms=4.5, mfc='none', color=colors[T], label=f'{T} K')
        ax.semilogx(pp, toth(pp, qmT, KT[T], n), '-', lw=1.5, color=colors[T])
        ax.semilogx(pp, msl(pp, qmM, KM[T], a), '--', lw=1.2, color=colors[T])
    ax.set(xlabel='P [MPa]', ylabel='q [mol/kg]',
           title=f'{"CO$_2$" if g=="CO2" else "CH$_4$"} — solid: Tóth, dashed: multi-site')
    ax.legend(fontsize=8)
fig.tight_layout()
""")

md(r"""
## Q3c — Heat of adsorption from the van 't Hoff plot

$$K = K_0\exp\!\left(-\frac{\Delta H_{ads}}{RT}\right)
\qquad\Longrightarrow\qquad
\ln K = \ln K_0 - \frac{\Delta H_{ads}}{R}\cdot\frac{1}{T}$$

A straight line of $\ln K$ against $1/T$ has **slope $=-\Delta H_{ads}/R$**, so
$\Delta H_{ads}=-R\times\text{slope}$. Three temperatures, two parameters — one degree of
freedom, so a high $R^2$ here confirms consistency rather than proving it.
""")

code("""
def vant_hoff(Ks):
    T = np.array(T_list, float)
    x, y = 1 / T, np.log([Ks[T_] for T_ in T_list])
    slope, intercept = np.polyfit(x, y, 1)
    r2 = 1 - ((y - (slope * x + intercept))**2).sum() / ((y - y.mean())**2).sum()
    return {'slope': slope, 'lnK0': intercept, 'K0': np.exp(intercept),
            'dH_ads [kJ/mol]': -slope * R / 1000, 'R2': r2, 'x': x, 'y': y}

vh = {}
rows = []
for g in gases:
    vh[(g, 'Toth')] = vant_hoff(toth_par[g][2])
    vh[(g, 'multi-site Langmuir')] = vant_hoff(msl_par[g][2])
for (g, m), v in vh.items():
    rows.append({'gas': g, 'model': m, 'slope [K]': v['slope'], 'K0 [1/MPa]': v['K0'],
                 'dH_ads [kJ/mol]': v['dH_ads [kJ/mol]'], 'R2': v['R2']})
pd.DataFrame(rows).set_index(['gas', 'model']).round(5)
""")

code("""
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.8))
for ax, g in zip(axes, ['CO2', 'CH4']):
    for m, style in (('Toth', 'o-'), ('multi-site Langmuir', 's--')):
        v = vh[(g, m)]
        xx = np.linspace(v['x'].min() * 0.999, v['x'].max() * 1.001, 10)
        ax.plot(v['x'] * 1000, v['y'], style[0], ms=6, mfc='none')
        ax.plot(xx * 1000, v['slope'] * xx + v['lnK0'], style[1:], lw=1.5,
                label=f"{m}:  $\\\\Delta H$ = {v['dH_ads [kJ/mol]']:.1f} kJ/mol")
    ax.set(xlabel='1000/T  [1/K]', ylabel='ln K',
           title=f'van \\'t Hoff — {"CO$_2$" if g=="CO2" else "CH$_4$"} on 13X')
    ax.legend(fontsize=8)
fig.tight_layout()
""")

md("## Final answers")

code("""
q2_out = q2[['qmax [mmol/g]', 'K [1/mmHg]', 'R2', 'AARD_%']].round(5)
print('Q2  Langmuir, CO2 at 25 C\\n')
print(q2_out.to_string(), '\\n')

print('Q3  zeolite 13X\\n')
out = []
for g in gases:
    qmT, n, KT = toth_par[g]
    qmM, a, KM = msl_par[g]
    out.append({'gas': g, 'model': 'Toth', 'qmax [mol/kg]': qmT, 'n or a': n,
                **{f'K{T}': KT[T] for T in T_list},
                'dH_ads [kJ/mol]': vh[(g, 'Toth')]['dH_ads [kJ/mol]']})
    out.append({'gas': g, 'model': 'multi-site Langmuir', 'qmax [mol/kg]': qmM, 'n or a': a,
                **{f'K{T}': KM[T] for T in T_list},
                'dH_ads [kJ/mol]': vh[(g, 'multi-site Langmuir')]['dH_ads [kJ/mol]']})
print(pd.DataFrame(out).set_index(['gas', 'model']).round(4).to_string())
""")

md(r"""
### What the numbers mean

**Tóth $n$.** $n_{CO_2}\approx0.24$ is far below 1 — CO₂ sees a very heterogeneous
energy landscape on 13X, because it binds to the extra-framework Na⁺ cations first
(strong, few) and to the rest of the cage afterwards (weak, many). $n_{CH_4}\approx0.61$ is
much closer to 1: non-polar CH₄ has no such preferred cation site, so the surface looks
comparatively uniform to it. This is precisely the heterogeneity that made plain Langmuir
fail on activated carbon in Q2.

**Multi-site $a$.** $a_{CH_4}\approx2.2$ against $a_{CO_2}\approx6.1$ — under this model
a CO₂ molecule ties up several sites, consistent with a linear quadrupolar molecule bridging
across cations, while CH₄ behaves nearly as a small compact adsorbate. (Remember $a$ was made
identifiable by pinning $q_{max}$; its absolute value should be read as a shape parameter,
not literally counted.)

**Δ$H_{ads}$.** Both models agree: about **−65 to −68 kJ/mol for CO₂** and
**−16 kJ/mol for CH₄** — the model choice changes the value by only a few per cent, which is
the real check that the fit is physically meaningful and not an artefact of one equation.
Both are negative: adsorption is exothermic, so loading falls as temperature rises, exactly
as the three isotherms show.

The four-fold difference in $|\Delta H_{ads}|$ is the whole basis of the separation:
CO₂'s quadrupole interacts strongly with the electric field of the Na⁺ cations in 13X,
CH₄ only through weak dispersion. This is why zeolite 13X is used for CO₂/CH₄ separation
(biogas upgrading, natural-gas sweetening) in PSA/TSA cycles — and the large $|\Delta H|$
for CO₂ is also why the bed heats up appreciably on adsorption, which is what a
non-isothermal adsorber model has to account for.

Both models fit the data well ($R^2>0.995$ throughout). Tóth is the better description of
CO₂ and is easier to use since it is explicit in $q$; the multi-site Langmuir has the
advantage of a thermodynamically consistent multicomponent extension.
""")

nb["cells"] = C
nb.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
               "language_info": {"name": "python", "version": "3"}}
nbf.write(nb, "Tutorial2_Q2_Q3_Solutions.ipynb")
print("wrote Tutorial2_Q2_Q3_Solutions.ipynb")
