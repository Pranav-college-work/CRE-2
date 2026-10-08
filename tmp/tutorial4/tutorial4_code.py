"""Tutorial 4: self-contained, commented calculations and plots for Q1-Q8.

HOW TO RUN
    Save this as tutorial4_code.py, open a terminal in that folder, and run:
        python -m pip install numpy scipy matplotlib
        python tutorial4_code.py
    `python -m pip` installs packages for the Python interpreter being used.
    No internet connection or external data files are needed after installation.

WHAT YOU GET
    Numerical answers and verification results appear in the terminal.
    Four SVG (Scalable Vector Graphics) files appear in the CURRENT WORKING
    DIRECTORY: q7a.svg, q7b.svg, q7b_full.svg, q8.svg. Re-running replaces them.
    Open those files in a browser. No plot window is expected.

READING ORDER
    q1_to_q6() reproduces arithmetic and scalar root solves.
    first_order() gives the exact solution used to verify Q7.
    slab_profile() solves the nonlinear differential equation for Q7.
    q7() and q8() turn numerical results into the requested plots.

NOTATION AND UNITS
    Phi (capital P): R*sqrt(k/De), the radius-based spherical modulus in Q3-Q4.
    phi: L*sqrt(k*C_s**(n-1)/De) for Q7; (V_p/S_p)*sqrt(k/De) for Q8.
    For a sphere in Q8, Phi=3*phi. Do not interchange these definitions.
    x inside profile functions means DIMENSIONLESS xi=x_physical/L, not metres.
    u=C_A/C_As and gradient=du/dxi are dimensionless. In dimensional units:
        dC_A/dx_physical = (C_As/L)*gradient
        outward molar flux = -De*(C_As/L)*gradient
    The negative flux indicates reactant diffuses inward.

ASSUMPTIONS AND SOURCES
    Steady, isothermal, uniform-activity pellets with constant effective De.
    Fogler, 5th ed., Ch. 15, pp. 728-736: spherical profile and effectiveness.
    Levenspiel, 3rd ed., Ch. 18, pp. 386-390: V/S convention and shape formulas.
    The Q4 numerical completion is CONDITIONAL: it restores C(R/2)/Cs=0.1
    from Fogler P15-5B, p. 760, while keeping the tutorial's dimensions.
    The HTML contains the full derivations and local book-page links.

CHECKS
    `assert` stops the program when a required accuracy/physics check fails.
    Do not remove failed checks or run with Python's -O flag (disables asserts).
    The solver is verified for the tutorial cases, not every possible n and phi.
"""
# NumPy arrays apply mathematical operations to many coordinates at once.
import numpy as np
import matplotlib
# Select file rendering BEFORE importing pyplot: no graphical desktop required.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# solve_bvp: boundary-value problem solver; simpson: numerical integration.
from scipy.integrate import solve_bvp, simpson
# Scaled modified Bessel functions avoid very large intermediate values in Q8.
from scipy.special import ive
# brentq locates a zero between endpoints where a function has opposite signs.
from scipy.optimize import brentq

# Appearance only: readable labels, fewer borders, editable text in SVG output.
plt.rcParams.update({'font.size': 11, 'axes.spines.top': False,
                     'axes.spines.right': False, 'svg.fonttype': 'none'})
COLORS = ['#126e82', '#bb5a2a', '#7759a6', '#387d44']

def sphere_eta(Phi):
    """Return scalar spherical eta for nonnegative Phi=R*sqrt(k/De).

    Eta is a dimensionless ratio of actual to intrinsic rate at the surface
    concentration. Formula: Fogler Eq. (15-32), printed p. 731.
    """
    if abs(Phi) < 1e-3:
        # Near zero the exact formula subtracts nearly equal numbers. This
        # series avoids loss of significant digits and returns eta(0)=1.
        return 1-Phi**2/15+2*Phi**4/315
    # coth(Phi)=1/tanh(Phi); the Phi here is NOT Q8's smaller V/S modulus.
    return 3*(Phi/np.tanh(Phi)-1)/Phi**2

