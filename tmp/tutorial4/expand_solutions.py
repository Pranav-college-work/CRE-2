"""Expand the verified Tutorial 4 artifact with locally checked book citations."""
from pathlib import Path
from urllib.parse import quote
import runpy
from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
runpy.run_path(str(HERE/'build_html.py'))
OUT = HERE.parents[1]/'Tutorial 4'/'Tutorial4_Solutions.html'
soup = BeautifulSoup(OUT.read_text(encoding='utf-8'), 'html.parser')

F='Fogler 5th Edn(full).pdf'
L='Levenspiel(full).pdf'
P='Course Policy and Lecture Plan for CRE II (CL24303)- MO2026.pdf'
T='Tutorial 4_CL24303_MO26.pdf'
# Each page number below is a 1-based PDF-viewer page, checked against the
# printed running page in the local file. No edition offsets are guessed.
REFS={
'P':(P,3,'Course planner, MO2026','Lecture plan, Module 3, lectures 20–25; printed p. 3, PDF p. 3. Lectures 20–22 assign OL Ch. 18 and HSF Ch. 15. The book list is on printed/PDF p. 1.'),
'T':(T,1,'Tutorial 4, CL24303, MO2026','Question data: Q1–Q4 on PDF p. 1; Q5–Q8 on PDF p. 2. PDF p. 3 is blank. Assigned 25 September 2026.'),
'F1':(F,719,'Fogler, Elements of Chemical Reaction Engineering, 5th ed.','§14.2.1, Table 14-1, printed p. 684 (PDF p. 719): Knudsen transport. §14.2.4 and Table 14-3, printed pp. 686–687 (PDF pp. 721–722): diffusivity versus temperature and pressure.'),
'F2':(F,756,'Fogler, 5th ed.','§15.2.1, printed pp. 721–723 (PDF pp. 756–758), Eq. (15-1) and Example 15-1: effective diffusivity, porosity, tortuosity and constriction.'),
'F3':(F,758,'Fogler, 5th ed.','§§15.2.2–15.2.4, printed pp. 723–729 (PDF pp. 758–764): shell balance, rate bases, dimensionless equation, radius-based modulus Eq. (15-23), and spherical concentration profile Eq. (15-27).'),
'F4':(F,765,'Fogler, 5th ed.','§15.3.1, printed pp. 730–733 (PDF pp. 765–768): η definition Eq. (15-28), spherical η Eq. (15-32), shape comparison Fig. 15-5, and strong-diffusion limit Eqs. (15-33)–(15-34).'),
'F5':(F,769,'Fogler, 5th ed.','§15.3.4, printed pp. 734–735 (PDF pp. 769–770), Eqs. (15-37)–(15-39): observed-rate Weisz–Prater parameter and its interpretation.'),
'F6':(F,770,'Fogler, 5th ed.','Example 15-2, printed pp. 735–737 (PDF pp. 770–772): two pellet sizes, the same rate/radius data as Tutorial Q3, identical run conditions, and elimination of unknown surface concentration. The η₁ value on p. 736 uses a large-modulus approximation.'),
'F7':(F,778,'Fogler, 5th ed.','§15.6.1, printed pp. 743–744 (PDF pp. 778–779), Eq. (15-62) and MR < 0.15: Mears external mass-transfer criterion. The printed density is bed bulk density; see the explicit basis discussion in Q5.'),
'F8':(F,795,'Fogler, 5th ed.','Problem P15-5B, printed p. 760 (PDF p. 795): platinum-plated sphere, C(R/2)/Cₛ = 0.1, original diameter 2 × 10⁻³ cm, original inward distance 3 × 10⁻⁴ cm. This additional concentration datum is absent from Tutorial Q4.'),
'F9':(F,768,'Fogler, 5th ed.','§15.3.3, printed pp. 733–734 (PDF pp. 768–769), Eq. (15-35): strong-diffusion effectiveness for nth-order reaction. The slab first-integral and dead-core derivations in this solution are worked out directly from the tutorial equation.'),
'F10':(F,775,'Fogler, 5th ed.','§15.5, printed pp. 740–743 (PDF pp. 775–778), especially Eqs. (15-52)–(15-59): film balance and distinction between internal and overall effectiveness factors.'),
'L1':(L,397,'Levenspiel, Chemical Reaction Engineering, 3rd ed.','§18.2, printed pp. 381–385 (PDF pp. 397–401), Eqs. (10)–(12): one-dimensional diffusion–reaction profile and tanh-modulus effectiveness. The book measures position inward from the pore entrance; Q7 measures outward from the symmetry plane.'),
'L2':(L,401,'Levenspiel, 3rd ed.','§18.3, printed pp. 385–388 (PDF pp. 401–404): characteristic length Eq. (13); rate bases Eqs. (14)–(19); shape formulas Eqs. (20)–(23); observable modulus Eq. (24); size scaling Eq. (25).'),
'L3':(L,405,'Levenspiel, 3rd ed.','§18.3, “Arbitrary Reaction Kinetics,” printed pp. 389–390 (PDF pp. 405–406), Eqs. (26)–(29): generalized modulus and apparent order under strong pore diffusion.'),
'L4':(L,440,'Levenspiel, 3rd ed.','Problem 18.31, printed p. 424 (PDF p. 440): the same 9 mm → 18 mm pellet and 63.2% conversion problem as Tutorial Q6.'),
}
def cite(*keys):
    return ' '.join(f'<a class="cite" href="#ref-{k}" title="{REFS[k][2]} — {REFS[k][3]}">[{k}]</a>' for k in keys)
def parse(markup): return BeautifulSoup(markup,'html.parser')
def append_to(id,markup):
    section=soup.find(id=id)
    for child in list(parse(markup).contents): section.append(child)
def insert_before(id,markup):
    section=soup.find(id=id)
    for child in list(parse(markup).contents): section.insert_before(child)
def after_heading(id,markup):
    heading=soup.find(id=id).find('h2')
    for child in reversed(list(parse(markup).contents)): heading.insert_after(child)

soup.title.string='Tutorial 4 | Detailed, textbook-referenced solutions | CRE II'
soup.find('header').find('p').string='A self-contained guide to catalyst-pore diffusion: physical reasoning, full derivations, worked calculations, and references to the course textbooks.'
soup.find('header').find(class_='meta').string='CL24303 · All eight questions · Revised against the local course planner and textbooks'
soup.find(id='overview').find(class_='note').clear()
soup.find(id='overview').find(class_='note').append(parse('<b>Read the source notes carefully.</b> Q3 matches Fogler Example 15-2. Q4 closely matches Fogler Problem P15-5B, but the tutorial omits the internal concentration datum and changes the dimensions. Both the answer to the printed question and a clearly conditional textbook-based completion are given below. '+cite('F6','F8')))

