# -*- coding: utf-8 -*-
"""Builds Tutorial2_Solutions.html - self-contained solution sheet (figures embedded)."""
import base64
import io
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tut2_data import CARBON, SILICA, CH4, CO2
from tut2_fit import langmuir, toth, msl

R = json.load(open("tut2_results.json"))
TS = [298, 308, 323]
COL = {298: "#2563eb", 308: "#ea580c", 323: "#16a34a"}

plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": .25,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": "white", "savefig.facecolor": "white"})


def png(fig):
    b = io.BytesIO()
    fig.savefig(b, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()


# --- fig 1: Q2 ---
fig, ax = plt.subplots(1, 2, figsize=(8.4, 3.1))
for a, (lab, key, data) in zip(ax, [("Activated carbon", "carbon", CARBON),
                                    ("Silica gel", "silica", SILICA)]):
    p = np.array([d[0] for d in data]); q = np.array([d[1] for d in data])
    r = R["Q2"][key]
    pp = np.linspace(0, p.max() * 1.05, 300)
    a.plot(p, q, "o", ms=5, mfc="none", color="#334155", label="experimental")
    a.plot(pp, langmuir(pp, r["qmax"], r["K"]), "-", lw=1.8, color="#dc2626",
           label="Langmuir fit")
    a.axhline(r["qmax"], ls=":", c="0.6", lw=1)
    a.set_title(f"CO$_2$ / {lab}   ($R^2$ = {r['R2']:.4f})", fontsize=9)
    a.set_xlabel("p  [mmHg]"); a.set_ylabel("q  [mmol/g]")
    a.legend(fontsize=7.5, loc="lower right")
fig.tight_layout()
F1 = png(fig)

# --- fig 2: Q3 isotherms ---
fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.2))
for ax_, gas, sets in zip(axes, ["CO2", "CH4"], [CO2, CH4]):
    t, m = R["Q3"][gas]["toth"], R["Q3"][gas]["msl"]
    for T in TS:
        p = np.array([d[0] for d in sets[T]]); q = np.array([d[1] for d in sets[T]])
        pp = np.linspace(1e-5, p.max() * 1.02, 250)
        ax_.plot(p, q, "o", ms=4, mfc="none", color=COL[T], label=f"{T} K")
        ax_.plot(pp, toth(pp, t["qmax"], t["K"][str(T)], t["n"]), "-", lw=1.5, color=COL[T])
        ax_.plot(pp, msl(pp, m["qmax"], m["K"][str(T)], m["a"]), "--", lw=1.1, color=COL[T])
    ax_.set_title(f"{'CO$_2$' if gas=='CO2' else 'CH$_4$'} on 13X  "
                  "(— Tóth,  -- multi-site)", fontsize=9)
    ax_.set_xlabel("P  [MPa]"); ax_.set_ylabel("q  [mol/kg]")
    ax_.legend(fontsize=7.5)
fig.tight_layout()
F2 = png(fig)

# --- fig 3: van 't Hoff ---
fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.1))
for ax_, gas in zip(axes, ["CO2", "CH4"]):
    for mk, key, lab in (("o", "vanthoff_toth", "Tóth"),
                         ("s", "vanthoff_msl", "multi-site Langmuir")):
        v = R["Q3"][gas][key]
        x = np.array(v["invT"]) * 1000
        y = np.array(v["lnK"])
        xx = np.linspace(x.min() * .998, x.max() * 1.002, 10)
        ax_.plot(x, y, mk, ms=6, mfc="none",
                 color="#dc2626" if mk == "o" else "#2563eb")
        ax_.plot(xx, v["slope"] * xx / 1000 + v["intercept"],
                 "-" if mk == "o" else "--", lw=1.4,
                 color="#dc2626" if mk == "o" else "#2563eb",
                 label=f"{lab}:  $\\Delta H$ = {v['dH_kJ']:.1f} kJ/mol")
    ax_.set_title(f"van 't Hoff — {'CO$_2$' if gas=='CO2' else 'CH$_4$'}", fontsize=9)
    ax_.set_xlabel("1000/T  [K$^{-1}$]"); ax_.set_ylabel("ln K")
    ax_.legend(fontsize=7.5)