def q1_to_q6():
    """Print Q1-Q6 answers, keeping each question's units consistent.

    There is no return value. A format like :.8g changes only displayed rounding
    to eight significant digits. `1e5` means 10**5; `**` means exponentiation.
    """
    # Q1: the Knudsen correlation expects radius in cm, T in K and M in g/mol.
    pore_radius_cm = 50*1e-8           # 1 angstrom = 1e-8 cm.
    temperature_K = 100+273.15         # Celsius must be converted before sqrt(T).
    molar_mass_hydrogen = 2.016        # g/mol.
    structure_factor = 0.4*0.8/4      # porosity * constriction / tortuosity.
    dk = 9.70e3*pore_radius_cm*np.sqrt(temperature_K/molar_mass_hydrogen)
    for pressure in [1, 10]:           # pressure in atm, as the given formula uses.
        dab = 0.86/pressure            # Molecular diffusivity in cm^2/s.
        combined = 1/(1/dab + 1/dk)   # Add diffusion resistances, not coefficients.
        print(f'Q1 p={pressure} atm: D_AB={dab:.8g}, D_K={dk:.8g}, '
              f'D={combined:.8g}, D_e={structure_factor*combined:.8g} cm^2/s')

    # Q2: use hours throughout; an extra conversion to seconds is unnecessary.
    rate_mass = 1e5                    # mol/(kg-cat*h), printed rate is 10^5.
    pellet_density = 2200              # 2.2 g/cm^3 in kg/m^3.
    radius_m = 0.5e-3/2               # Convert DIAMETER of .5 mm to radius in m.
    de = 5e-5                         # m^2/h, already effective.
    surface_concentration = 20         # mol/m^3; given concentration approximation.
    rate_volume = rate_mass*pellet_density  # mol/(m^3 pellet*h).
    wp2 = rate_volume*radius_m**2/(de*surface_concentration)
    # Sphere V/S=R/3, so the length-squared parameter M_W is C_WP/9.
    print(f'Q2 C_WP={wp2:g}; M_W={wp2/9:.7g}')

    # Q3: identical kinetics and surface concentration allow rate ratios to cancel.
    def rate_ratio_error(small_Phi):
        """Return predicted eta1/eta2 minus measured rate1/rate2 = 3/15."""
        # The large pellet has ten times the radius, hence Phi1=10*Phi2.
        return sphere_eta(10*small_Phi)/sphere_eta(small_Phi)-3/15
    # brentq seeks zero error; .01 and 10 are search bounds, not input data.
    phi2 = brentq(rate_ratio_error, 0.01, 10)
    print(f'Q3 Phi1={10*phi2:.9g}, Phi2={phi2:.9g}, '
          f'eta1={sphere_eta(10*phi2):.9g}, eta2={sphere_eta(phi2):.9g}')

    # Q4: find the target modulus before assigning ANY missing rate constant.
    # lambda defines a short function; its zero corresponds to eta=.8.
    target = brentq(lambda z: sphere_eta(z)-0.8, 0.01, 10)
    print(f'Q4 target Phi={target:.10g}; diameter coefficient '
          f'{2*target*np.sqrt(0.1):.10g} cm when k is in 1/s')
    # Interpretation: d_new[cm]=the printed coefficient/sqrt(k[1/s]); De=.1 cm^2/s.
    # CONDITIONAL: restore C(R/2)/C_s=0.1 from Fogler P15-5B.
    # Retain the TUTORIAL radius R=0.1 cm, not the textbook radius.
    original = 2*np.arccosh(10)        # From 1/cosh(Phi_old/2)=.1.
    old_radius_cm = 0.1
    de_cm2_s = 0.1
    xi = (old_radius_cm-0.03)/old_radius_cm  # Evaluate at r/R=.7, not .3.
    concentration = .001*np.sinh(xi*original)/(xi*np.sinh(original))
    inferred_k = original**2*de_cm2_s/old_radius_cm**2
    new_diameter_cm = 2*old_radius_cm*target/original  # Phi proportional to diameter.
    print(f'Q4 conditional: k={inferred_k:.9g} 1/s, '
          f'C={concentration:.9g} mol/dm^3, d_new={new_diameter_cm:.9g} cm')

    # Q5: rate is ALREADY per pellet volume; do not multiply by density again.
    rate_volume = 1e5                  # mol/(h*m^3 pellet).
    radius_m = 2.4e-3/2
    film_coefficient = 300             # m/h, from m^3/(h*m^2).
    bulk_concentration = 20            # mol/m^3.
    de = 5e-5                         # m^2/h; porosity is already included.
    # q_v*V=kg*S*(Cb-Cs), and V/S=R/3 for a sphere.
    surface = bulk_concentration-rate_volume*radius_m/(3*film_coefficient)
    wp5 = rate_volume*radius_m**2/(de*surface)
    # Radius-based, pellet-volume Mears screen for reaction order n=1.
    # The HTML explains why bed void fraction and pellet porosity are different.
    mears = rate_volume*radius_m/(film_coefficient*bulk_concentration)
    print(f'Q5 C_s={surface:.9g}, C_WP={wp5:.9g}, C_M={mears:.9g}')

    # Q6: doubling diameter halves the first-order PFR exponent -ln(1-X).
    # It does NOT halve X. Other reactor conditions and catalyst mass are fixed.
    old_conversion = 0.632
    diameter_ratio = 9/18              # old diameter / new diameter.
    x2 = 1-(1-old_conversion)**diameter_ratio
    print(f'Q6 X2={x2:.9g}')