insert_before('overview',f'''<section id="reading"><h2>How this solution follows the course planner</h2>
<p>The planner assigns <b>Module 3, lectures 20–22</b> to solid-catalysed reaction kinetics and isothermal interphase/intraphase effectiveness factors, with <b>Levenspiel Chapter 18</b> and <b>Fogler Chapter 15</b> as the reading. It places Tutorial 4 at lecture 23. The worksheet was assigned later than the planned date, but its content still belongs to that module. {cite('P','T')}</p>
<div class="table-wrap"><table><thead><tr><th>Tutorial topic</th><th>Relevant assigned reading</th><th>What to learn from it</th></tr></thead><tbody>
<tr><td>Q1: pore and effective diffusion</td><td>Fogler §15.2.1; supporting §14.2 {cite('F1','F2')}</td><td>Distinguish a fluid diffusivity from an effective pellet diffusivity.</td></tr>
<tr><td>Q2, Q3, Q5: identify resistance</td><td>Fogler §15.3.4, Example 15-2, §15.6.1; Levenspiel §18.3 {cite('F5','F6','F7','L2')}</td><td>Use measured rates, the right density basis, and the right characteristic length.</td></tr>
<tr><td>Q4: spherical concentration and size</td><td>Fogler §§15.2.2–15.3.1 and P15-5B {cite('F3','F4','F8')}</td><td>Derive the profile, apply boundary conditions, and solve for a target η.</td></tr>
<tr><td>Q6: pellet size and conversion</td><td>Levenspiel §18.3 and Problem 18.31; Fogler §15.3.1 {cite('L2','L4','F4')}</td><td>Connect η ∝ 1/d to the packed-bed mole balance.</td></tr>
<tr><td>Q7, Q8: profiles, order and shape</td><td>Levenspiel §§18.2–18.3; Fogler §§15.2–15.3 {cite('L1','L2','L3','F9')}</td><td>Turn diffusion balances into differential equations and interpret their solutions.</td></tr>
</tbody></table></div>
<p>Later Module 3 lectures list Levenspiel Chapters 19, 20 and 22, but their reactor/contacting models are not needed to solve these eight questions. Smith and Carberry are listed as course references; the planner specifically identifies Fogler and Levenspiel for this topic, so those are the primary sources used here.</p>
<p><b>Citation format:</b> a reference such as [F3] leads to a precise section, equation and printed-page range. The reference entry also gives the local PDF page number and a clickable link. Printed page 729 in Fogler is PDF page 764 in the supplied full book; printed page 387 in Levenspiel is PDF page 403. This distinction prevents opening the wrong page.</p>
<p class="small">Explanations, derivations and numerical results are written for this worksheet. Book equations are identified at their point of use; a citation to a related method does not imply that the book contains this tutorial’s exact numerical answer.</p>
</section>''')

insert_before('q1',f'''<section id="foundations"><h2>The ideas needed for every question</h2>
<h3>1. Why diffusion changes an observed reaction rate</h3>
<p>A porous catalyst pellet is a solid containing connected pores. Reactant moves from the surrounding bulk fluid, across an external fluid film, through the pore network, and finally to internal catalytic sites. Reaction consumes A as it travels inward. If consumption is fast compared with replenishment, the centre receives less reactant than the exterior. The catalyst can be chemically active throughout while much of its interior contributes little to the measured rate. {cite('F3','L1')}</p>
<div class="eq">Bulk fluid, C<sub>Ab</sub> → external film → pellet surface, C<sub>As</sub> → pores → interior, C<sub>A</sub>(r)<br>For a consuming, isothermal pellet: C<sub>Ab</sub> ≥ C<sub>As</sub> ≥ C<sub>A</sub>(r)</div>
<p><b>External resistance</b> causes the first concentration drop, C<sub>Ab</sub> − C<sub>As</sub>. <b>Internal resistance</b> causes the spatial variation inside the pellet. An experiment may have either, both, or neither. A high internal-diffusion parameter does not prove that external transport is negligible; Q5 checks the two separately.</p>
<h3>2. Intrinsic rate, observed rate and effectiveness factor</h3>
<p>The intrinsic local rate is the rate law at the actual local concentration and temperature, before any concentration gradient is averaged over. Write its positive volumetric disappearance rate as q<sub>int</sub>(r) = kC<sub>A</sub>(r)<sup>n</sup>. The total pellet rate is the integral of that local rate. Dividing by the pellet volume gives the observed average q<sub>v</sub>.</p>
<div class="eq">q<sub>v</sub> = (1/V<sub>p</sub>) ∫<sub>Vₚ</sub> kC<sub>A</sub><sup>n</sup> dV<br>η = q<sub>v</sub> / (kC<sub>As</sub><sup>n</sup>)<br>Therefore q<sub>v</sub> = ηkC<sub>As</sub><sup>n</sup></div>
<p>η compares the real pellet with an imaginary pellet whose <em>entire interior</em> is at the external-surface concentration. For the isothermal, consuming power-law reactions in this tutorial, 0 ≤ η ≤ 1. It is a ratio of rates, not necessarily the fraction of catalyst volume that is physically active. A first-order pellet with η = 0.2 delivers 20% of the uniformly supplied pellet’s rate. {cite('F4')}</p>
<p>For a first-order reaction, the <b>overall</b> effectiveness factor referenced to bulk concentration is Ω = q<sub>v</sub>/(kC<sub>Ab</sub>) = ηC<sub>As</sub>/C<sub>Ab</sub>. Thus Ω includes the external drop as well as the internal loss; η alone does not. {cite('F10')}</p>
<h3>3. Make the units match before inserting numbers</h3>
<div class="table-wrap"><table><thead><tr><th>Quantity</th><th>Definition</th><th>Typical units here</th></tr></thead><tbody>
<tr><td>q<sub>m</sub> = −r′<sub>A,obs</sub></td><td>Rate per catalyst mass</td><td>mol kg-cat⁻¹ h⁻¹, or mol g-cat⁻¹ s⁻¹</td></tr>
<tr><td>q<sub>v</sub></td><td>Rate per total pellet volume</td><td>mol m-pellet⁻³ h⁻¹</td></tr>
<tr><td>ρ<sub>p</sub></td><td>Catalyst mass / total pellet volume</td><td>kg m-pellet⁻³</td></tr>
<tr><td>q<sub>v</sub> = ρ<sub>p</sub>q<sub>m</sub></td><td>Mass-rate to pellet-volume-rate conversion</td><td>Use g-based density with a g-based rate, or kg with kg.</td></tr>
<tr><td>k for q<sub>int</sub> = kC<sup>n</sup></td><td>Rate constant on the pellet-volume basis</td><td>(m³/mol)<sup>n−1</sup> time⁻¹; for n = 1, time⁻¹</td></tr>
</tbody></table></div>
<p>The concentration refers to the pore fluid, while the homogenised reaction rate and flux are referred to pellet volume and gross cross-sectional area. The effective diffusivity makes this averaged description possible. A skeletal-solid density, a pellet density and a packed-bed bulk density are different quantities. Do not swap them without changing the rate basis. {cite('F2','F3','L2')}</p>
<h3>4. What the Thiele modulus actually compares</h3>
<p>A diffusion time over distance ℓ is of order t<sub>D</sub> = ℓ²/D<sub>e</sub>. For first-order reaction the chemical time is t<sub>R</sub> = 1/k. Their ratio is φ² = kℓ²/D<sub>e</sub>. If φ is small, diffusion can replenish the pellet before much reactant is consumed. If φ is large, reaction consumes reactant faster than it can reach the deep interior. The modulus needs an <em>intrinsic</em> k; substituting a diffusion-slowed observed k would make the test circular. {cite('F3','F4')}</p>
<div class="table-wrap"><table><thead><tr><th>Convention</th><th>Sphere</th><th>How to use it</th></tr></thead><tbody>
<tr><td>Radius-based, used in Fogler’s spherical derivation</td><td>Φ = R√(k/D<sub>e</sub>)</td><td>η = 3(Φ coth Φ − 1)/Φ²</td></tr>
<tr><td>V/S-based, used for the shape comparison</td><td>φ = (R/3)√(k/D<sub>e</sub>) = Φ/3</td><td>η = (3φ coth 3φ − 1)/(3φ²)</td></tr>
</tbody></table></div>
<p>These are the same physics in different coordinates. The factor of three must move into <em>every</em> occurrence of the radius-based modulus. This is the source of Q4’s printed inconsistency. Levenspiel’s characteristic-length definition is Eq. (13), p. 386; the matching shape expressions are Eqs. (20)–(23), p. 387. {cite('L2','F4')}</p>
<h3>5. Diagnose diffusion when intrinsic k is unknown</h3>
<p>For a sphere, define the radius-based observed-rate parameter and Levenspiel’s characteristic-length parameter as follows:</p>
<div class="eq">C<sub>WP</sub> = q<sub>v</sub>R²/(D<sub>e</sub>C<sub>As</sub>)<br>M<sub>W</sub> = q<sub>v</sub>(V<sub>p</sub>/S<sub>p</sub>)²/(D<sub>e</sub>C<sub>As</sub>) = C<sub>WP</sub>/9</div>
<p>Both can be calculated from observed rate data. For first order, C<sub>WP</sub> = ηΦ² and M<sub>W</sub> = ηφ². Fogler discusses C<sub>WP</sub> ≪ 1 versus ≫ 1. Levenspiel gives practical guide values <b>M<sub>W</sub> &lt; 0.15</b> for negligible pore resistance and <b>M<sub>W</sub> &gt; 4</b> for strong resistance. These are regime guides, not a discontinuous change in physics, and their numbers belong to their stated length convention. {cite('F5','L2')}</p>
<p>For nth-order kinetics, a useful radius-based definition is Φ<sub>n</sub>² = kR²C<sub>As</sub><sup>n−1</sup>/D<sub>e</sub>; multiplying by η again gives C<sub>WP</sub>. Levenspiel also uses a generalised nth-order Thiele modulus containing √[(n + 1)/2]. That generalisation is <em>not</em> the φ supplied in Q7’s differential equation. {cite('F9','L3')}</p>
<h3>6. A repeatable solution method</h3><ol><li>Identify whether the requested quantity is a diffusivity, profile, diagnostic parameter, effectiveness factor or reactor conversion.</li><li>Write the geometry and rate basis explicitly; convert diameter to radius when necessary.</li><li>Select a formula whose assumptions and modulus definition match the problem.</li><li>Insert consistent units, calculate, and interpret the size of the result.</li><li>Check the relevant limit: concentration cannot exceed the surface value here, η cannot exceed one, and a combined diffusivity must be below both constituent diffusivities.</li></ol>
</section>''')

