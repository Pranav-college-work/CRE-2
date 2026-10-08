from pathlib import Path
import base64
import html

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent.parent / 'Tutorial 4' / 'Tutorial4_Solutions.html'
code = (ROOT / 'tutorial4_code.py').read_text(encoding='utf-8')

def figure(name, caption):
    data = base64.b64encode((ROOT/name).read_bytes()).decode()
    return f'<figure><img src="data:image/svg+xml;base64,{data}" alt="{html.escape(caption)}"><figcaption>{caption} <a download="{name}" href="data:image/svg+xml;base64,{data}">Download SVG</a></figcaption></figure>'

page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tutorial 4 | Worked solutions | CRE II</title>
<style>
:root{--paper:#f7f5ef;--ink:#1d3038;--muted:#52666e;--teal:#126e82;--line:#d5ddd9;--wash:#eaf2f1;--amber:#a35a16}*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:78px}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.75 'Segoe UI',Arial,sans-serif}header{max-width:1120px;margin:auto;padding:64px 36px 38px;border-bottom:1px solid var(--line)}.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.15em;font-weight:700;color:var(--teal)}h1{font-family:Georgia,serif;font-size:clamp(38px,6vw,68px);line-height:1.05;font-weight:400;margin:18px 0}header p{max-width:730px;color:var(--muted);font-size:19px}.meta{font-size:13px;color:var(--muted)}nav{position:sticky;top:0;z-index:3;background:#f7f5eff5;border-bottom:1px solid var(--line);padding:12px 20px;text-align:center;backdrop-filter:blur(10px)}nav a{display:inline-block;padding:3px 10px;text-decoration:none;font-weight:600;font-size:14px}a{color:var(--teal)}main{max-width:1060px;margin:auto;padding:12px 30px 70px}section{padding:32px 0;border-bottom:1px solid var(--line)}h2{font:400 clamp(26px,4vw,36px)/1.2 Georgia,serif;margin:10px 0 24px}h2 .num{display:block;font:700 12px/2 'Segoe UI',sans-serif;color:var(--teal);letter-spacing:.15em;text-transform:uppercase}h3{font-size:19px;margin:28px 0 9px}p{margin:12px 0}.given{color:var(--muted);font-size:15px}.eq{background:white;border:1px solid var(--line);border-left:3px solid var(--teal);padding:15px 20px;margin:16px 0;font:19px/1.9 Cambria,Georgia,serif;overflow-x:auto}.result,.note{padding:17px 21px;margin:18px 0;background:var(--wash);border-left:3px solid var(--teal)}.note{background:#fff3df;border-color:var(--amber)}.result strong{color:#07596b}sub,sup{line-height:0}.table-wrap{overflow-x:auto;margin:18px 0}table{border-collapse:collapse;width:100%;font-size:15px;background:#fff}td,th{padding:12px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{background:#eaf0ed;font-weight:600}td:first-child{font-weight:500}.small,figcaption{font-size:13px;color:var(--muted)}figure{margin:24px 0;padding:15px;background:#fff;border:1px solid var(--line)}figure img{width:100%;height:auto;display:block}figcaption{padding-top:10px}figcaption a{float:right;margin-left:10px}details{margin:20px 0;background:white;border:1px solid var(--line);padding:14px 18px}summary{cursor:pointer;font-weight:650}pre{font:13px/1.65 Consolas,monospace;overflow:auto;background:#152a34;color:#eaf3f4;padding:22px;tab-size:4}code{font-family:Consolas,monospace}button,.button{display:inline-block;font:600 14px 'Segoe UI',sans-serif;border:1px solid var(--teal);background:var(--teal);color:#fff;padding:10px 15px;border-radius:3px;cursor:pointer;text-decoration:none}button.secondary{background:transparent;color:var(--teal)}input{font:inherit;padding:8px;border:1px solid #7d9299;border-radius:3px;max-width:170px}.tools{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:20px 0}footer{padding:30px 0;color:var(--muted);font-size:13px}.two{display:grid;grid-template-columns:1fr 1fr;gap:18px}.two .result{margin:0}.toclist{columns:2;list-style:none;padding:0}.toclist li{margin:6px 0}li{margin:7px 0}#k-output{display:block;margin-top:12px;font-weight:600}a:focus-visible,button:focus-visible,summary:focus-visible,input:focus-visible{outline:3px solid #bb5a2a;outline-offset:3px}
@media(max-width:650px){body{font-size:16px}header{padding:36px 20px 24px}main{padding:10px 18px 40px}nav{padding:7px}nav a{padding:4px 7px;font-size:13px}.two{grid-template-columns:1fr}.toclist{columns:1}.eq{font-size:17px;padding:12px}figure{padding:5px}figcaption a{float:none;display:block;margin:5px 0}td,th{padding:9px}h2{font-size:28px}}
@media print{body{background:white;font-size:11pt}header,main{max-width:none;padding:12px 0}header{padding-bottom:20px}h1{font-size:36pt}nav,.tools,.interactive,figcaption a{display:none}section{padding:18px 0}.eq,.result,.note,figure,tr{break-inside:avoid}h2,h3{break-after:avoid}figure{padding:0}a{color:inherit}pre{white-space:pre-wrap;background:#eee;color:#111;font-size:8pt}details{border:none;padding:0}summary{display:none}details:not([open]){display:none}}
</style></head><body>
<header><div class="eyebrow">Chemical Reaction Engineering II · CL24303 · MO2026</div>
<h1>Tutorial 4<br>Worked solutions</h1><p>Diffusion through catalyst pores, effectiveness factors, and the effect of pellet size on conversion.</p>
<div class="meta">Assigned 25 September 2026 · Due 4 October 2026, 23:59 · All eight questions</div>
<div class="tools"><button onclick="window.print()">Print / save as PDF</button><a class="button" href="Tutorial%204_CL24303_MO26.pdf">Open question sheet</a></div></header>
<nav aria-label="Question navigation"><a href="#overview">Overview</a><a href="#q1">Q1</a><a href="#q2">Q2</a><a href="#q3">Q3</a><a href="#q4">Q4</a><a href="#q5">Q5</a><a href="#q6">Q6</a><a href="#q7">Q7</a><a href="#q8">Q8</a><a href="#code">Python</a></nav>
<main>
<section id="overview"><h2>Before you start</h2><p>Rates of disappearance are written as positive quantities. Unless stated otherwise, assume steady state, isothermal pellets, uniform catalyst activity and constant effective diffusivity. The spherical-pellet calculations use the pellet radius <i>R</i>, not its diameter.</p>
<div class="note"><b>Two details in the question sheet matter.</b> Q3 does not give a reactant concentration; its two rates can still be compared if the runs have the same temperature and surface concentration. Q4 omits <i>k</i> and combines incompatible Thiele-modulus conventions. Its answers are therefore given as functions of <i>k</i>, with the convention corrected explicitly.</div>
<div class="table-wrap"><table><thead><tr><th>Symbol</th><th>Meaning and convention</th></tr></thead><tbody>
<tr><td>q<sub>m</sub>, q<sub>v</sub></td><td>Observed rate per catalyst mass and per pellet volume; q<sub>v</sub> = ρ<sub>p</sub>q<sub>m</sub>.</td></tr>
<tr><td>C<sub>As</sub>, C<sub>Ab</sub></td><td>Reactant concentration at the pellet surface and in the bulk fluid.</td></tr>
<tr><td>Φ = R√(k/D<sub>e</sub>)</td><td>Radius-based spherical Thiele modulus, used in Q3–Q4.</td></tr>
<tr><td>φ = (V<sub>p</sub>/S<sub>p</sub>)√(k/D<sub>e</sub>)</td><td>Volume-to-external-area convention in Q8: φ = Φ/3 for a sphere. For a flat slab, V<sub>p</sub>/S<sub>p</sub> = L, its half-thickness.</td></tr>
<tr><td>η</td><td>Actual internal reaction rate divided by the rate if the entire pellet were at C<sub>As</sub>.</td></tr></tbody></table></div></section>

<section id="q1"><h2><span class="num">Question 01</span>Bulk, Knudsen and effective diffusivity</h2>
<p class="given">Given: pore radius r = 50 Å, T = 100 °C, p = 1 or 10 atm; ε = 0.4, σ = 0.8, τ = 4.</p>
<h3>(a) Convert units and calculate both diffusivities</h3>
<div class="eq">r = 50 × 10<sup>−8</sup> = 5.0 × 10<sup>−7</sup> cm; &nbsp; T = 373.15 K<br>D<sub>AB</sub> = 0.86/p &nbsp; cm² s<sup>−1</sup><br>D<sub>K,H₂</sub> = 9.70 × 10³(5.0 × 10<sup>−7</sup>)√(373.15/2.016)<br>= 0.0659839 cm² s<sup>−1</sup></div>
<p>The molecular mass is M<sub>H₂</sub> = 2.016 g mol<sup>−1</sup>. Knudsen diffusivity is independent of pressure in the supplied correlation, because transport is controlled by collisions with the pore walls.</p>
<h3>(b) Combine the two resistances</h3><div class="eq">1/D<sub>H₂</sub> = 1/D<sub>AB</sub> + 1/D<sub>K</sub><br>D<sub>H₂</sub> = D<sub>AB</sub>D<sub>K</sub> / (D<sub>AB</sub> + D<sub>K</sub>)</div>
<h3>(c) Apply the pellet structure correction</h3><div class="eq">D<sub>e</sub> = D<sub>H₂</sub> εσ/τ = D<sub>H₂</sub>(0.4 × 0.8/4) = 0.08D<sub>H₂</sub></div>
<div class="table-wrap"><table><thead><tr><th>Pressure</th><th>D<sub>AB</sub></th><th>D<sub>K</sub></th><th>D<sub>H₂</sub></th><th>D<sub>e</sub></th></tr></thead><tbody>
<tr><td>1 atm</td><td>0.860</td><td>0.065984</td><td>0.061282</td><td><b>0.0049026</b></td></tr><tr><td>10 atm</td><td>0.0860</td><td>0.065984</td><td>0.037337</td><td><b>0.0029870</b></td></tr></tbody></table></div>
<p class="small">All table diffusivities are in cm² s⁻¹. In SI, D<sub>e</sub> = 4.9026 × 10⁻⁷ and 2.9870 × 10⁻⁷ m² s⁻¹, respectively. Taking M<sub>H₂</sub> = 2 instead gives approximately 0.004921 and 0.002994 cm² s⁻¹.</p>
<div class="result"><strong>Interpretation:</strong> the combined diffusivity is smaller than either individual diffusivity. At 1 atm, the Knudsen resistance dominates; at 10 atm, molecular diffusion contributes substantially, lowering D<sub>e</sub>.</div></section>

<section id="q2"><h2><span class="num">Question 02</span>Is strong pore diffusion possible?</h2>
<p class="given">Second order; d<sub>p</sub> = 0.5 mm, ρ<sub>p</sub> = 2.2 g cm⁻³, q<sub>m</sub> = 10⁵ mol h⁻¹ kg-cat⁻¹, C<sub>A</sub> = 20 mol m⁻³, D<sub>e</sub> = 5 × 10⁻⁵ m² h⁻¹.</p>
<p>Use the radius-based Weisz–Prater parameter. A value much smaller than one indicates negligible internal diffusion; a value much larger than one indicates substantial internal diffusion. This observed-rate test does not require the unknown second-order rate constant.</p>
<div class="eq">C<sub>WP</sub> = q<sub>m</sub>ρ<sub>p</sub>R² / (D<sub>e</sub>C<sub>As</sub>)<br>R = 2.5 × 10<sup>−4</sup> m; &nbsp; ρ<sub>p</sub> = 2200 kg m<sup>−3</sup><br>q<sub>v</sub> = 10⁵ × 2200 = 2.2 × 10⁸ mol m<sup>−3</sup> h<sup>−1</sup><br>C<sub>WP</sub> ≈ [(2.2 × 10⁸)(2.5 × 10<sup>−4</sup>)²] / [(5 × 10<sup>−5</sup>)(20)]<br>= <b>13,750</b></div>
<div class="result"><strong>Yes: strong pore diffusion resistance is indicated.</strong> C<sub>WP</sub> ≫ 1. If the given concentration is the bulk value rather than the surface value, C<sub>As</sub> ≤ 20 and the actual parameter is even larger.</div>
<p class="small">The printed rate is 10⁵, not 105. The second-order reaction affects detailed effectiveness-factor relations; do not insert a first-order η formula here. An alternative convention using L<sub>c</sub> = R/3 gives C<sub>WP,L</sub> = 13,750/9 ≈ 1528, with the same conclusion.</p></section>

<section id="q3"><h2><span class="num">Question 03</span>Which pellet is strongly diffusion limited?</h2>
<p class="given">First order; ρ<sub>p</sub> = 1.6 g cm⁻³, D<sub>e</sub> = 2 × 10⁻⁶ m² s⁻¹. Run 1: q<sub>m1</sub> = 3 × 10⁻⁵ mol g-cat⁻¹ s⁻¹, R₁ = 0.01 m. Run 2: q<sub>m2</sub> = 15 × 10⁻⁵ mol g-cat⁻¹ s⁻¹, R₂ = 0.001 m.</p>
<div class="note"><b>Required comparison assumption:</b> spherical pellets with the same intrinsic kinetics, density, diffusivity, temperature and surface concentration, with negligible external transfer effects. Without comparable conditions, the two observed rates alone cannot identify internal diffusion uniquely.</div>
<h3>Eliminate the unknown intrinsic rate</h3><p>For first-order reaction, q<sub>m</sub> = ηkC<sub>As</sub>/ρ<sub>p</sub>. Taking the ratio cancels both <i>k</i> and C<sub>As</sub>.</p>
<div class="eq">η(Φ) = 3(Φ coth Φ − 1)/Φ²<br>Φ₁ = (R₁/R₂)Φ₂ = 10Φ₂<br>η(10Φ₂)/η(Φ₂) = q<sub>m1</sub>/q<sub>m2</sub> = 3/15 = 0.2</div>
<p>Solve this one-variable equation numerically (for example, by bisection or Brent’s method).</p>
<div class="table-wrap"><table><thead><tr><th>Run</th><th>Φ = R√(k/D<sub>e</sub>)</th><th>η</th><th>C<sub>WP</sub> = ηΦ²</th><th>Conclusion</th></tr></thead><tbody>
<tr><td>1: R = 10 mm</td><td>16.4561</td><td>0.171225</td><td>46.3684</td><td><b>Strong pore diffusion</b></td></tr>
<tr><td>2: R = 1 mm</td><td>1.64561</td><td>0.856123</td><td>2.31842</td><td>Moderate internal effect; not strong</td></tr></tbody></table></div>
<div class="result"><strong>Run 1 is in the strong pore-diffusion regime.</strong> Only about 17.1% of the intrinsic rate at the surface concentration is realised. Run 2 retains about 85.6%, so it is not fully free of diffusion resistance.</div>
<p>As a check, if <em>both</em> runs were strongly limited, η ∝ 1/R would give a rate ratio of 0.1, rather than the observed 0.2. The exact spherical formula is needed for the smaller pellet.</p>
<details><summary>Optional consistency check using the supplied density and diffusivity</summary><p>ρ<sub>p</sub> = 1.6 × 10⁶ g m⁻³, so q<sub>v1</sub> = 48 and q<sub>v2</sub> = 240 mol m⁻³ s⁻¹. The fitted Φ₂ implies k = D<sub>e</sub>Φ₂²/R₂² = 5.41609 s⁻¹ and a common C<sub>As</sub> = q<sub>v2</sub>/(η₂k) = 51.7594 mol m⁻³. These are inferred under the comparison assumptions, not additional data printed in the question.</p></details></section>

<section id="q4"><h2><span class="num">Question 04</span>Concentration inside a spherical pellet</h2>
<p class="given">C<sub>As</sub> = 0.001 g-mol dm⁻³, d = 0.2 cm, R = 0.1 cm, D<sub>e</sub> = 0.1 cm² s⁻¹. Evaluate 0.03 cm inward from the surface and find the diameter for η = 0.8.</p>
<div class="note"><b>The worksheet needs a correction and one extra datum.</b> The profile sinh(ξφ)/(ξ sinh φ) uses φ = R√(k/D<sub>e</sub>), whereas the printed definition is R√(k/D<sub>e</sub>)/3. With that printed definition, the profile must contain <b>3φ</b>. Also, no numerical value of <i>k</i> is supplied, so neither requested dimensional answer is unique.</div>
<h3>(a) Position and concentration</h3><p>The radial coordinate is measured from the centre, so r = R − 0.03 = 0.07 cm and ξ = r/R = 0.7. Define Φ = R√(k/D<sub>e</sub>) consistently.</p>
<div class="eq">C<sub>A</sub>/C<sub>As</sub> = sinh(ξΦ)/(ξ sinh Φ)<br>Φ = (0.1 cm)√[k/(0.1 cm² s<sup>−1</sup>)]<br><b>C<sub>A</sub>(r = 0.07 cm) = (0.001/0.7) sinh(0.7Φ)/sinh Φ &nbsp; mol dm<sup>−3</sup></b></div>
<p>A g-mol is a mole. Hence C<sub>As</sub> = 0.001 mol dm⁻³ = 10⁻⁶ mol cm⁻³ = 1 mol m⁻³. Keeping the concentration in mol dm⁻³ is valid because the profile is a dimensionless ratio.</p>
<h3>(b) Diameter for 80% effectiveness</h3><div class="eq">0.8 = 3(Φ<sub>new</sub> coth Φ<sub>new</sub> − 1)/Φ<sub>new</sub>²<br>Φ<sub>new</sub> = <b>2.04207798</b>; &nbsp; φ<sub>new</sub> = Φ<sub>new</sub>/3 = 0.68069266<br>d<sub>new</sub> = 2Φ<sub>new</sub>√(D<sub>e</sub>/k) = <b>4.08415596√(D<sub>e</sub>/k)</b><br>d<sub>new</sub> = <b>1.2915235 / √[k/(1 s<sup>−1</sup>)] &nbsp; cm</b></div>
<div class="result"><strong>These are the complete results possible from the supplied data.</strong> Insert the missing first-order rate constant <i>k</i> in s⁻¹ to obtain numerical concentration and diameter. A diameter reduction is required only if k &gt; 41.7008 s⁻¹; below this value, the original pellet already has η &gt; 0.8.</div>
<div class="interactive"><h3>Evaluate when the missing k is available</h3><label for="k-input">k (s⁻¹): </label><input type="number" id="k-input" min="0" step="any" placeholder="Enter k"><button id="calculate-k">Calculate</button><output id="k-output" aria-live="polite">No rate constant assumed.</output></div></section>

<section id="q5"><h2><span class="num">Question 05</span>Internal or external mass-transfer limitation?</h2>
<p class="given">d<sub>p</sub> = 2.4 mm; D<sub>e</sub> = 5 × 10⁻⁵ m² h⁻¹; k<sub>g</sub> = 300 m h⁻¹; C<sub>Ag</sub> = 20 mol m⁻³; q<sub>v</sub> = 10⁵ mol h⁻¹ m⁻³-cat; first order. Density = 2.8 g cm⁻³ and pellet porosity = 0.4 are also listed.</p>
<h3>1. Keep the rate and geometry on the same basis</h3><p>Interpret “m³ cat” as total pellet volume. The observed rate is already per pellet volume, so do not multiply by density again. D<sub>e</sub> is already effective, so do not apply another porosity correction.</p>
<div class="eq">R = 1.2 × 10<sup>−3</sup> m; &nbsp; V<sub>p</sub>/S<sub>p</sub> = R/3 = 4.0 × 10<sup>−4</sup> m</div>
<h3>2. Mears criterion for external mass transfer</h3><div class="eq">C<sub>M</sub> = n q<sub>v</sub>R / (k<sub>g</sub>C<sub>Ag</sub>)<br>= (1)(10⁵)(1.2 × 10<sup>−3</sup>)/(300 × 20)<br>= <b>0.0200 &lt; 0.15</b></div>
<p>Using the radius-based form, external mass-transfer resistance is negligible by the Mears criterion. A direct pellet balance confirms the small concentration drop:</p>
<div class="eq">q<sub>v</sub>V<sub>p</sub> = k<sub>g</sub>S<sub>p</sub>(C<sub>Ag</sub> − C<sub>As</sub>)<br>C<sub>As</sub> = 20 − q<sub>v</sub>R/(3k<sub>g</sub>) = <b>19.8667 mol m<sup>−3</sup></b><br>(C<sub>Ag</sub> − C<sub>As</sub>)/C<sub>Ag</sub> = 0.006667 = 0.667%</div>
<h3>3. Weisz–Prater criterion for internal diffusion</h3><div class="eq">C<sub>WP</sub> = q<sub>v</sub>R²/(D<sub>e</sub>C<sub>As</sub>)<br>= [(10⁵)(1.2 × 10<sup>−3</sup>)²]/[(5 × 10<sup>−5</sup>)(19.8667)]<br>= <b>144.97 ≫ 1</b></div>
<div class="result"><strong>The observed rate is limited by internal pore diffusion; external mass transfer is negligible.</strong> Using C<sub>As</sub> ≈ C<sub>Ag</sub> gives C<sub>WP</sub> = 144, which leads to the same conclusion.</div>
<p class="small">With the alternative characteristic length R/3, the corresponding numbers are C<sub>WP,L</sub> = 16.107 and C<sub>M,L</sub> = 0.006667. State the convention used. If the rate were explicitly per skeletal-solid volume instead, its pellet-volume value would be (1 − ε<sub>p</sub>)q<sub>v</sub>; that interpretation would also give strong internal and negligible external resistance.</p></section>

<section id="q6"><h2><span class="num">Question 06</span>Doubling the pellet diameter</h2>
<p class="given">First-order packed-bed reaction; 9 mm pellets give X₁ = 0.632 under strong pore diffusion. Replace them with 18 mm pellets.</p>
<p>Assume the same catalyst mass, inlet flow, temperature and intrinsic kinetics, with unchanged relevant concentration–conversion relation and negligible pressure effects on the rate. Under strong internal diffusion, η ∝ 1/R ∝ 1/d<sub>p</sub>, so doubling the diameter halves the observed first-order rate coefficient.</p>
<div class="eq">k<sub>app,2</sub>/k<sub>app,1</sub> = d<sub>p1</sub>/d<sub>p2</sub> = 9/18 = 1/2<br>For a constant-density plug-flow model: −ln(1 − X) = k<sub>app</sub>τ<br>−ln(1 − X₂) = ½[−ln(1 − 0.632)]<br>1 − X₂ = √0.368 = 0.606630<br><b>X₂ = 0.393370 ≈ 39.3%</b></div>
<div class="result"><strong>Conversion falls from 63.2% to about 39.3%.</strong> This is a drop of 23.9 percentage points. Halving the rate coefficient does not halve the conversion because the plug-flow relation is exponential.</div>
<p class="small">The pellets are enlarged to reduce pressure drop, but no pressure profile is supplied. The numerical answer isolates the pellet-size effect; a simultaneous pressure change affecting kinetics would need additional reactor data.</p></section>

<section id="q7"><h2><span class="num">Question 07</span>Reaction–diffusion profiles in a flat catalyst</h2>
<p>Let L be the half-thickness of a slab exposed on both faces, ξ = x/L and u = C<sub>A</sub>/C<sub>As</sub>. The centre plane is ξ = 0 and the external surface is ξ = 1.</p>
<div class="eq">d²u/dξ² = φ²u<sup>n</sup>, &nbsp; u′(0) = 0, &nbsp; u(1) = 1<br>φ² = kL²C<sub>As</sub><sup>n−1</sup>/D<sub>e</sub><br>dC<sub>A</sub>/dx = (C<sub>As</sub>/L)u′(ξ)</div>
<p>The code below computes both concentration and its gradient. It uses a boundary-value solver with continuation in φ, and checks the numerical first-order solution against the analytical expression. Curves are generated from the computed values and embedded as vector graphics.</p>
<h3>(a) First-order benchmark: φ = 0.1, 1, 10, 100</h3><p>For n = 1, the general solution is u = A cosh(φξ) + B sinh(φξ). The zero-gradient condition gives B = 0; u(1) = 1 gives A = 1/cosh φ.</p>
<div class="eq">u(ξ) = cosh(φξ)/cosh φ<br>u′(ξ) = φ sinh(φξ)/cosh φ; &nbsp; η = tanh φ/φ</div>
{{Q7A}}
<div class="table-wrap"><table><thead><tr><th>φ</th><th>u(0) = 1/cosh φ</th><th>η</th><th>Meaning</th></tr></thead><tbody><tr><td>0.1</td><td>0.995021</td><td>0.996680</td><td>Nearly uniform concentration</td></tr><tr><td>1</td><td>0.648054</td><td>0.761594</td><td>Appreciable concentration gradient</td></tr><tr><td>10</td><td>9.07999 × 10⁻⁵</td><td>0.100000</td><td>Reaction concentrated near the surface</td></tr><tr><td>100</td><td>7.44015 × 10⁻⁴⁴</td><td>0.010000</td><td>Only a very thin surface layer contributes</td></tr></tbody></table></div>
<h3>(b) Compare n = 0.5, 1.5 and 2 at φ = 0.1 and 100</h3>
{{Q7B}}
{{Q7FULL}}
<p>At φ = 0.1, every profile remains close to one, so the entire slab is supplied with reactant. At φ = 100, concentration changes rapidly near the surface and most of the interior contributes little. The detailed plot uses ξ = 0.9–1 to make those gradients visible; the full-domain plot shows the complete half-slab.</p>
<p>At a fixed φ and for 0 &lt; u &lt; 1, increasing <i>n</i> makes u<sup>n</sup> smaller. The dimensionless sink is therefore weaker at low concentrations and the concentration penetrates farther into the slab. This comparison holds φ fixed; <i>k</i> has different units for different reaction orders.</p>
<h3>The half-order case has a dead core</h3><p>For 0 &lt; n &lt; 1, concentration can reach zero at a finite distance. Starting from u = u′ = 0 at an interface ξ₀, integration of the governing equation gives:</p>
<div class="eq">φ<sub>crit</sub> = √[2(n + 1)]/(1 − n)<br>ξ₀ = 1 − φ<sub>crit</sub>/φ &nbsp; (when φ ≥ φ<sub>crit</sub>)<br>u = 0 for ξ ≤ ξ₀;<br>u = [(ξ − ξ₀)/(1 − ξ₀)]<sup>2/(1−n)</sup> for ξ ≥ ξ₀</div>
<p>For n = 0.5, φ<sub>crit</sub> = 2√3 = 3.46410. Thus at φ = 100, ξ₀ = <b>0.965359</b> and u = [(ξ − ξ₀)/(1 − ξ₀)]⁴ in the active region. Only the outer 3.464% of each half-slab contains reactant. The code uses this exact piecewise solution for the dead-core branch; it does not force a positive solution where none exists.</p>
<div class="table-wrap"><table><thead><tr><th>n, at φ = 100</th><th>u(0)</th><th>u′(1)</th><th>η = ∫₀¹u<sup>n</sup>dξ</th></tr></thead><tbody>
<tr><td>0.5</td><td>0, exact dead core</td><td>115.4701</td><td>0.0115470</td></tr><tr><td>1</td><td>7.44015 × 10⁻⁴⁴, analytical</td><td>100.0000</td><td>0.0100000</td></tr><tr><td>1.5</td><td>5.51973 × 10⁻⁶</td><td>89.4427</td><td>0.00894427</td></tr><tr><td>2</td><td>8.42950 × 10⁻⁴</td><td>81.6497</td><td>0.00816497</td></tr></tbody></table></div>
<p>A higher concentration profile does not automatically mean a larger effectiveness factor across different <i>n</i>: η integrates u<sup>n</sup>, not u. For strong diffusion, η ≈ √[2/(n + 1)]/φ, consistent with the last column.</p>
<div class="result"><strong>Numerical checks passed:</strong> the maximum absolute first-order error is below 5 × 10⁻¹⁰ over the plotted grid. For the Q7(b) cases, the integrated reaction matches the surface flux, η = u′(1)/φ², within 2 × 10⁻⁷. Boundary conditions and monotonic concentration profiles are also checked. Extremely small centre values should be read from the analytical first-order solution.</div></section>

<section id="q8"><h2><span class="num">Question 08</span>Effectiveness factors for three shapes</h2>
<p>Use the worksheet’s common characteristic-length convention, φ = (V<sub>p</sub>/S<sub>p</sub>)√(k/D<sub>e</sub>). For a long cylinder, end effects are neglected. For a flat plate, L is the half-thickness.</p>
<div class="table-wrap"><table><thead><tr><th>Shape</th><th>φ</th><th>η</th></tr></thead><tbody>
<tr><td>Flat plate</td><td>L√(k/D<sub>e</sub>)</td><td>tanh φ / φ</td></tr><tr><td>Sphere</td><td>(R/3)√(k/D<sub>e</sub>)</td><td>(3φ coth 3φ − 1)/(3φ²)</td></tr><tr><td>Long cylinder</td><td>(R/2)√(k/D<sub>e</sub>)</td><td>I₁(2φ)/[φI₀(2φ)]</td></tr></tbody></table></div>
<p>I₀ and I₁ are modified Bessel functions of the first kind. The Python code uses their exponentially scaled versions, <code>ive</code>; the scaling cancels in the ratio and avoids overflow.</p>
{{Q8}}
<div class="table-wrap"><table><thead><tr><th>φ</th><th>Flat plate η</th><th>Sphere η</th><th>Cylinder η</th></tr></thead><tbody><tr><td>1</td><td>0.761594</td><td>0.671636</td><td>0.697775</td></tr><tr><td>10</td><td>0.100000</td><td>0.0966667</td><td>0.0974671</td></tr><tr><td>100</td><td>0.0100000</td><td>0.00996667</td><td>0.00997497</td></tr></tbody></table></div>
<h3>Physical interpretation</h3><ul><li><b>All three curves decrease:</b> a larger φ means reaction is faster relative to diffusion, or the diffusion length is larger. Interior catalyst is used less effectively.</li><li><b>Small-φ limit:</b> although the requested graph starts at 1, all three expressions approach η = 1 as φ → 0, when internal concentration gradients vanish.</li><li><b>Large-φ limit:</b> every shape approaches η ≈ 1/φ with the V/S definition. Reaction takes place in a thin outer layer, making local surface behaviour more important than the overall shape.</li><li><b>At the same plotted φ:</b> η<sub>plate</sub> &gt; η<sub>cylinder</sub> &gt; η<sub>sphere</sub> in the requested range. This compares equal V/S-based modulus, not equal numerical radius or thickness.</li></ul>
<div class="result"><strong>At φ = 100, each pellet uses only about 1% of its intrinsic reaction capacity.</strong> Reducing particle size increases η, but a packed bed then generally has a larger pressure drop—the trade-off illustrated by Q6.</div></section>

<section id="code"><h2>Runnable Python for Q7 and Q8</h2><p>Download the script, install its dependencies, and run it in a folder of your choice. It writes the four SVG figures shown above. Numerical checks are built into the script and run automatically.</p>
<pre>python -m pip install numpy scipy matplotlib
python tutorial4_code.py</pre>
<div class="tools"><a class="button" download="tutorial4_code.py" href="data:text/x-python;base64,{{CODE64}}">Download Python code</a><button class="secondary" id="copy-code">Copy code</button><span id="copy-status" aria-live="polite"></span></div>
<details><summary>View the complete, commented Python script</summary><pre><code id="python-code">{{CODE}}</code></pre></details>
<p class="small">This HTML contains its own figures and code, and works offline. No screenshots or external plotting libraries are needed to view it. Open the code panel before printing if you want the full script included in the printout.</p></section>

<section id="answers"><h2>Quick answer check</h2><div class="table-wrap"><table><thead><tr><th>Question</th><th>Result</th></tr></thead><tbody><tr><td>1</td><td>D<sub>e</sub> = 0.0049026 cm²/s at 1 atm; 0.0029870 cm²/s at 10 atm.</td></tr><tr><td>2</td><td>C<sub>WP</sub> = 13,750: strong internal diffusion.</td></tr><tr><td>3</td><td>Run 1 strongly limited; Run 2 moderately affected, under matched conditions.</td></tr><tr><td>4</td><td>Missing k; concentration and diameter given parametrically. Target Φ = 2.04208.</td></tr><tr><td>5</td><td>C<sub>M</sub> = 0.0200; C<sub>WP</sub> = 144.97: internal limitation only.</td></tr><tr><td>6</td><td>X₂ ≈ 39.3%, with other reactor conditions unchanged.</td></tr><tr><td>7</td><td>Profiles and Python supplied; n = 0.5, φ = 100 has ξ₀ = 0.965359.</td></tr><tr><td>8</td><td>All shapes approach η ≈ 1/φ under strong pore diffusion.</td></tr></tbody></table></div></section>
<footer><p><b>Source:</b> <a href="Tutorial%204_CL24303_MO26.pdf">Tutorial 4_CL24303_MO26.pdf</a>, all three pages; page 3 is blank in the provided file. These are worked solutions, not an official answer key.</p><p>For the conventional spherical effectiveness expression and observed-rate criteria, see H. Scott Fogler’s <a href="https://websites.umich.edu/~elements/5e/15chap/Fogler_Web_Ch15.pdf">Diffusion and Reaction in Porous Catalysts, Chapter 15</a>. The numerical results and graphs here are calculated from the tutorial data; assumptions and the Q4 inconsistency are stated where they affect the answer.</p></footer>
</main>
<script>
document.getElementById('calculate-k').addEventListener('click',()=>{
 const k=Number(document.getElementById('k-input').value),out=document.getElementById('k-output');
 if(!Number.isFinite(k)||k<=0){out.textContent='Enter a positive, finite k in s⁻¹.';return;}
 const p=Math.sqrt(0.1*k),x=0.7;
 const ratio=p<1e-4 ? 1+(x*x-1)*p*p/6 : Math.exp((x-1)*p)*(-Math.expm1(-2*x*p))/(-Math.expm1(-2*p))/x;
 const c=.001*ratio,d=1.291523513732011/Math.sqrt(k);
 out.textContent=`C_A at r = 0.07 cm: ${c.toExponential(6)} mol/dm³. Target diameter: ${d.toPrecision(7)} cm. `+(d<.2?'The target requires a smaller pellet.':'The original pellet already meets η ≥ 0.8.');
});
document.getElementById('copy-code').addEventListener('click',async()=>{
 const text=document.getElementById('python-code').textContent;
 try{await navigator.clipboard.writeText(text);document.getElementById('copy-status').textContent='Copied.';}
 catch(e){document.querySelector('#code details').open=true;document.getElementById('copy-status').textContent='Use the download button, or select the code below.';}
});
</script></body></html>'''
page = page.replace('{{Q7A}}', figure('q7a.svg', 'Numerical first-order profiles with analytical values marked by open circles.'))
page = page.replace('{{Q7B}}', figure('q7b.svg', 'Reaction-order comparison: expanded concentration scale at low phi; surface detail at high phi.'))
page = page.replace('{{Q7FULL}}', figure('q7b_full.svg', 'All high-phi reaction-order profiles over the complete domain, 0 ≤ xi ≤ 1.'))
page = page.replace('{{Q8}}', figure('q8.svg', 'Effectiveness factors over phi = 1–100, with a close view of phi = 1–5.'))
page = page.replace('{{CODE64}}', base64.b64encode(code.encode()).decode()).replace('{{CODE}}', html.escape(code))
OUT.write_text(page, encoding='utf-8')
print(f'Created {OUT} ({OUT.stat().st_size:,} bytes)')