def first_order(x, phi):
    """Return exact dimensionless first-order u on NumPy coordinates x=xi.

    Divide cosh(phi*x)/cosh(phi) by exp(phi) top and bottom. The equivalent
    expression below has only non-positive exponential arguments on [0,1],
    so it does not overflow at large phi.
    """
    # Algebraically identical to cosh(phi*x)/cosh(phi), without overflow.
    return (np.exp(phi*(x-1)) + np.exp(-phi*(x+1))) / (1+np.exp(-2*phi))

def slab_profile(n, phi, x):
    """Return (u, gradient), two NumPy arrays evaluated at x=dimensionless xi.

    Inputs: positive finite scalars n and phi; increasing, nonempty 1-D array x
    of positions in [0,1]. Lists are accepted and converted to floating arrays.
    Outputs: concentration C/C_s and gradient du/dxi, each the same shape as x.
    Equation: u''=phi**2*u**n, with u'(0)=0 at centre and u(1)=1 at surface.
    Assumptions: isothermal slab, constant De, uniform activity.
    Method: exact zero-core branch where appropriate; otherwise a BVP solve.
    BVP means boundary-value problem: conditions are specified at BOTH ends.
    The unknown centre concentration must be solved, not prescribed as zero.
    """
    if not np.isfinite(n) or not np.isfinite(phi) or n <= 0 or phi <= 0:
        raise ValueError('This implementation requires finite n > 0 and phi > 0.')
    x = np.asarray(x, dtype=float)     # Elementwise operations need a numeric array.
    if (x.ndim != 1 or x.size == 0 or not np.all(np.isfinite(x))
            or np.any(x < 0) or np.any(x > 1) or np.any(np.diff(x) <= 0)):
        raise ValueError('x must be an increasing 1-D array of positions in [0,1].')
    if n < 1:
        # Sublinear kinetics can exhaust reactant a finite distance from surface.
        phi_critical = np.sqrt(2*(n+1))/(1-n)
        if phi >= phi_critical:
            # Exact free-boundary solution: u=u'=0 at xi=xi0.
            xi0 = 1 - phi_critical/phi  # Edge of the exactly zero-concentration core.
            power = 2/(1-n)            # Fourth power for n=.5.
            z = np.maximum((x-xi0)/(1-xi0), 0)  # Map active layer to [0,1].
            # The gradient includes dz/dxi=1/(1-xi0), by the chain rule.
            return z**power, power*z**(power-1)/(1-xi0)

    # Continue from a weak-reaction solution to resolve steep profiles.
    mesh = np.linspace(0, 1, 151)      # Initial solver positions; endpoints included.
    # State array has shape (2, number_of_nodes): row 0=u, row 1=v=u'.
    # Weak reaction suggests u~1 and v~0; vstack combines those guesses as rows.
    guess = np.vstack((np.ones_like(mesh), np.zeros_like(mesh)))
    def bc(ya, yb):
        """Boundary residuals: ya=[u(0),v(0)], yb=[u(1),v(1)]."""
        # Both returned entries must be zero. Notice u(0)=ya[0] is NOT fixed.
        return np.array([ya[1], yb[0]-1])
    # Multiplicative steps from weak reaction to the target; not time integration.
    # 50 is a continuation setting, not a physical constant.
    for current_phi in np.geomspace(min(0.1, phi), phi, 50):
        def ode(xi, y):
            """ODE (ordinary differential equation) system: [u',v']=[v,phi^2*u^n]."""
            # Newton iterations can temporarily cross zero; only protect
            # the fractional power during iteration, then validate output.
            # xi is required by SciPy even though our law has no explicit xi term.
            return np.vstack((y[1], current_phi**2*np.maximum(y[0], 0)**n))
        # tol controls a scaled ODE residual, NOT relative error in a tiny u(0).
        # max_nodes caps adaptive refinement; a failure is raised below.
        sol = solve_bvp(ode, bc, mesh, guess, tol=1e-7, max_nodes=40000)
        if not sol.success:
            raise RuntimeError(f'n={n}, phi={current_phi}: {sol.message}')
        # Restart on a surface-refined mesh; retaining every previous node
        # can accumulate unnecessary nodes over the continuation sequence.
        uniform_mesh = np.linspace(0, 1, 301)
        surface_mesh = 1-np.geomspace(1e-5, 1, 301)  # Extra nodes near xi=1.
        # np.r_ joins arrays; round removes near-duplicate floating-point values;
        # unique sorts and removes repeats, ensuring strictly increasing nodes.
        mesh = np.unique(np.round(np.r_[uniform_mesh, surface_mesh], 12))
        guess = sol.sol(mesh)          # Previous solution becomes next initial guess.
    # sol.sol is an interpolant: evaluate on the output grid, not only solver nodes.
    u, gradient = sol.sol(x)
    # [:,0] selects both state values at the centre; [:,-1] selects the surface.
    if u.min() < -1e-9 or np.max(np.abs(bc(sol.y[:, 0], sol.y[:, -1]))) > 1e-8:
        raise RuntimeError('Nonphysical concentration or failed boundary condition.')
    # A second, local check follows by integrating u''=phi^2*u^n once.
    # Numerical noise near u=0 is judged by an absolute, scaled tolerance.
    # Check (u')^2=2*phi^2/(n+1)*(u^(n+1)-u_centre^(n+1)). The actual centre
    # is needed even when x requests just a surface zoom, e.g. x=.9,...,1.
    centre_u = max(float(sol.sol(0)[0]), 0)
    integral_rhs = 2*phi**2/(n+1)*(np.maximum(u, 0)**(n+1)-centre_u**(n+1))
    # Scaling by 1+phi^2 makes the tolerance usable across the tutorial range.
    assert np.max(np.abs(gradient**2-integral_rhs))/(1+phi**2) < 2e-7, 'First integral failed.'
    return u, gradient