after_heading('q1',f'<p class="source-line">Reading: the supplied correlations are in Tutorial Q1; transport interpretation and pellet corrections are in Fogler §§14.2 and 15.2.1. {cite("T","F1","F2")}</p>')
after_heading('q2',f'<p class="source-line">Reading: Fogler §15.3.4 and Levenspiel §18.3, especially the observable modulus. {cite("F5","L2")}</p>')
after_heading('q3',f'<p class="source-line">Source match: the measured rates and radii coincide with Fogler Example 15-2. {cite("F6")}</p>')
after_heading('q4',f'<p class="source-line">Reading: spherical balance and profile, Fogler §§15.2.2–15.3.1. Related original problem: P15-5B. {cite("F3","F4","F8")}</p>')
after_heading('q5',f'<p class="source-line">Reading: Fogler §§15.3.4, 15.5 and 15.6.1. The direct film balance below fixes the geometric and volume basis. {cite("F5","F10","F7")}</p>')
after_heading('q6',f'<p class="source-line">Source match: this is Levenspiel Problem 18.31. The inverse-size rate scaling is derived in §18.3, Eq. (25). {cite("L4","L2")}</p>')
after_heading('q7',f'<p class="source-line">Reading: Levenspiel §18.2 for the one-dimensional first-order solution; §18.3 and Fogler §15.3.3 for reaction-order effects. The derivation below starts from the given slab equation. {cite("L1","L3","F9","T")}</p>')
after_heading('q8',f'<p class="source-line">Reading: Levenspiel §18.3, Eqs. (13), (20)–(23), and Fig. 18.6; Fogler Fig. 15-5(b). {cite("L2","F4")}</p>')

# Additional derivations and interpretation are attached immediately to their
# respective worked problem, preserving all verified numerical tables/plots.
append_to('q1',f'''<h3>Why the calculation has three separate stages</h3>
<p><b>Stage 1: fluid-scale transport.</b> Molecular diffusion describes collisions between gas molecules. Knudsen diffusion describes repeated encounters with pore walls when the pore is narrow compared with the molecular mean free path. Their relative importance can change with pressure, even though the pore radius remains fixed. {cite('F1')}</p>
<p><b>Stage 2: combine mechanisms using the relation supplied.</b> The reciprocal addition says that both mechanisms impede the same transport. For the tutorial’s model, “resistance” is proportional to 1/D. Solving the reciprocal equation by multiplying through by DD<sub>AB</sub>D<sub>K</sub> yields D(D<sub>AB</sub> + D<sub>K</sub>) = D<sub>AB</sub>D<sub>K</sub>. This explains why an arithmetic average would be wrong. The supplied relation is the assumed model for this exercise, not a full multicomponent reacting-gas transport model. {cite('T')}</p>
<p><b>Stage 3: pellet-scale geometry.</b> Only a fraction ε of the pellet is open pore space; winding paths increase travel distance; narrow throats reduce transport further. Those effects make the effective pellet diffusivity smaller than the combined pore-fluid diffusivity. Follow the problem’s stated τ convention rather than adding an extra square to tortuosity. {cite('F2')}</p>
<div class="eq">At 1 atm: D = [1/0.860 + 1/0.0659839]<sup>−1</sup> = [1.16279 + 15.1552]<sup>−1</sup><br>At 10 atm: D = [1/0.0860 + 1/0.0659839]<sup>−1</sup> = [11.6279 + 15.1552]<sup>−1</sup></div>
<p>The Knudsen contribution to total reciprocal resistance is (1/D<sub>K</sub>)/(1/D<sub>AB</sub> + 1/D<sub>K</sub>) = 92.87% at 1 atm and 56.58% at 10 atm. Increasing pressure tenfold therefore does not decrease the combined diffusivity tenfold: only the molecular contribution has that pressure dependence.</p>
<div class="note"><b>Common mistakes:</b> use the <em>pore radius</em> 50 Å, not a catalyst-pellet radius; convert Å to cm before using the 9.70 × 10³ coefficient; use kelvin in √T; and remember 1 cm²/s = 10⁻⁴ m²/s, not 10⁻² m²/s.</div>
<p><b>Limiting checks.</b> If D<sub>AB</sub> ≫ D<sub>K</sub>, then D ≈ D<sub>K</sub>. If D<sub>K</sub> ≫ D<sub>AB</sub>, then D ≈ D<sub>AB</sub>. The calculated numbers satisfy both the ordering D &lt; min(D<sub>AB</sub>,D<sub>K</sub>) and D<sub>e</sub> = 0.08D.</p>''')

append_to('q2',f'''<h3>Where the diagnostic expression comes from</h3>
<p>For this second-order reaction, the hypothetical uniform-concentration pellet would have q<sub>int,s</sub> = kC<sub>As</sub>². Thus η = q<sub>v</sub>/(kC<sub>As</sub>²). The corresponding radius-based Thiele modulus obeys Φ₂² = kC<sub>As</sub>R²/D<sub>e</sub>. Multiplying cancels the unknown k:</p>
<div class="eq">ηΦ₂² = [q<sub>v</sub>/(kC<sub>As</sub>²)] [kC<sub>As</sub>R²/D<sub>e</sub>]<br>= q<sub>v</sub>R²/(D<sub>e</sub>C<sub>As</sub>) = C<sub>WP</sub></div>
<p>This is why a measured rate is sufficient to test for internal transport resistance even though the intrinsic rate constant is unavailable. The cancellation is valid with consistently defined rate and modulus; the <em>first-order spherical formula for η</em> is not valid for this second-order pellet. {cite('F5','F9')}</p>
<h3>Unit-by-unit check</h3><div class="eq">ρ<sub>p</sub> = 2.2 (g/cm³) × (1 kg/1000 g) × (10⁶ cm³/m³) = 2200 kg/m³<br>[q<sub>v</sub>R²] = (mol m⁻³ h⁻¹)(m²) = mol m⁻¹ h⁻¹<br>[D<sub>e</sub>C<sub>As</sub>] = (m² h⁻¹)(mol m⁻³) = mol m⁻¹ h⁻¹</div>
<p>The two units cancel, as they must. Using R = 0.5 mm would incorrectly quadruple C<sub>WP</sub>. Using the numerical density 2.2 alongside a rate per kilogram and SI diffusivity would understate the parameter by 1000.</p>
<h3>Interpret the answer without overclaiming</h3><p>Using Levenspiel’s length ℓ = V/S = R/3 gives M<sub>W</sub> = 1527.78, far above his strong-resistance guide value of 4. The result is nowhere near a borderline regime, so reasonable order-dependent changes in a practical screening threshold cannot change the conclusion. {cite('L2')}</p>
<p>The test diagnoses severe internal concentration gradients under the stated transport model. It does not provide an exact second-order η or prove that all other resistances are absent. To identify external limitation independently, one would need a film coefficient or suitable flow-variation data, as in Q5.</p>
<div class="result"><strong>One-sentence answer:</strong> the observed rate is extremely large relative to the pore-diffusion capacity q<sub>D</sub> = D<sub>e</sub>C<sub>As</sub>/R², giving C<sub>WP</sub> = 1.375 × 10⁴; strong pore diffusion resistance is indicated.</div>''')

