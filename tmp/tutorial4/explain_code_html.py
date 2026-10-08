"""Embed the commented script and its reading guide into the existing solution."""
from pathlib import Path
import html
import io
import keyword
import runpy
import token
import tokenize
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
runpy.run_path(str(HERE/'expand_solutions.py'),run_name='__main__')
OUT=HERE.parents[1]/'Tutorial 4'/'Tutorial4_Solutions.html'
soup=BeautifulSoup(OUT.read_text(encoding='utf-8'),'html.parser')
code=(HERE/'tutorial4_code.py').read_text(encoding='utf-8')

guide='''<div id="code-reading-guide">
<h3>Start here: how to run and read the program</h3>
<p>The Python download is now a standalone teaching script: it contains its own setup instructions, assumptions, notation, units, function documentation and explanations beside each non-obvious calculation. Read it from top to bottom once, then follow the calls in the final block: <code>q1_to_q6()</code>, <code>q7()</code>, and <code>q8()</code>.</p>
<p>Save it as <code>tutorial4_code.py</code>. Open a terminal in the folder where you saved it. The command <code>python -m pip install numpy scipy matplotlib</code> runs Python’s package installer for that interpreter: NumPy supplies numeric arrays, SciPy supplies numerical solvers, and Matplotlib creates plots. Then <code>python tutorial4_code.py</code> executes the file. It prints results and saves four SVG files in the terminal’s current folder. Re-running replaces those four files. No plot window is expected because the script deliberately saves the figures. See the <a href="https://packaging.python.org/en/latest/tutorials/installing-packages/">Python package-installation guide</a> for setup details.</p>

<h3>Five Python ideas used throughout the script</h3>
<div class="table-wrap"><table><thead><tr><th>Syntax</th><th>What it means here</th><th>Why it matters</th></tr></thead><tbody>
<tr><td><code>1e-5</code>, <code>x**2</code></td><td>10⁻⁵ and x squared.</td><td><code>^</code> is not Python’s exponent operator; using it would change or break the calculation.</td></tr>
<tr><td><code>def f(x): ... return y</code></td><td>A named calculation with an input x and a returned output y.</td><td>A function keeps the equation separate from plotting, so it can be reused and checked.</td></tr>
<tr><td><code>np.array([0, 0.5, 1])</code></td><td>Three numbers stored together. Array arithmetic acts on each entry.</td><td><code>x**2</code> returns [0, 0.25, 1], allowing a whole concentration curve to be calculated at once.</td></tr>
<tr><td><code>y[0]</code>, <code>y[1]</code>, <code>y[:, -1]</code></td><td>Python indexing starts at zero. For the solver’s two-row array these select concentration, gradient, and both values at the last node.</td><td>Confusing the rows swaps the concentration and its derivative and changes the boundary conditions.</td></tr>
<tr><td><code>assert condition, 'message'</code></td><td>Stop with a readable error if a required check is false.</td><td>A completed plot is not proof of a correct solution. Do not run with <code>python -O</code>, which disables assertions.</td></tr>
</tbody></table></div>
<p><code>zip</code> pairs matching entries from parameter and colour lists; <code>lambda</code> makes a short one-expression function; <code>f'...{value:.8g}...'</code> inserts a value into printed text with eight significant digits. None of those display choices changes the stored full-precision calculation. For an introduction to arrays and their shapes, see <a href="https://numpy.org/doc/stable/user/absolute_beginners.html">NumPy’s beginner guide</a>.</p>

<h3>Trace one calculation from inputs to results</h3>
<ol><li><b>Q3, root finding:</b> the known radius ratio is 10 and the measured rate ratio is 3/15. <code>rate_ratio_error(z)</code> evaluates η(10z)/η(z) − 3/15. The correct small-pellet modulus makes this error zero. <code>brentq</code> searches between 0.01 and 10; these are bounds, not physical measurements. It combines a bracketed search with interpolation. <a href="https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brentq.html">SciPy: brentq</a>.</li>
<li><b>Q7, set the state:</b> <code>guess</code> has shape (2, 151). Row 0 guesses u at 151 positions; row 1 guesses u′ there. A guess helps the solver start; it is not an extra boundary condition.</li>
<li><b>Q7, translate the equation:</b> <code>ode</code> returns [u′, φ²uⁿ], because we replaced one second-order equation by two first-order equations. <code>bc</code> returns [u′(0), u(1) − 1]. Both errors must vanish. The centre concentration u(0) is an output.</li>
<li><b>Q7, converge:</b> solve weak reaction first, then gradually raise φ while reusing the preceding solution. This is <em>continuation</em>, a sequence of steady problems, not time evolution. The solver refines its mesh to resolve steep gradients. Its tolerance controls the scaled equation residual, not relative accuracy in a concentration near 10⁻⁴⁴. <a href="https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_bvp.html">SciPy: solve_bvp</a>.</li>
<li><b>Q7, evaluate and verify:</b> <code>sol.sol(x)</code> interpolates the converged state at the requested plotting positions. Check the first integral, integrate uⁿ, and compare that integral with u′(1)/φ². Those are independent descriptions of the same conservation law.</li>
<li><b>Q8, compare shapes:</b> a 1000-element φ array gives three 1000-element η arrays. Plot labels identify the common V/S-based modulus; the spherical radius-based value is three times larger.</li></ol>

<h3>Why these numerical choices were made</h3><div class="table-wrap"><table><thead><tr><th>Choice</th><th>Alternatives</th><th>Reason and trade-off</th></tr></thead><tbody>
<tr><td>Brent root search for Q3–Q4</td><td>Manual bisection; Newton iteration.</td><td>A bracket is available and no derivative is required. A wrong bracket must be corrected rather than hidden.</td></tr>
<tr><td>Boundary-value solver plus continuation</td><td>Shooting from an estimated centre concentration; a hand-built finite-difference system.</td><td>Both endpoint conditions are applied directly, and the library refines the mesh. There is more setup than an analytical formula, but nonlinear orders have no general cosh solution.</td></tr>
<tr><td>Exact piecewise dead core</td><td>Force a positive BVP solution; replace uⁿ by a smoothed approximation.</td><td>The exact branch obeys both the physics and the interface conditions. It applies to this particular power-law model; different kinetics need a fresh derivation.</td></tr>
<tr><td>Vector SVG output</td><td>Raster PNG; interactive GUI windows.</td><td>SVG scales cleanly and satisfies the no-screenshots requirement. Files must be opened separately. See the <a href="https://matplotlib.org/stable/users/explain/quick_start.html">Matplotlib quick-start guide</a> for figure/axis terminology.</td></tr>
</tbody></table></div>

<h3>Expected output and what the checks mean</h3>
<pre>Q2 C_WP=13750; M_W=1527.778
Q3 Phi1=16.4561383, Phi2=1.64561383, eta1=0.171224692, eta2=0.856123459
Q6 X2=0.393369964
n=0.5, phi=100: u(0)=0, eta=0.01154701, surface gradient=115.4701
Saved q7a.svg, q7b.svg, q7b_full.svg and q8.svg.</pre>
<p>This is a selection of the output; there are more lines for the other questions and cases. Last digits of numerical errors may vary with library versions. A successful run finishes without an exception. The n = 1 maximum absolute profile error must be below 10⁻⁶; reaction integral versus surface flux must differ by less than 2 × 10⁻⁷. Those are acceptance bounds; the observed first-order errors in this run are much smaller.</p>

<h3>Numerical debugging notes</h3>
<div class="note"><b>1. “The maximum number of mesh nodes is exceeded.”</b><p><b>Symptom:</b> an earlier n = 1.5, high-φ run exhausted the solver mesh. <b>Diagnosis:</b> adding continuation steps alone did not resolve it. <b>Cause identified:</b> carrying every adaptively inserted node into each later solve accumulated an unnecessarily large mesh. <b>Fix:</b> replace <code>mesh, guess = sol.x, sol.y</code> with a fresh uniform-plus-surface mesh and <code>guess = sol.sol(mesh)</code>. <b>Lesson:</b> inspect mesh growth and resolution where gradients are steep before only increasing a resource limit.</p></div>
<div class="note"><b>2. “RuntimeWarning: invalid value encountered in divide”</b><p><b>Symptom:</b> the first combined mesh triggered invalid division inside the solver. <b>Diagnosis:</b> the uniform and logarithmic grids can contain nearly equal floating-point coordinates. <b>Cause:</b> extremely small intervals undermine slope/residual calculations. <b>Fix:</b> round coordinates to 12 decimal places before sorting/removing duplicates with <code>np.unique</code>. <b>Lesson:</b> strict ordering and sensible mesh spacing are numerical requirements, not presentation details.</p></div>
<div class="note"><b>3. A check must use the actual centre</b><p><b>Issue found while documenting:</b> the earlier first-integral check used <code>u[0]</code> as the centre concentration. That was valid for the full-domain plotting grids, but a caller could request only ξ = 0.9–1. <b>Cause:</b> it confused the first requested output position with the physical boundary. <b>Fix:</b> explicitly evaluate <code>sol.sol(0)[0]</code>. <b>Lesson:</b> distinguish the solver domain from the positions at which results are requested. The full tutorial results are unchanged.</p></div>

<h3>Troubleshooting and safe changes</h3><div class="table-wrap"><table><thead><tr><th>What you see or want</th><th>What to do</th></tr></thead><tbody>
<tr><td><code>ModuleNotFoundError</code></td><td>Run the installation command with the same Python interpreter used to execute the script.</td></tr>
<tr><td>No plot window</td><td>Expected. Look for the four SVG files in the current working folder and open them in a browser.</td></tr>
<tr><td>Solver failure or failed assertion</td><td>Read the reported n and φ. Restore the tutorial values, check boundary conditions and units, and then investigate mesh or convergence. Do not delete the check to obtain a plot.</td></tr>
<tr><td>Almost coincident low-φ curves</td><td>Expected near-uniform concentrations. Use the expanded y-axis rather than changing the physical values.</td></tr>
<tr><td>Add another reaction order</td><td>Edit the order list in both Q7(b) plotting loops, and supply enough colours. <code>zip</code> stops at the shorter list, so an unmatched new order would otherwise be omitted.</td></tr>
<tr><td>Change the physical rate law</td><td>Revise the equation, boundary conditions where needed, and analytical checks. Editing n alone does not model heat release, variable diffusivity or adsorption kinetics.</td></tr>
</tbody></table></div>

<h3>Three short exercises</h3>
<p><b>Practice:</b> evaluate <code>sphere_eta(2.0420779775)</code>. Success means a result close to 0.8.</p><details><summary>Practice solution</summary><pre>from tutorial4_code import sphere_eta
print(sphere_eta(2.0420779775))  # Approximately 0.8.</pre></details>
<p><b>Check a profile:</b> request n = 1, φ = 1 at ξ = 0, 0.5 and 1. Verify u(1) = 1, u′(0) ≈ 0 and agreement with the exact profile.</p><details><summary>Profile solution</summary><pre>import numpy as np
from tutorial4_code import slab_profile, first_order
x = np.array([0.0, 0.5, 1.0])  # Dimensionless positions, not metres.
u, gradient = slab_profile(1, 1, x)
print(u)                      # About [0.648054, 0.730763, 1.000000].
print(gradient[0])            # Approximately zero by centre symmetry.
print(np.max(np.abs(u-first_order(x, 1))))  # A small absolute error.</pre></details>
<p><b>Challenge:</b> for n = 0.5 and φ = 10, calculate where the dead core ends. Predict which requested positions should have exactly zero concentration before running the code.</p><details><summary>Challenge solution</summary><pre>import numpy as np
from tutorial4_code import slab_profile
xi0 = 1-np.sqrt(3)/(0.5*10)    # About 0.65358984.
x = np.array([0.0, 0.5, xi0, 0.9, 1.0])
u, gradient = slab_profile(0.5, 10, x)
print(xi0, u)                 # First three concentrations are zero.
assert np.all(u[:3] == 0)      # Exact piecewise branch, not roundoff zero.
assert np.isclose(u[-1], 1)    # Surface boundary condition.</pre></details>
<p class="small"><b>Glossary:</b> a <em>mesh</em> is the set of solver positions; a <em>residual</em> measures how far an equation or boundary condition is from being satisfied; an <em>interpolant</em> estimates values between solved nodes; <em>continuation</em> reuses a nearby converged solution; a <em>root</em> is an input that makes a function zero; <em>array shape</em> describes its dimensions, such as two rows by 151 positions.</p>
</div>'''