def format_axis(ax, title):
    """Label one Matplotlib axis (plot panel); styling does not change results."""
    # r'...' is a raw string, preserving backslashes for mathematical labels.
    ax.set(title=title, xlabel=r'$\xi=x/L$ (centre to surface)',
           ylabel=r'$\widetilde C_A=C_A/C_{AS}$', xlim=(0, 1), ylim=(0, 1.04))
    ax.grid(alpha=0.2)

def q7():
    """Generate Q7a, Q7b and the full-domain companion; print accuracy checks.

    q7a compares numerical lines with exact first-order open-circle markers.
    q7b compares reaction orders at phi=.1 and 100. q7b_full shows the interior
    that would be hidden by a surface-only zoom. Each file is vector SVG.
    """
    x = np.linspace(0, 1, 10001)       # Dense output grid, not 10001 solver nodes.
    # fig is the whole figure; axes contains two independently labelled panels.
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    for phi, color in zip([0.1, 1, 10, 100], COLORS):  # Pair parameters and colours.
        u, du = slab_profile(1, phi, x)
        exact = first_order(x, phi)
        error = np.max(np.abs(u-exact))  # Largest ABSOLUTE error across all points.
        print(f'n=1, phi={phi:g}: max analytical error={error:.3e}')
        assert error < 1e-6, 'First-order numerical and analytical profiles disagree.'
        for ax in axes:                # Same curve in full-domain and zoom views.
            ax.plot(x, u, color=color, label=f'phi = {phi:g}, numerical')
            # Sparse open markers make coincidence with the numerical line visible.
            sample = np.linspace(0, len(x)-1, 31, dtype=int)  # 31 integer indices.
            # 'o'=circles, ms=marker size, mfc='none'=open centres; avoid duplicate legend.
            ax.plot(x[sample], exact[sample], 'o', ms=3.2, mfc='none',
                    color=color, label='_nolegend_')
    format_axis(axes[0], 'Q7(a): first-order profiles')
    format_axis(axes[1], 'Surface detail; circles = analytical solution')
    axes[1].set_xlim(0.9, 1)           # Reveal the thin surface layer at phi=100.
    axes[0].legend(fontsize=9)
    fig.savefig('q7a.svg')             # Save vector graphics rather than screenshots.
    plt.close(fig)                    # Release the completed figure's memory.

    # Q7(b): one phi per panel; compare all reaction orders within that panel.
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    for ax, phi in zip(axes, [0.1, 100]):
        for n, color in zip([0.5, 1, 1.5, 2], COLORS):
            u, du = slab_profile(n, phi, x)
            # Eta integrates u^n. Integrating u alone is correct ONLY for n=1.
            eta = simpson(np.maximum(u, 0)**n, x=x)
            # Integrated reaction must equal the surface diffusive flux.
            flux_eta = du[-1]/phi**2   # [-1] selects the surface at xi=1.
            assert abs(eta-flux_eta) < 2e-7, 'Integrated reaction does not match flux.'
            # diff subtracts adjacent values: concentration must rise toward surface.
            assert np.min(np.diff(u)) > -1e-8, 'Concentration is not monotonic.'
            print(f'n={n:g}, phi={phi:g}: u(0)={u[0]:.6g}, '
                  f'eta={eta:.7g}, surface gradient={du[-1]:.7g}')
            # Dashed first-order line is the reference for the nonlinear cases.
            ax.plot(x, u, color=color, linestyle='--' if n == 1 else '-',
                    label=f'n = {n:g}')
        format_axis(ax, f'Q7(b): phi = {phi:g}')
        if phi == 0.1:
            ax.set_ylim(0.9949, 1.0002)  # A full 0-1 y-axis hides small differences.
        else:
            ax.set_xlim(0.9, 1)
        ax.legend(fontsize=9)
    fig.savefig('q7b.svg')
    plt.close(fig)

    # Full domain for the strongly limited profiles, including the dead core.
    fig, ax = plt.subplots(figsize=(8, 4.1), constrained_layout=True)
    for n, color in zip([0.5, 1, 1.5, 2], COLORS):
        u, _ = slab_profile(n, 100, x)  # `_` means the gradient output is unused.
        ax.plot(x, u, color=color, label=f'n = {n:g}')
    format_axis(ax, 'Q7(b): phi = 100, full half-slab')
    ax.legend()
    fig.savefig('q7b_full.svg')
    plt.close(fig)