append_to('q3',f'''<h3>Derive the equation that is solved numerically</h3>
<p>Let z = Φ₂ for the smaller sphere. The larger sphere then has Φ₁ = 10z. Substitution into the exact expression gives:</p>
<div class="eq">η(10z)/η(z) = [(10z coth 10z − 1)/(100z²)] / [(z coth z − 1)/z²]<br>= (10z coth 10z − 1)/[100(z coth z − 1)] = 0.2<br>Equivalently: <b>(z coth z − 1)/(10z coth 10z − 1) = 0.05</b></div>
<p>The final form is the equation used in Fogler Example 15-2. Its positive solution is z = 1.64561383. One can bracket it between z = 1 and z = 2 and repeatedly bisect the interval, or use a numerical root finder. This solves the finite-size problem rather than assuming in advance which run is diffusion limited. {cite('F6')}</p>
<h3>Check the regime using both book conventions</h3><div class="table-wrap"><table><thead><tr><th>Run</th><th>φ = Φ/3</th><th>M<sub>W</sub> = C<sub>WP</sub>/9</th><th>Levenspiel interpretation</th></tr></thead><tbody><tr><td>1</td><td>5.48538</td><td>5.15205</td><td>Above the strong-resistance guide values φ &gt; 4 and M<sub>W</sub> &gt; 4.</td></tr><tr><td>2</td><td>0.548538</td><td>0.257602</td><td>Intermediate: above the negligible-resistance guide but well below strong resistance.</td></tr></tbody></table></div>
<p>The exact η₂ = 0.8561 means a 14.39% rate reduction relative to the intrinsic rate at the same surface concentration. Calling Run 2 “not strongly limited” is justified; calling it “completely diffusion-free” would be too strong. {cite('L2')}</p>
<h3>Why the book shows about 0.182 for the large pellet</h3><p>Fogler rounds Φ₁ to 16.5 and then uses the asymptote η ≈ 3/Φ₁, giving 3/16.5 = 0.1818. The exact expression also contains the negative 3/Φ₁² term:</p>
<div class="eq">η(Φ₁) = 3 coth Φ₁/Φ₁ − 3/Φ₁²<br>At Φ₁ = 16.4561: η<sub>exact</sub> = 0.171225; &nbsp; 3/Φ₁ ≈ 0.182303</div>
<p>The asymptote is about 6.5% high here. This solution retains the exact result, which reproduces η₁/η₂ = 0.200000. The difference from the book’s displayed 0.182 is an approximation difference, not a different physical conclusion. {cite('F4','F6')}</p>
<div class="note"><b>Why no concentration was needed:</b> it cancels only because C<sub>As</sub>, k and the catalyst properties are common to the two runs. The source example explicitly says identical conditions and negligible external resistance. The tutorial leaves that wording implicit; the solution states it instead of assigning an arbitrary concentration.</div>''')

append_to('q4',f'''<h3>Derive the spherical profile rather than memorising it</h3>
<p>For a first-order reaction in a sphere, the steady material balance with constant D<sub>e</sub> is D<sub>e</sub>[C″ + (2/r)C′] − kC = 0. The extra (2/r)C′ term appears because the diffusion area changes as 4πr². With u = C/C<sub>As</sub> and ξ = r/R:</p>
<div class="eq">u″ + (2/ξ)u′ − Φ²u = 0, &nbsp; Φ² = kR²/D<sub>e</sub><br>Let y = ξu. Then u″ + (2/ξ)u′ = y″/ξ, so y″ − Φ²y = 0.<br>y = A sinh(Φξ) + B cosh(Φξ)</div>
<p>A finite centre concentration requires y(0) = 0, otherwise u = y/ξ would diverge. Hence B = 0. The surface condition u(1) = 1 gives A = 1/sinh Φ. Therefore u = sinh(Φξ)/(ξ sinh Φ), exactly the radius-based formula used above. {cite('F3')}</p>
<p>At ξ = 0 the displayed expression looks like 0/0, but its limit is finite: u(0) = Φ/sinh Φ. Near the centre its expansion is u(ξ) = [Φ/sinh Φ][1 + Φ²ξ²/6 + …], so u′(0) = 0 as symmetry requires.</p>
<h3>Derive the effectiveness factor from the surface flux</h3><p>The outward coordinate has dC/dr &gt; 0 because concentration increases toward the surface. Fick’s law therefore gives an inward, negative outward flux N<sub>A,r</sub> = −D<sub>e</sub>dC/dr. Its inward magnitude, multiplied by area, equals the total reaction rate.</p>
<div class="eq">Q<sub>A</sub> = 4πR²D<sub>e</sub>(dC/dr)<sub>R</sub> = 4πRD<sub>e</sub>C<sub>As</sub>u′(1)<br>u′(1) = Φ coth Φ − 1<br>η = Q<sub>A</sub> / [(4πR³/3)kC<sub>As</sub>] = 3(Φ coth Φ − 1)/Φ²</div>
<p>This is Fogler Eq. (15-32). It explains both the factor of three and why the surface concentration cancels from η for first-order kinetics. The target η = 0.8 is a design condition for the <em>new</em> pellet; it cannot be used as if it described the original pellet. {cite('F4')}</p>
<h3>Textbook-based completion of the missing datum — conditional</h3>
<p>Fogler P15-5B closely matches the tutorial’s wording and supplies <b>C(R/2) = 0.1C<sub>As</sub></b>. It uses diameter 0.002 cm and an inward distance 0.0003 cm, both 100 times smaller than the tutorial’s 0.2 cm and 0.03 cm. The relative evaluation position ξ = 0.7 is the same. The following calculation restores only the omitted concentration condition while keeping the tutorial’s dimensions. This is a supported interpretation of the likely intended problem, not a datum actually printed in the tutorial. {cite('F8','T')}</p>
<div class="eq">At ξ = 1/2: 0.1 = 2 sinh(Φ/2)/sinh Φ<br>Using sinh Φ = 2 sinh(Φ/2) cosh(Φ/2):<br>0.1 = 1/cosh(Φ/2)<br>Φ<sub>old</sub> = 2 arcosh(10) = <b>5.98644569</b></div>
<p>The missing intrinsic rate constant can now be inferred for the tutorial’s radius:</p>
<div class="eq">k = D<sub>e</sub>Φ<sub>old</sub>²/R<sub>old</sub>²<br>= (0.1)(5.98644569)²/(0.1)² = <b>358.37532 s⁻¹</b><br>C(0.07 cm) = 0.001 × sinh(0.7 × 5.98644569)/[0.7 sinh(5.98644569)]<br>= <b>2.370506 × 10⁻⁴ mol dm⁻³</b></div>
<p>Because k and D<sub>e</sub> stay the same after reducing the pellet, Φ is proportional to diameter. Use the ratio rather than performing another unit conversion:</p>
<div class="eq">d<sub>new</sub>/d<sub>old</sub> = Φ<sub>new</sub>/Φ<sub>old</sub><br>d<sub>new</sub> = 0.2 × 2.04207798/5.98644569<br>= <b>0.0682234 cm = 0.682234 mm</b></div>
<div class="result"><strong>If the source problem’s omitted condition is intended:</strong> part (a) gives C<sub>A</sub> = 2.371 × 10⁻⁴ mol dm⁻³; part (b) gives diameter 0.06822 cm. The original pellet has η ≈ 0.41743 and the resized pellet has η = 0.8. Without that condition or an independently supplied k, the parametric answers above remain the only unique conclusions.</div>
<p><b>Do not copy the book’s diameter directly.</b> Its answer is about 6.8 × 10⁻⁴ cm because its starting pellet is 100 times smaller. With the tutorial’s dimensions the conditional new diameter is 100 times larger. The concentration ratio is unchanged because both problems evaluate the same ξ and use the same restored Φ. The book’s concentration answer 2.36 × 10⁻⁴ mol dm⁻³ uses rounding; the value above follows the unrounded hyperbolic calculation. {cite('F8')}</p>
<p><b>Physical interpretation.</b> Reducing R lowers the diffusion time R²/D<sub>e</sub>, flattens the concentration profile and makes more of the internal platinum useful. The model assumes size reduction leaves k and D<sub>e</sub> unchanged; it does not account for a change in pore structure or catalyst loading during grinding.</p>''')

