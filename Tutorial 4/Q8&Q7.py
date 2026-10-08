import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import solve_bvp, simpson
from scipy.special import ive

COLORS = ['#126e82', '#bb5a2a', '#7759a6', '#387d44']

def first_order(x, phi):
    return (np.exp(phi * (x - 1)) + np.exp(-phi * (x + 1))) / (1 + np.exp(-2 * phi))

def slab_profile(n, phi, x):
    if not np.isfinite(n) or not np.isfinite(phi) or n <= 0 or phi <= 0:
        raise ValueError('This implementation requires finite n > 0 and phi > 0.')
    x = np.asarray(x, dtype=float)
    if (x.ndim != 1 or x.size == 0 or not np.all(np.isfinite(x))
            or np.any(x < 0) or np.any(x > 1) or np.any(np.diff(x) <= 0)):
        raise ValueError('x must be an increasing 1-D array of positions in [0,1].')
    if n < 1:
        phi_critical = np.sqrt(2 * (n + 1)) / (1 - n)
        if phi >= phi_critical:
            xi0 = 1 - phi_critical / phi
            power = 2 / (1 - n)
            z = np.maximum((x - xi0) / (1 - xi0), 0)
            return z**power, power * z**(power - 1) / (1 - xi0)

    mesh = np.linspace(0, 1, 151)
    guess = np.vstack((np.ones_like(mesh), np.zeros_like(mesh)))

    def bc(ya, yb):
        return np.array([ya[1], yb[0] - 1])

    for current_phi in np.geomspace(min(0.1, phi), phi, 50):
        def ode(xi, y):
            return np.vstack((y[1], current_phi**2 * np.maximum(y[0], 0)**n))

        sol = solve_bvp(ode, bc, mesh, guess, tol=1e-7, max_nodes=40000)
        if not sol.success:
            raise RuntimeError(f'n={n}, phi={current_phi}: {sol.message}')

        uniform_mesh = np.linspace(0, 1, 301)
        surface_mesh = 1 - np.geomspace(1e-5, 1, 301)
        mesh = np.unique(np.round(np.r_[uniform_mesh, surface_mesh], 12))
        guess = sol.sol(mesh)

    u, gradient = sol.sol(x)
    if u.min() < -1e-9 or np.max(np.abs(bc(sol.y[:, 0], sol.y[:, -1]))) > 1e-8:
        raise RuntimeError('Nonphysical concentration or failed boundary condition.')
    centre_u = max(float(sol.sol(0)[0]), 0)
    integral_rhs = 2 * phi**2 / (n + 1) * (np.maximum(u, 0)**(n + 1) - centre_u**(n + 1))
    assert np.max(np.abs(gradient**2 - integral_rhs)) / (1 + phi**2) < 2e-7, 'First integral failed.'
    return u, gradient

def format_axis(ax, title):
    ax.set(title=title, xlabel=r'$\xi=x/L$ (centre to surface)',
           ylabel=r'$\widetilde C_A=C_A/C_{AS}$', xlim=(0, 1), ylim=(0, 1.04))
    ax.grid(alpha=0.2)

def q7():
    x = np.linspace(0, 1, 10001)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    for phi, color in zip([0.1, 1, 10, 100], COLORS):
        u, du = slab_profile(1, phi, x)
        exact = first_order(x, phi)
        error = np.max(np.abs(u - exact))
        print(f'n=1, phi={phi:g}: max analytical error={error:.3e}')
        assert error < 1e-6, 'First-order numerical and analytical profiles disagree.'
        for ax in axes:
            ax.plot(x, u, color=color, label=f'phi = {phi:g}, numerical')
            sample = np.linspace(0, len(x) - 1, 31, dtype=int)
            ax.plot(x[sample], exact[sample], 'o', ms=3.2, mfc='none',
                    color=color, label='_nolegend_')
    format_axis(axes[0], 'Q7(a): first-order profiles')
    format_axis(axes[1], 'Surface detail; circles = analytical solution')
    axes[1].set_xlim(0.9, 1)
    axes[0].legend(fontsize=9)
    fig.savefig('q7a.svg')
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    for ax, phi in zip(axes, [0.1, 100]):
        for n, color in zip([0.5, 1, 1.5, 2], COLORS):
            u, du = slab_profile(n, phi, x)
            eta = simpson(np.maximum(u, 0)**n, x=x)
            flux_eta = du[-1] / phi**2
            assert abs(eta - flux_eta) < 2e-7, 'Integrated reaction does not match flux.'
            assert np.min(np.diff(u)) > -1e-8, 'Concentration is not monotonic.'
            print(f'n={n:g}, phi={phi:g}: u(0)={u[0]:.6g}, '
                  f'eta={eta:.7g}, surface gradient={du[-1]:.7g}')
            ax.plot(x, u, color=color, linestyle='--' if n == 1 else '-',
                    label=f'n = {n:g}')
        format_axis(ax, f'Q7(b): phi = {phi:g}')
        if phi == 0.1:
            ax.set_ylim(0.9949, 1.0002)
        else:
            ax.set_xlim(0.9, 1)
        ax.legend(fontsize=9)
    fig.savefig('q7b.svg')
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.1), constrained_layout=True)
    for n, color in zip([0.5, 1, 1.5, 2], COLORS):
        u, _ = slab_profile(n, 100, x)
        ax.plot(x, u, color=color, label=f'n = {n:g}')
    format_axis(ax, 'Q7(b): phi = 100, full half-slab')
    ax.legend()
    fig.savefig('q7b_full.svg')
    plt.close(fig)

def q8():
    phi = np.linspace(1, 100, 1000)
    plate = np.tanh(phi) / phi
    sphere = (3 * phi / np.tanh(3 * phi) - 1) / (3 * phi**2)
    cylinder = ive(1, 2 * phi) / (phi * ive(0, 2 * phi))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    for name, eta, color in zip(['Flat plate', 'Sphere', 'Cylinder'],
                                 [plate, sphere, cylinder], COLORS):
        assert np.all((eta > 0) & (eta <= 1)), f'{name}: eta outside (0,1].'
        assert np.all(np.diff(eta) < 0), f'{name}: eta must decrease with phi.'
        for ax in axes:
            ax.plot(phi, eta, label=name, color=color)
    for ax in axes:
        ax.set(xlabel=r'$\phi=(V_p/S_p)\sqrt{k/D_e}$', ylabel=r'$\eta$')
        ax.grid(alpha=0.2)
        ax.legend()
    axes[0].set(title='Q8: effectiveness versus Thiele modulus', xlim=(1, 100))
    axes[1].set(title='Detail near phi = 1', xlim=(1, 5), ylim=(0.17, 0.8))
    fig.savefig('q8.svg')
    plt.close(fig)

if __name__ == '__main__':
    q7()
    q8()