chapter=soup.find(id='code')
download_tools=chapter.find(class_='tools')
download_tools.insert_after(BeautifulSoup(guide,'html.parser'))

# Token-based, offline syntax highlighting preserves the source exactly.
# CSS-generated line numbers never enter clipboard text or the download.
lines=code.splitlines(keepends=True)
starts=[0]
for line in lines: starts.append(starts[-1]+len(line))
styles=['']*len(code)
for tok in tokenize.generate_tokens(io.StringIO(code).readline):
    cls={token.COMMENT:'cm',token.STRING:'str',token.NUMBER:'num',token.OP:'op'}.get(tok.type,'')
    if tok.type==token.NAME and keyword.iskeyword(tok.string): cls='kw'
    if cls:
        a=starts[tok.start[0]-1]+tok.start[1]
        b=starts[tok.end[0]-1]+tok.end[1]
        styles[a:b]=[cls]*(b-a)
highlighted=[]
position=0
for line in lines:
    content=line.rstrip('\r\n')
    result=[]
    j=0
    while j<len(content):
        cls=styles[position+j];end=j+1
        while end<len(content) and styles[position+end]==cls: end+=1
        text=html.escape(content[j:end])
        result.append(f'<span class="{cls}">{text}</span>' if cls else text)
        j=end
    highlighted.append('<span class="line">'+''.join(result)+'</span>\n')
    position+=len(line)