append_to('q5',f'''<h3>Why density, porosity, pressure and temperature do not all enter the arithmetic</h3>
<p>The data include more quantities than this diagnostic needs. The observed rate is already in mol/(h·m³ cat), which we interpret as per total pellet volume. Multiplying by 2800 kg/m³ would produce an incorrect extra mass factor. If desired, first converting q<sub>v</sub> to q<sub>m</sub> = 10⁵/2800 = 35.7143 mol/(kg·h), and then multiplying by the <em>same</em> pellet density in C<sub>WP</sub>, returns 10⁵ exactly. {cite('L2','F3')}</p>
<p>Porosity is already represented in the supplied effective D<sub>e</sub>. The listed pressure and temperature are useful experimental context, but C<sub>Ag</sub>, k<sub>g</sub> and D<sub>e</sub> are already specified at the measurement conditions. Re-estimating those quantities is unnecessary.</p>
<h3>Derive the surface concentration from conservation</h3>
<p>At steady state, every mole entering the pellet across its exterior must be consumed inside. Let the positive inward flux be j<sub>A</sub> = k<sub>g</sub>(C<sub>Ag</sub> − C<sub>As</sub>). The rate demand of one sphere is q<sub>v</sub>V<sub>p</sub>. Therefore:</p>
<div class="eq">j<sub>A</sub> = q<sub>v</sub>V<sub>p</sub>/S<sub>p</sub> = q<sub>v</sub>R/3<br>= (10⁵)(0.0012)/3 = 40 mol m⁻² h⁻¹<br>C<sub>Ag</sub> − C<sub>As</sub> = 40/300 = 0.133333 mol m⁻³</div>
<p>This is a direct conservation statement, independent of an empirical screening threshold. The film can support a maximum flux k<sub>g</sub>C<sub>Ag</sub> = 6000 mol m⁻² h⁻¹ if C<sub>As</sub> were zero; the actual demand of 40 is only 0.667% of that maximum. There is consequently very little concentration loss across the film. {cite('F10')}</p>
<h3>How the Mears number relates to that drop</h3>
<div class="eq">δ = (C<sub>Ag</sub> − C<sub>As</sub>)/C<sub>Ag</sub> = q<sub>v</sub>R/(3k<sub>g</sub>C<sub>Ag</sub>)<br>C<sub>M,pellet</sub> = nq<sub>v</sub>R/(k<sub>g</sub>C<sub>Ag</sub>) = 3nδ</div>
<p>For small δ, a local power-law rate evaluated at the surface differs from that evaluated at the bulk by roughly nδ. Thus C<sub>M</sub> &lt; 0.15 corresponds to a small film-induced rate change on this spherical radius convention. Here n = 1 and C<sub>M</sub> = 0.02 gives δ = 0.006667 exactly.</p>
<div class="note"><b>Book notation and density basis.</b> Fogler Eq. (15-62) prints q<sub>m</sub>ρ<sub>b</sub>Rn/(k<sub>c</sub>C<sub>Ab</sub>) and labels ρ<sub>b</sub> as bed bulk density. This worksheet supplies a pellet-volume rate and pellet porosity, not a bed void fraction. The 0.0200 above is explicitly the <em>pellet-volume, radius-based screen</em>, supported independently by the exact single-pellet film balance. If a bed-basis number is required under Fogler’s printed convention, q<sub>bed</sub> = (1 − ε<sub>b</sub>)q<sub>v</sub> and MR<sub>bed</sub> = (1 − ε<sub>b</sub>) × 0.0200, also below 0.15 for any physical ε<sub>b</sub>. Do not substitute the pellet’s internal porosity ε<sub>p</sub> = 0.4 for the unspecified bed void fraction ε<sub>b</sub>. {cite('F7')}</div>
<h3>Why internal diffusion can be strong while the film drop is tiny</h3>
<p>External transport has a large k<sub>g</sub> and needs only a small concentration difference to supply the pellet. Internal transport must carry that reactant through tortuous pores with a small D<sub>e</sub>. Different resistances can therefore have very different strengths in the same experiment. Using the measured rate with the slightly corrected surface concentration gives C<sub>WP</sub> = 144.966, or M<sub>W</sub> = 16.1074; both show severe internal resistance in their respective conventions. {cite('F5','L2')}</p>
<details><summary>Optional quantitative check: infer internal effectiveness</summary><p>For the assumed first-order spherical model, C<sub>WP</sub> = 3(Φ coth Φ − 1). Its value 144.966 implies Φ ≈ 49.3221; coth Φ is indistinguishable from 1 at this size. Hence η = C<sub>WP</sub>/Φ² ≈ 0.05959. The model therefore predicts only about 6% internal effectiveness while losing less than 1% concentration across the film. This inference is additional to the requested criteria, not an extra experimental measurement.</p></details>
<div class="result"><strong>Final classification:</strong> strong internal pore diffusion; negligible external mass-transfer influence under the stated isothermal model. The criteria do not test heat-transfer limitations, for which thermal data would be required.</div>''')