fig.tight_layout()
F3 = png(fig)

# ------------------------------------------------------------------ HTML
q2c, q2s = R["Q2"]["carbon"], R["Q2"]["silica"]
g = lambda gas, mdl: R["Q3"][gas][mdl]


def q3row(gas, mdl, vh, sym):
    d, v = g(gas, mdl), g(gas, vh)
    return (f"<tr><td>{'CO₂' if gas=='CO2' else 'CH₄'}</td>"
            f"<td>{d['qmax']:.3f}</td><td>{d[sym]:.4f}</td>"
            + "".join(f"<td>{d['K'][str(T)]:.4g}</td>" for T in TS)
            + f"<td>{d['R2']:.5f}</td><td>{d['AARD']:.2f}</td>"
            f"<td><b>{v['dH_kJ']:.1f}</b></td></tr>")


HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CRE-II Tutorial 2 Solutions</title>
<style>
:root{{--bg:#ffffff;--fg:#1e2430;--mut:#5b6472;--line:#e2e6ec;--card:#f8fafc;
--accent:#b3261e;--accent2:#1d4ed8;--code:#f1f5f9;--th:#eef2f7;}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{
--bg:#12151b;--fg:#e6e9ef;--mut:#9aa4b2;--line:#2a303a;--card:#191d25;
--accent:#ff8a80;--accent2:#7aa2ff;--code:#1c212a;--th:#1e242e;}}}}
:root[data-theme="dark"]{{--bg:#12151b;--fg:#e6e9ef;--mut:#9aa4b2;--line:#2a303a;
--card:#191d25;--accent:#ff8a80;--accent2:#7aa2ff;--code:#1c212a;--th:#1e242e;}}
body{{background:var(--bg);color:var(--fg);margin:0;padding:2.2rem 1.2rem 4rem;
font:15px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;}}
main{{max-width:860px;margin:0 auto;}}
h1{{font-size:1.55rem;margin:0 0 .25rem;letter-spacing:-.01em;}}
.sub{{color:var(--mut);font-size:.9rem;margin:0 0 2rem;}}
h2{{font-size:1.18rem;margin:2.6rem 0 .8rem;padding-bottom:.4rem;
border-bottom:2px solid var(--accent);}}
h3{{font-size:1rem;margin:1.7rem 0 .5rem;color:var(--accent2);}}
p{{margin:.65rem 0;}}
.eq{{background:var(--card);border-left:3px solid var(--accent2);padding:.7rem 1rem;
margin:.9rem 0;overflow-x:auto;font-family:"Cambria Math",Cambria,Georgia,serif;
font-size:1.02rem;}}
.eq i,i.v{{font-family:"Cambria Math",Cambria,Georgia,serif;}}
sub,sup{{font-size:.72em;}}
.frac{{display:inline-block;vertical-align:middle;text-align:center;margin:0 .25em;}}
.frac>span{{display:block;padding:0 .35em;}}
.frac .den{{border-top:1px solid currentColor;}}
table{{border-collapse:collapse;width:100%;margin:.9rem 0;font-size:.86rem;}}
th,td{{border:1px solid var(--line);padding:.42rem .55rem;text-align:right;}}
th{{background:var(--th);font-weight:600;text-align:center;}}
td:first-child,th:first-child{{text-align:left;}}
.wrap{{overflow-x:auto;}}
figure{{margin:1.2rem 0;}}
img{{max-width:100%;height:auto;border:1px solid var(--line);border-radius:6px;}}
figcaption{{color:var(--mut);font-size:.8rem;margin-top:.4rem;}}
.note{{background:var(--card);border:1px solid var(--line);border-radius:8px;
padding:.85rem 1rem;margin:1.1rem 0;font-size:.89rem;}}
.note b{{color:var(--accent);}}
.ans{{background:var(--card);border-left:3px solid var(--accent);padding:.75rem 1rem;
margin:1rem 0;font-weight:600;}}
code{{background:var(--code);padding:.1rem .35rem;border-radius:4px;font-size:.86em;}}
ul{{margin:.5rem 0 .5rem 1.1rem;padding:0;}} li{{margin:.3rem 0;}}
.files{{display:flex;gap:.6rem;flex-wrap:wrap;margin:.8rem 0;}}
.files span{{background:var(--card);border:1px solid var(--line);border-radius:6px;
padding:.35rem .7rem;font-size:.82rem;font-family:ui-monospace,Menlo,Consolas,monospace;}}
.mut{{color:var(--mut);}}
</style>
</head>
<body>
<main>
<h1>Chemical Reaction Engineering II (CL24303) — Tutorial 2</h1>
<p class="sub">MO2026 · Solutions to Q1, Q2 and Q3 · adsorption equilibria</p>

<div class="files"><span>Tutorial2_Q2_Q3_Solutions.xlsx</span>
<span>Tutorial2_Q2_Q3_Solutions.ipynb</span></div>

<!-- ================= Q1 ================= -->
<h2>Q1 — Dissociative chemisorption of N₂ and H₂ on Fe</h2>

<p>Both gases dissociate on adsorption, so each molecule needs a <b>pair</b> of adjacent
vacant sites S:</p>

<div class="eq">
N<sub>2</sub> + 2S ⇌ 2 N·S &nbsp;&nbsp;&nbsp;&nbsp;
H<sub>2</sub> + 2S ⇌ 2 H·S
</div>

<p><b>Step 1 — equilibrium for each gas.</b> At equilibrium the rates of adsorption and
desorption are equal, so for nitrogen</p>

<div class="eq">
K<sub>N₂</sub> =
<span class="frac"><span>C<sub>N·S</sub><sup>2</sup></span>
<span class="den">p<sub>N₂</sub> C<sub>v</sub><sup>2</sup></span></span>
&nbsp;&nbsp;⟹&nbsp;&nbsp;
C<sub>N·S</sub> = C<sub>v</sub> √(K<sub>N₂</sub> p<sub>N₂</sub>)
</div>

<p>The square root is the fingerprint of dissociation — the surface concentration goes as
√p, not p. Identically for hydrogen:</p>

<div class="eq">
C<sub>H·S</sub> = C<sub>v</sub> √(K<sub>H₂</sub> p<sub>H₂</sub>)
</div>

<p><b>Step 2 — site balance.</b> Every dissociatively adsorbed molecule takes two sites out
of circulation, so the total site concentration C<sub>t</sub> is</p>

<div class="eq">
C<sub>t</sub> = C<sub>v</sub> + 2 C<sub>N·S</sub> + 2 C<sub>H·S</sub>
</div>

<p><b>Step 3 — eliminate C<sub>v</sub>.</b> Substituting the two equilibrium expressions,</p>

<div class="eq">
C<sub>t</sub> = C<sub>v</sub>[ 1 + 2√(K<sub>N₂</sub>p<sub>N₂</sub>) +
2√(K<sub>H₂</sub>p<sub>H₂</sub>) ]
&nbsp;&nbsp;⟹&nbsp;&nbsp;
C<sub>v</sub> =
<span class="frac"><span>C<sub>t</sub></span>
<span class="den">1 + 2√(K<sub>N₂</sub>p<sub>N₂</sub>) + 2√(K<sub>H₂</sub>p<sub>H₂</sub>)</span></span>
</div>

<p>and putting this back into C<sub>N·S</sub> = C<sub>v</sub>√(K<sub>N₂</sub>p<sub>N₂</sub>):</p>

<div class="ans">
C<sub>N·S</sub> =
<span class="frac"><span>C<sub>t</sub> √(K<sub>N₂</sub> p<sub>N₂</sub>)</span>
<span class="den">1 + 2√(K<sub>N₂</sub>p<sub>N₂</sub>) + 2√(K<sub>H₂</sub>p<sub>H₂</sub>)</span></span>
&nbsp;&nbsp;∎
</div>

<div class="note">
<b>Note on the factor 2.</b> The 2's come from Step 2, where each adsorbed species is
counted as blocking a <i>pair</i> of sites. If instead one books the site balance per
adsorbed <i>atom</i> (one N atom on one site), it reads
C<sub>t</sub> = C<sub>v</sub> + C<sub>N·S</sub> + C<sub>H·S</sub> and the 2's drop out.
Both conventions appear in the literature; the form asked for here is the dual-site one.
Either way the key physics is unchanged: <b>√p dependence</b>, and NH₃ synthesis is
inhibited by H₂ because adsorbed H competes for the sites N needs.
</div>

<!-- ================= Q2 ================= -->
<h2>Q2 — Langmuir isotherm for CO₂ at 25 °C</h2>

<div class="eq">
θ = <span class="frac"><span>q</span><span class="den">q<sub>max</sub></span></span> =
<span class="frac"><span>Kp</span><span class="den">1 + Kp</span></span>
&nbsp;&nbsp;⟹&nbsp;&nbsp;
q = <span class="frac"><span>q<sub>max</sub> K p</span><span class="den">1 + Kp</span></span>
</div>

<p><b>Method.</b> Two parameters fitted by minimising
SSE = Σ(q<sub>calc</sub> − q<sub>exp</sub>)² directly on the non-linear equation
(Excel → Data → Solver, GRG Nonlinear, <i>Min</i>, changing q<sub>max</sub> and K).
The starting guess is taken from the linearised form
p/q = 1/(q<sub>max</sub>K) + p/q<sub>max</sub>, whose slope gives 1/q<sub>max</sub>.
The linear fit is <i>only</i> a starting guess — it distorts the error weighting.</p>

<div class="wrap"><table>
<tr><th>Adsorbent</th><th>q<sub>max</sub> [mmol/g]</th><th>K [mmHg⁻¹]</th>
<th>R²</th><th>RMSE</th><th>AARD %</th></tr>
<tr><td>Activated carbon</td><td>{q2c['qmax']:.3f}</td><td>{q2c['K']:.5f}</td>
<td>{q2c['R2']:.4f}</td><td>{q2c['RMSE']:.4f}</td><td>{q2c['AARD']:.2f}</td></tr>
<tr><td>Silica gel</td><td>{q2s['qmax']:.3f}</td><td>{q2s['K']:.6f}</td>
<td>{q2s['R2']:.4f}</td><td>{q2s['RMSE']:.4f}</td><td>{q2s['AARD']:.2f}</td></tr>
</table></div>

<figure><img src="{F1}" alt="Langmuir fits for CO2 on activated carbon and silica gel">
<figcaption>Points: experimental. Line: Langmuir fit. Dotted line: fitted
q<sub>max</sub>.</figcaption></figure>

<p><b>Interpretation.</b></p>
<ul>
<li><b>Silica gel</b> — R² = {q2s['R2']:.4f}, residuals random. Langmuir works. But
Kp ≪ 1 over the whole range, so the data never approach saturation and q<sub>max</sub>
is a long extrapolation.</li>
<li><b>Activated carbon</b> — R² = {q2c['R2']:.3f} only, and the residuals are
<i>systematic</i> rather than random. Langmuir assumes one uniform site type; activated
carbon has a wide distribution of pore sizes and binding energies, so the real isotherm
rises faster at low p and flattens more slowly than a single-site Langmuir can. A
heterogeneous isotherm (Tóth / Freundlich / Sips) is needed — which is exactly what
Q3 uses.</li>
<li>Carbon binds CO₂ ≈ {q2c['K']/q2s['K']:.0f}× more strongly than silica
(K = {q2c['K']:.4f} vs {q2s['K']:.5f} mmHg⁻¹): at 100 mmHg the carbon is already
≈ {100*q2c['K']*100/(1+q2c['K']*100):.0f} % covered, the silica only
≈ {100*q2s['K']*100/(1+q2s['K']*100):.0f} %.</li>
</ul>

<!-- ================= Q3 ================= -->
<h2>Q3 — Tóth and multi-site Langmuir on zeolite 13X</h2>

<div class="eq">
<b>Tóth:</b>&nbsp;
<span class="frac"><span>q</span><span class="den">q<sub>max</sub></span></span> =
<span class="frac"><span>K p</span>
<span class="den">[ 1 + (K p)<sup>n</sup> ]<sup>1/n</sup></span></span>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<b>Multi-site Langmuir:</b>&nbsp;
<span class="frac"><span>q</span><span class="den">q<sub>max</sub></span></span> =
K p ( 1 − q/q<sub>max</sub> )<sup>a</sup>
</div>

<p>Both collapse to Langmuir at n = 1 / a = 1. Tóth's <i>n</i> measures surface
<b>heterogeneity</b> (n &lt; 1); the multi-site <i>a</i> is the number of sites one
molecule occupies.</p>

<h3>Fitting strategy (this is the part that matters)</h3>
<ul>
<li><b>All three temperatures are fitted together.</b> q<sub>max</sub>, n and a belong to
the adsorbent–adsorbate pair and are temperature-independent; all of the temperature
dependence sits in K. So one regression per gas: 5 parameters
(q<sub>max</sub>, n, K<sub>298</sub>, K<sub>308</sub>, K<sub>323</sub>) against all the
data. Fitting each isotherm separately would let q<sub>max</sub> drift with T and make the
van 't Hoff plot meaningless.</li>
<li><b>The multi-site model is implicit in q</b> — θ = Kp(1−θ)<sup>a</sup> cannot be
rearranged. But θ<sub>exp</sub> = q<sub>exp</sub>/q<sub>max</sub> is known, so
p<sub>calc</sub> = θ/[K(1−θ)<sup>a</sup>] <i>is</i> explicit. It is therefore regressed in
the pressure direction, minimising Σ(ln p<sub>calc</sub> − ln p<sub>exp</sub>)² — plain
Excel formulas, no iteration. The p = 0 point is dropped (ln 0).</li>
<li><b>q<sub>max</sub> and a are strongly correlated</b> in the multi-site model — turned
loose, Solver walks a past 20 with an equally unphysical q<sub>max</sub>. q<sub>max</sub>
is therefore <b>fixed at the Tóth value</b>: the same gas on the same zeolite must saturate
at the same loading. Only a and the three K are regressed.</li>
</ul>

<h3>Results</h3>
<p class="mut" style="font-size:.85rem;margin-bottom:.2rem">Tóth
&nbsp;·&nbsp; K in MPa⁻¹, q<sub>max</sub> in mol/kg</p>
<div class="wrap"><table>
<tr><th>Gas</th><th>q<sub>max</sub></th><th>n</th><th>K<sub>298</sub></th>
<th>K<sub>308</sub></th><th>K<sub>323</sub></th><th>R²</th><th>AARD %</th>
<th>ΔH<sub>ads</sub> [kJ/mol]</th></tr>
{q3row('CO2','toth','vanthoff_toth','n')}
{q3row('CH4','toth','vanthoff_toth','n')}
</table></div>

<p class="mut" style="font-size:.85rem;margin-bottom:.2rem">Multi-site Langmuir
&nbsp;·&nbsp; q<sub>max</sub> fixed at the Tóth value</p>
<div class="wrap"><table>
<tr><th>Gas</th><th>q<sub>max</sub></th><th>a</th><th>K<sub>298</sub></th>
<th>K<sub>308</sub></th><th>K<sub>323</sub></th><th>R²</th><th>AARD %</th>
<th>ΔH<sub>ads</sub> [kJ/mol]</th></tr>
{q3row('CO2','msl','vanthoff_msl','a')}
{q3row('CH4','msl','vanthoff_msl','a')}
</table></div>

<figure><img src="{F2}" alt="Toth and multi-site Langmuir fits on zeolite 13X">
<figcaption>Both models track all three isotherms with R² &gt; 0.995.</figcaption></figure>

<h3>ΔH<sub>ads</sub> from the van 't Hoff plot</h3>

<div class="eq">
K = K<sub>0</sub> exp( −ΔH<sub>ads</sub> / RT )
&nbsp;&nbsp;⟹&nbsp;&nbsp;
ln K = ln K<sub>0</sub> −
<span class="frac"><span>ΔH<sub>ads</sub></span><span class="den">R</span></span>
·<span class="frac"><span>1</span><span class="den">T</span></span>
</div>

<p>A straight line of ln K against 1/T has <b>slope = −ΔH<sub>ads</sub>/R</b>, so
ΔH<sub>ads</sub> = −R × slope (Excel: <code>=SLOPE(lnK, 1/T)</code>).</p>

<figure><img src="{F3}" alt="van 't Hoff plots for CO2 and CH4 on zeolite 13X">
<figcaption>Three temperatures, two parameters — a high R² here confirms consistency
rather than proving it.</figcaption></figure>

<div class="ans">
ΔH<sub>ads</sub> (CO₂) ≈ −{abs(g('CO2','vanthoff_toth')['dH_kJ']):.0f} to
−{abs(g('CO2','vanthoff_msl')['dH_kJ']):.0f} kJ/mol&nbsp;&nbsp;·&nbsp;&nbsp;
ΔH<sub>ads</sub> (CH₄) ≈ −{abs(g('CH4','vanthoff_toth')['dH_kJ']):.0f} kJ/mol
</div>

<h3>What the numbers say</h3>
<ul>
<li><b>Tóth n.</b> n(CO₂) = {g('CO2','toth')['n']:.2f} is far below 1 — CO₂ sees a very
heterogeneous surface, because it binds first to the strong, few extra-framework Na⁺
cations and only then to the rest of the cage. n(CH₄) = {g('CH4','toth')['n']:.2f} is much
closer to 1: non-polar CH₄ has no preferred cation site, so the surface looks nearly
uniform to it.</li>
<li><b>Multi-site a.</b> a(CO₂) = {g('CO2','msl')['a']:.1f} vs
a(CH₄) = {g('CH4','msl')['a']:.1f} — the linear, quadrupolar CO₂ effectively ties up
several sites, CH₄ behaves as a small compact adsorbate. (Since q<sub>max</sub> was pinned
to make <i>a</i> identifiable, read it as a shape parameter, not a literal site count.)</li>
<li><b>Both models agree on ΔH<sub>ads</sub> to within a few percent</b> — that agreement,
not the R² of either fit alone, is the real evidence the number is physical and not an
artefact of one equation.</li>
<li><b>Why 13X separates CO₂ from CH₄.</b> |ΔH<sub>ads</sub>| for CO₂ is
≈ {g('CO2','vanthoff_toth')['dH_kJ']/g('CH4','vanthoff_toth')['dH_kJ']:.1f}× that of CH₄:
the CO₂ quadrupole couples strongly to the electric field of the Na⁺ cations, CH₄ only
through weak dispersion. Hence 13X for biogas upgrading and natural-gas sweetening in
PSA/TSA cycles. The large |ΔH| for CO₂ also means the bed heats up noticeably on
adsorption — which is why a real adsorber is modelled non-isothermally.</li>
<li>Both ΔH are negative: adsorption is exothermic, so loading falls as T rises — exactly
what the three isotherms show.</li>
</ul>

<div class="note">
<b>Running the Solver yourself.</b> In the workbook, yellow cells are the decision
variables and the green cell is the objective. Data → Solver → Set Objective = green cell,
To: <i>Min</i>, By Changing = yellow cells, Method = <b>GRG Nonlinear</b>, tick
"Make Unconstrained Variables Non-Negative", Solve. Every sheet is already at the converged
optimum, so Solver should return immediately without moving the parameters.
</div>

</main>
</body>
</html>
"""

open("Tutorial2_Solutions.html", "w", encoding="utf-8").write(HTML)
print("wrote Tutorial2_Solutions.html (%.0f KB)" % (len(HTML) / 1024))