def q8():
    """Save q8.svg: first-order eta for three shapes using the SAME V/S modulus.

    Each formula acts elementwise on the whole phi array. The first panel shows
    phi=1-100 and the second enlarges phi=1-5. Levenspiel Eqs. (20)-(23), p. 387.
    """
    phi = np.linspace(1, 100, 1000)    # 1000 plotted samples; zero is not requested.
    plate = np.tanh(phi)/phi           # For a plate, V/S is its half-thickness L.
    sphere = (3*phi/np.tanh(3*phi)-1)/(3*phi**2)  # Radius-based Phi=3*phi.
    # Exponentially scaled Bessel functions prevent overflow at large phi.
    # ive(n,z)=exp(-abs(z))*I_n(z) for positive real z; scaling cancels in ratio.
    cylinder = ive(1, 2*phi)/(phi*ive(0, 2*phi))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    # zip keeps each shape's name, values and plotting colour together.
    for name, eta, color in zip(['Flat plate', 'Sphere', 'Cylinder'],
                                 [plate, sphere, cylinder], COLORS):
        # Check EVERY sampled eta and every difference between adjacent samples.
        assert np.all((eta > 0) & (eta <= 1)), f'{name}: eta outside (0,1].'
        assert np.all(np.diff(eta) < 0), f'{name}: eta must decrease with phi.'
        for ax in axes:
            ax.plot(phi, eta, label=name, color=color)
    for ax in axes:
        ax.set(xlabel=r'$\phi=(V_p/S_p)\sqrt{k/D_e}$', ylabel=r'$\eta$')
        ax.grid(alpha=0.2)
        ax.legend()
    axes[0].set(title='Q8: effectiveness versus Thiele modulus', xlim=(1,100))
    axes[1].set(title='Detail near phi = 1', xlim=(1,5), ylim=(0.17,0.8))
    fig.savefig('q8.svg')
    plt.close(fig)

# Run everything when started as a script, but not when imported for one helper.
# Example: `from tutorial4_code import slab_profile` does not create all figures.
if __name__ == '__main__':
    q1_to_q6()
    q7()
    q8()
    print('Saved q7a.svg, q7b.svg, q7b_full.svg and q8.svg.')