append_to('q6',f'''<h3>Derive the 1/diameter dependence</h3>
<p>For a strongly diffusion-limited first-order sphere, η ≈ 3/Φ and Φ = R√(k/D<sub>e</sub>). Therefore:</p>
<div class="eq">q<sub>v</sub> = ηkC<sub>As</sub> ≈ (3/R)√(kD<sub>e</sub>) C<sub>As</sub><br>q<sub>m</sub> = q<sub>v</sub>/ρ<sub>p</sub> ≈ [3√(kD<sub>e</sub>)/(ρ<sub>p</sub>R)]C<sub>As</sub><br>Define k′<sub>app</sub> = 3√(kD<sub>e</sub>)/(ρ<sub>p</sub>R). Then k′<sub>app</sub> ∝ 1/R ∝ 1/d.</div>
<p>At fixed total catalyst mass, larger pellets mean less exterior area available for the active near-surface layer. This lowers the rate per unit catalyst mass. The total rate of <em>one</em> larger pellet may still be larger, but the bed contains fewer of those pellets. The mass-specific rate is what belongs in the catalyst-weight reactor equation. {cite('F4','L2')}</p>
<h3>Derive conversion from the catalyst-weight mole balance</h3>
<p>For a plug-flow packed bed with catalyst mass coordinate W, F<sub>A0</sub>dX/dW = q<sub>m</sub>. With A → R at constant temperature and pressure, no net molar expansion and unchanged volumetric feed rate v₀, C<sub>A</sub> = C<sub>A0</sub>(1 − X). Negligible external resistance makes C<sub>As</sub> ≈ C<sub>A</sub>.</p>
<div class="eq">F<sub>A0</sub> dX/dW = k′<sub>app</sub>C<sub>A0</sub>(1 − X)<br>Since F<sub>A0</sub> = v₀C<sub>A0</sub>: dX/(1 − X) = (k′<sub>app</sub>/v₀)dW<br>Integrating from X = 0 to X and W = 0 to W:<br><b>−ln(1 − X) = k′<sub>app</sub>W/v₀</b></div>
<p>The inlet concentration cancels because the reaction is first order. Under unchanged W/v₀, the integrated exponent halves when the pellet diameter doubles. The original value is −ln(0.368) = 0.999672, very close to one; the new value is 0.499836.</p>
<h3>Useful general form and sanity checks</h3><div class="eq">X₂ = 1 − (1 − X₁)<sup>d₁/d₂</sup> &nbsp; under the same strong-diffusion assumptions</div>
<p>When d₂ = d₁, this returns X₂ = X₁. If d₂ increases, the exponent decreases and conversion falls. Conversely, halving the diameter while remaining strongly limited gives X₂ = 1 − 0.368² = 86.46%. The latter scaling eventually fails if size reduction brings the pellets out of the strong-diffusion regime; η cannot grow above one.</p>
<p>The answer 39.3% is the intended result for Levenspiel Problem 18.31. Actual pressure-drop improvement might partly compensate for the rate loss in a real gas-phase reactor, but no pressure profile, flow adjustment or bed-packing change is given here. The tutorial’s numerical comparison therefore holds those influences fixed. {cite('L4')}</p>''')

append_to('q7',f'''<h3>Build the slab equation from a material balance</h3>
<p>Take a thin slice of thickness dx and constant area A<sub>c</sub>. Let N<sub>A</sub> be the molar flux in the positive x-direction, with x increasing from the centre to the surface. At steady state, inflow minus outflow minus consumption is zero:</p>
<div class="eq">N<sub>A</sub>(x)A<sub>c</sub> − N<sub>A</sub>(x + dx)A<sub>c</sub> − kC<sub>A</sub><sup>n</sup>A<sub>c</sub>dx = 0<br>Divide by A<sub>c</sub>dx and take dx → 0:<br>−dN<sub>A</sub>/dx − kC<sub>A</sub><sup>n</sup> = 0<br>With N<sub>A</sub> = −D<sub>e</sub>dC<sub>A</sub>/dx:<br><b>D<sub>e</sub>d²C<sub>A</sub>/dx² − kC<sub>A</sub><sup>n</sup> = 0</b></div>
<p>The slab has a constant diffusion area, so it has no spherical 2C′/r term. The same one-dimensional balance underlies Levenspiel’s single-pore model after converting the wall-area rate constant into a volume-based rate constant. The mathematical profile is the same, although a single cylindrical pore and a homogenised flat porous pellet are different physical models. {cite('L1')}</p>
<h3>Non-dimensionalise each term explicitly</h3>
<div class="eq">C<sub>A</sub> = C<sub>As</sub>u, &nbsp; x = Lξ<br>dC<sub>A</sub>/dx = (C<sub>As</sub>/L) du/dξ<br>d²C<sub>A</sub>/dx² = (C<sub>As</sub>/L²) d²u/dξ²<br>D<sub>e</sub>(C<sub>As</sub>/L²)u″ − kC<sub>As</sub><sup>n</sup>u<sup>n</sup> = 0<br><b>u″ − [kL²C<sub>As</sub><sup>n−1</sup>/D<sub>e</sub>]u<sup>n</sup> = 0</b></div>
<p>The bracket is φ² for this question. Since kC<sub>As</sub><sup>n−1</sup> has units time⁻¹, φ is dimensionless for every reaction order. The boundary u(1) = 1 fixes the surface concentration; u′(0) = 0 follows from mirror symmetry at the centre plane. It does <em>not</em> set the centre concentration to zero.</p>
<p>Levenspiel measures distance from the pore entrance, giving cosh[m(L − x)]/cosh(mL). Here distance is measured from the symmetry plane, giving cosh(φξ)/cosh φ. Reversing the coordinate explains the apparent difference; the physical profile is identical. {cite('L1')}</p>
<h3>What the boundary-value solver actually solves</h3>
<p>A second-order equation is converted to two first-order equations by introducing v = u′. The unknowns are the two functions u(ξ) and v(ξ):</p>
<div class="eq">y₀ = u, &nbsp; y₁ = v = u′<br>dy₀/dξ = y₁<br>dy₁/dξ = φ²y₀<sup>n</sup><br>Boundary residual vector = [y₁(0), &nbsp; y₀(1) − 1]</div>
<p>The residual vector must be zero. Unlike an initial-value problem, we do not know both u and u′ at ξ = 0: the centre value u(0) must be found so that u(1) becomes one. The boundary-value solver adjusts the whole profile and its mesh to satisfy the differential equations and both end conditions.</p>
<ol><li><b>Start at weak reaction.</b> At φ = 0.1, u ≈ 1 and v ≈ 0 are sensible initial guesses.</li><li><b>Increase φ gradually.</b> Continuation solves a sequence from 0.1 to the target φ, using the preceding solution as the next guess. This avoids asking the solver to discover a thin φ = 100 surface layer from a flat initial guess.</li><li><b>Resolve the surface.</b> The code combines a uniform mesh with extra points near ξ = 1. At large φ the profile changes over a dimensionless thickness of order 1/φ.</li><li><b>Keep fractional powers real during iteration.</b> Trial values can dip slightly below zero, so the iteration evaluates max(u,0)<sup>n</sup>. This is numerical protection, not permission for a negative final concentration.</li><li><b>Check convergence and physical behaviour.</b> The solver must report success; the boundary values, nonnegative concentration within tolerance, monotonicity, conservation and first integral are checked. A solver failure is raised instead of silently plotting a failed result.</li></ol>
<h3>Derive two independent checks on the numerical solution</h3>
<p><b>Integrated material balance.</b> Integrating u″ = φ²u<sup>n</sup> from 0 to 1 and using u′(0) = 0 gives:</p>
<div class="eq">u′(1) = φ²∫₀¹u<sup>n</sup>dξ<br>For a slab: η = ∫₀¹u<sup>n</sup>dξ = <b>u′(1)/φ²</b></div>
<p>The left expression for η measures total reaction in the slab; the right expression measures the reactant flux through its surface. At steady state they must agree. This check is useful for nonlinear profiles even when no closed-form full solution is available.</p>
<p><b>First integral.</b> Multiply the ODE by 2u′. Then d(u′²)/dξ = 2φ²u<sup>n</sup>u′. Integrate from the centre, where u′ = 0 and u = u₀:</p>
<div class="eq"><b>u′² = [2φ²/(n + 1)](u<sup>n+1</sup> − u₀<sup>n+1</sup>)</b><br>At the surface: u′(1) = φ√{{2[1 − u₀<sup>n+1</sup>]/(n + 1)}}<br>η = √{{2[1 − u₀<sup>n+1</sup>]/(n + 1)}}/φ</div>
<p>This identity is exact for the stated slab equation and nonnegative profile. It checks the computed concentration and gradient point by point. In the strong-diffusion limit u₀ becomes negligible, recovering η ≈ √[2/(n + 1)]/φ. This is the flat-geometry counterpart of the strong-diffusion expression discussed in the books. {cite('F9','L3')}</p>
<h3>Derive the dead-core solution for 0 &lt; n &lt; 1</h3>
<p>Suppose reactant reaches zero at ξ = ξ₀ before reaching the centre. In the core, u = 0 and the reaction rate kC<sup>n</sup> is also zero. At the edge of the active layer, both u and u′ must vanish so there is no reactant flux leaking into the zero-concentration region. Set u₀ = 0 in the first integral on this active branch:</p>
<div class="eq">du/dξ = φ√[2/(n + 1)] u<sup>(n+1)/2</sup><br>u<sup>−(n+1)/2</sup>du = φ√[2/(n + 1)] dξ<br>[2/(1 − n)]u<sup>(1−n)/2</sup> = φ√[2/(n + 1)](ξ − ξ₀)<br>u = {{[φ(1 − n)/√(2(n + 1))](ξ − ξ₀)}}<sup>2/(1−n)</sup></div>
<p>Putting u(1) = 1 gives 1 − ξ₀ = √[2(n + 1)]/[φ(1 − n)]. A dead core can fit inside the half-slab only when ξ₀ ≥ 0, which yields φ ≥ φ<sub>crit</sub>. For n = 0.5 and φ = 100, the resulting ξ₀ and fourth-power profile are the exact piecewise expressions already used in the plotted solution.</p>
<p>This is why simply applying the first-order cosh profile to n = 0.5 would be wrong. It is also why an unqualified positive-profile solver can struggle on this branch. For n ≥ 1, the integral distance required to reach exactly zero diverges; the finite-slab solution remains positive, although first-order centre values may be extraordinarily small.</p>
<div class="note"><b>Numerical precision is not physical zero.</b> For n = 1 and φ = 100, u(0) = 7.44015 × 10⁻⁴⁴ analytically. A solver controlled by an absolute tolerance near 10⁻⁷ cannot claim high relative accuracy at that tiny concentration. The plotted shape and surface flux are accurate; the table uses the analytic centre value. For n = 0.5, the zero core is instead an exact feature of the model.</div>
<h3>Interpret concentration, gradient and flux separately</h3>
<p>Every physical profile rises toward the exterior, so u′ ≥ 0. Its curvature satisfies u″ = φ²u<sup>n</sup> ≥ 0, which means the slope increases outward. The dimensionless gradient returned by the script is u′. The dimensional concentration gradient is (C<sub>As</sub>/L)u′, while the outward molar flux is −(D<sub>e</sub>C<sub>As</sub>/L)u′. The negative sign states that reactant actually travels inward.</p>
<p>At φ = 0.1 a regular expansion gives u(ξ) ≈ 1 − (φ²/2)(1 − ξ²). To leading order, this is independent of n, explaining why all the low-φ curves nearly overlap. At high φ, order differences become visible because much of the pellet has u well below one. A lower n gives a larger u<sup>n</sup> at the same sub-unity u and consumes reactant more strongly there.</p>
<div class="result"><strong>Suggested interpretation in your own words:</strong> at low Thiele modulus, diffusion keeps almost the whole pellet close to the surface concentration. At high modulus, reaction consumes A near the surface before it reaches the interior. At equal dimensionless φ, higher reaction orders allow deeper concentration penetration, but their effectiveness factor can still be lower because effectiveness averages u<sup>n</sup>. Half-order kinetics at φ = 100 produce a finite zero-concentration core.</div>''')