code_tag=soup.find(id='python-code')
code_tag.clear()
fragment=BeautifulSoup('<pre>'+''.join(highlighted)+'</pre>','html.parser').pre
for child in list(fragment.contents): code_tag.append(child)
assert code_tag.get_text()==code, 'Highlighting changed the copied Python source.'
code_tag.parent['class']=['annotated-code']
code_tag.find_parent('details').find('summary').string='Read the complete annotated Python script (with line numbers)'
soup.find('style').append('''
.annotated-code{padding-left:0;counter-reset:source-line}.annotated-code .line{display:inline-block;min-height:1.65em;vertical-align:top;min-width:100%;padding-left:68px;position:relative}.annotated-code .line:before{counter-increment:source-line;content:counter(source-line);position:absolute;left:0;width:49px;text-align:right;color:#8da7af;border-right:1px solid #35505b;padding-right:10px;user-select:none}.annotated-code .cm{color:#a9c8b7}.annotated-code .str{color:#ead8ac}.annotated-code .kw{color:#b3d9ff;font-weight:600}.annotated-code .num{color:#f3c0a0}.annotated-code .op{color:#e1e9ed}
@media print{.annotated-code .cm,.annotated-code .str,.annotated-code .kw,.annotated-code .num,.annotated-code .op{color:#111}.annotated-code .line{white-space:pre-wrap;min-width:0;width:100%}}
''')
OUT.write_text(str(soup),encoding='utf-8')
print(f'Embedded {len(lines)} annotated Python lines; source and download remain identical.')