append_to('q8',f'''<h3>Derive the characteristic length for each shape</h3>
<p>The characteristic length ℓ = V<sub>p</sub>/S<sub>p</sub> uses only exterior area through which reactant can enter. Consider a wide plate of total thickness 2L, a long cylinder of radius R and length H, and a sphere of radius R. Edge effects of the plate and end effects of the cylinder are neglected. {cite('L2')}</p>
<div class="eq">Plate: ℓ = (2LA)/(2A) = L<br>Cylinder: ℓ = (πR²H)/(2πRH) = R/2<br>Sphere: ℓ = (4πR³/3)/(4πR²) = R/3</div>
<p>These factors explain why the arguments in the three exact formulas are φ, 2φ and 3φ. They do not mean the cylinder or sphere has a different physical diffusion coefficient.</p>
<h3>Flat plate: integrate the first-order profile</h3>
<div class="eq">u(ξ) = cosh(φξ)/cosh φ<br>η = ∫₀¹u(ξ)dξ = [sinh(φξ)/(φ cosh φ)]₀¹<br><b>η<sub>plate</sub> = tanh φ/φ</b></div>
<p>The volume average is simply an integral in ξ because every slice has the same area. This is the same expression derived in Q7 for n = 1. {cite('L1','L2')}</p>
<h3>Sphere: substitute the V/S-based modulus consistently</h3>
<p>Q4 derived η = 3(Φ coth Φ − 1)/Φ² with Φ = R√(k/D<sub>e</sub>). The Q8 modulus is φ = Φ/3, so:</p>
<div class="eq">η<sub>sphere</sub> = 3[(3φ)coth(3φ) − 1]/(3φ)²<br>= <b>[3φ coth(3φ) − 1]/(3φ²)</b><br>= (1/φ)[1/tanh(3φ) − 1/(3φ)]</div>
<p>The last line is the form printed by Levenspiel, Eq. (22); the middle line is the tutorial’s form. Their algebraic equality verifies that the worksheet’s Q8 formula is consistent even though its Q4 profile definition is not. {cite('L2','F4')}</p>
<h3>Long cylinder: why modified Bessel functions appear</h3>
<p>For radial diffusion in a long cylinder, the area varies as r rather than r². With s = r/R and α = R√(k/D<sub>e</sub>), the governing equation is:</p>
<div class="eq">u″ + (1/s)u′ − α²u = 0<br>u(s) = A I₀(αs) + B K₀(αs)</div>
<p>I₀ and K₀ are the two independent modified Bessel solutions. K₀ diverges at the axis, so a finite centre concentration requires B = 0. Enforcing u(1) = 1 gives u = I₀(αs)/I₀(α). Because dI₀(z)/dz = I₁(z), the surface gradient is u′(1) = αI₁(α)/I₀(α).</p>
<div class="eq">Q<sub>A</sub> = (2πRH)D<sub>e</sub>(C<sub>As</sub>/R)u′(1)<br>Ideal rate = (πR²H)kC<sub>As</sub><br>η = [2/α²]u′(1) = 2I₁(α)/[αI₀(α)]<br>Since α = 2φ: <b>η<sub>cylinder</sub> = I₁(2φ)/[φI₀(2φ)]</b></div>
<p>This derives the expression tabulated in Levenspiel Eq. (21), and explains the role of both the factor two and the ratio of Bessel functions. There is no need to memorise a separate unexplained cylinder correction. {cite('L2')}</p>
<h3>Check both asymptotic limits</h3>
<div class="table-wrap"><table><thead><tr><th>Shape</th><th>Small φ, leading departure from 1</th><th>Large φ, leading terms</th></tr></thead><tbody>
<tr><td>Plate</td><td>η = 1 − φ²/3 + …</td><td>η ≈ 1/φ</td></tr>
<tr><td>Cylinder</td><td>η = 1 − φ²/2 + …</td><td>η ≈ 1/φ − 1/(4φ²)</td></tr>
<tr><td>Sphere</td><td>η = 1 − 3φ²/5 + …</td><td>η ≈ 1/φ − 1/(3φ²)</td></tr></tbody></table></div>
<p>These series follow by expanding the exact formulas, and explain the ordering of the curves at equal φ. As φ becomes very large, the differences between shapes shrink relative to the common 1/φ term. A physical estimate gives the same leading result: the reacting layer is about δ ≈ √(D<sub>e</sub>/k) thick; its volume is approximately S<sub>p</sub>δ; dividing by the whole pellet volume yields η ≈ δ/(V<sub>p</sub>/S<sub>p</sub>) = 1/φ.</p>
<h3>How the code avoids numerical problems</h3>
<p>The plotted range is φ = 1–100, sampled at 1000 points. The sphere uses coth(3φ) = 1/tanh(3φ), avoiding separate evaluation of large sinh and cosh values. The cylinder uses exponentially scaled Bessel functions:</p>
<div class="eq">ive(ν,z) = exp(−|z|) I<sub>ν</sub>(z), for the real positive z used here<br>ive(1,2φ)/ive(0,2φ) = I₁(2φ)/I₀(2φ)</div>
<p>The exponential factors cancel exactly in the ratio. φ = 0 is outside the requested plot, so there is no division by zero. If the plot is extended to zero, set η(0) = 1 by continuity or use the small-φ series instead of substituting zero directly.</p>
<div class="note"><b>Compare like with like.</b> Equal plotted φ means equal ℓ√(k/D<sub>e</sub>), not equal radius R and plate half-thickness L. At the same numerical R = L, the plate, cylinder and sphere have different φ. Their plotted ordering cannot be read as a universal claim that one shape is always best under every size, mass or pressure-drop constraint.</div>
<div class="result"><strong>Suggested interpretation:</strong> increasing the reaction-to-diffusion ratio reduces η for every shape. At weak reaction the whole pellet is supplied and η approaches one. At strong reaction only a surface layer is used; the common V/S-based modulus makes all three curves approach 1/φ. Shape matters most in the intermediate regime.</div>''')

append_to('code','''<h3>A guide to the script’s main objects</h3><div class="table-wrap"><table><thead><tr><th>Code name</th><th>Meaning</th></tr></thead><tbody>
<tr><td><code>sphere_eta(Phi)</code></td><td>Exact radius-based spherical effectiveness used in Q3–Q4. Its small-argument series avoids cancellation.</td></tr>
<tr><td><code>q1_to_q6()</code></td><td>Recomputes the arithmetic and root solves for the first six problems. Q4’s restored source condition is labelled conditional.</td></tr>
<tr><td><code>first_order(x, phi)</code></td><td>Stable analytical cosh ratio. Exponential arguments are non-positive for 0 ≤ x ≤ 1, avoiding overflow.</td></tr>
<tr><td><code>slab_profile(n, phi, x)</code></td><td>Returns u and du/dξ at the coordinates in x; handles an exact dead core when appropriate.</td></tr>
<tr><td><code>mesh</code></td><td>Solver coordinates. The solver can add points; a refreshed mesh helps prevent unnecessary node accumulation during continuation.</td></tr>
<tr><td><code>guess</code></td><td>A two-row array: row 0 contains u estimates and row 1 contains u′ estimates at every mesh point.</td></tr>
<tr><td><code>bc(ya, yb)</code></td><td>Returns the centre-gradient and surface-concentration errors. The solver seeks both equal to zero.</td></tr>
<tr><td><code>sol.sol(x)</code></td><td>Evaluates the converged continuous solution on the dense plotting grid.</td></tr>
<tr><td><code>simpson(..., x=x)</code></td><td>Numerically integrates uⁿ to obtain slab η and compare it with the surface-flux expression.</td></tr>
<tr><td><code>ive</code></td><td>Scaled modified Bessel function, used in the cylinder effectiveness ratio.</td></tr>
</tbody></table></div>
<h3>Validation you can reproduce</h3><ol><li>Run the script. It prints the Q1–Q6 results and the analytical-profile errors for Q7(a).</li><li>For Q7(b), compare the printed surface gradient divided by φ² with η. They should agree to the displayed precision.</li><li>The script also checks the first-integral identity for numerical profiles, solver boundary residuals, monotonic concentration and a nonnegative profile within a tight absolute tolerance.</li><li>For Q8, it checks 0 &lt; η ≤ 1 and decreasing η over the entire requested interval.</li><li>Open the generated SVGs directly in a browser or vector editor. They are computed curves, not screenshots of software output.</li></ol>
<p>The solver has been checked for the tutorial’s specified n and φ values. It is not a universal solver for every possible kinetic law; a different rate law, nonisothermal pellet, variable diffusivity, or a value near a difficult branch transition requires fresh model and convergence checks.</p>''')

# Keep the quick-reference answer and opening summary aligned with the new,
# explicitly conditional numerical completion of Q4.
for tr in soup.find(id='answers').select('tbody tr'):
    if tr.find('td').get_text(strip=True)=='4':
        tr.find_all('td')[1].clear()
        tr.find_all('td')[1].append(parse('As printed: missing datum; target Φ = 2.04208. If C(R/2)/Cₛ = 0.1 from Fogler is restored: C = 2.3705 × 10⁻⁴ mol/dm³ and d<sub>new</sub> = 0.0682234 cm. '+cite('F8')))

Path(HERE/'expanded_stage.html').write_text(str(soup),encoding='utf-8')

def finish():
    """Finalize after all explanatory sections have been inserted."""
    global soup
    refs='<section id="references"><h2>References and local book pages</h2><p>Links below open the actual files in the parent course folder. The page after <code>#page=</code> is the PDF viewer’s one-based page number, not the printed book page. If a viewer ignores the page fragment, navigate manually using the listed PDF page.</p><ol class="references">'
    for key,(file,pdf,title,desc) in REFS.items():
        path=quote(file) if key=='T' else '../'+quote(file)
        refs+=f'<li id="ref-{key}"><b>[{key}] {title}.</b> {desc} <a href="{path}#page={pdf}" target="_blank" rel="noopener">Open local PDF at page {pdf}</a></li>'
    refs+='</ol><p>Only sources actually inspected for this revision are cited. The tutorial’s numerical correlations and supplied dimensions take priority over similar textbook problems; source-based additions are expressly labelled conditional.</p></section>'
    soup.find('footer').decompose()
    for node in list(parse(refs).contents): soup.find('main').append(node)
    soup.find('main').append(parse('<footer>Detailed study solution for CL24303 Tutorial 4. All figures are generated vector plots; calculations and Python are embedded. Prepared from the locally supplied tutorial, course planner, Fogler and Levenspiel. No internet connection is needed to read this file.</footer>'))
    for label,target in [('Reading','#reading'),('Concepts','#foundations'),('References','#references')]:
        a=soup.new_tag('a',href=target);a.string=label;soup.find('nav').append(a)
    soup.find('style').append(' .cite{font:600 12px/1.4 Segoe UI,sans-serif;white-space:nowrap;text-decoration:none;padding:2px 4px;border-radius:3px;background:#e6eeeb}.source-line{font-size:14px;color:var(--muted);border-bottom:1px dashed var(--line);padding-bottom:15px}.references{padding-left:24px}.references li{padding:14px 0;border-bottom:1px solid var(--line);scroll-margin-top:100px}.references li:target{background:#fff3df}nav{max-height:115px;overflow:auto}.derivation{background:#fff;padding:18px;border:1px solid var(--line)} @media print{.cite{background:none}.references{font-size:9pt}}')
    soup.find(id='code').find('h2').string='Runnable Python and how to read it'
    soup.find(id='code').find('p').string='The embedded script reproduces Q1–Q6 numerical results, then solves Q7 and generates the Q7–Q8 vector plots. Download it, install the dependencies and run it in a folder of your choice. Its numerical consistency checks run automatically.'
    OUT.write_text(str(soup),encoding='utf-8')
    print(f'Expanded {OUT}: {len(soup.get_text().split()):,} words, {len(soup.select("a.cite"))} in-text citations, {len(REFS)} reference entries.')

if __name__=='__main__':
    finish()
