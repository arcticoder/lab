"""
model.py — analytic model of the torsion balance in `params.py`.

Every formula is one that a cited paper also uses; `tools/force_noise_budget.py`
checks them against numbers published in:
  [SR13]  J. Soni, S. Roy, Rev. Sci. Instrum. 84, 095103 (2013): a torsion
          thrust stand with a fibre-optic displacement sensor and an
          eddy-current damper
  [CR22]  the cryogenic torsion balance of arXiv:2206.02890 (thermal torque
          noise S_tau = 4 kB T kappa / (Q omega), resonance and decay time)
"""

import math

import params as P


def strip_stiffness(width=None, thickness=None, length=None, shear=None, load_n=None):
    """Torsion constant of a thin rectangular strip, N*m/rad: G w t^3 / (3 L), plus the
    stiffening a taut ribbon gets from its tension, T w^2 / (12 L) [standard ribbon result,
    not checked against a source here]. load_n is the hang load; default the balance's weight."""
    w = P.STRIP_WIDTH if width is None else width
    t = P.STRIP_THICKNESS if thickness is None else thickness
    L = P.STRIP_LENGTH if length is None else length
    g = P.STRIP_SHEAR_MODULUS if shear is None else shear
    tension = P.MOVING_MASS * P.G_ACC if load_n is None else load_n
    return g * w * t**3 / (3 * L) + tension * w**2 / (12 * L)


def inertia():
    """Moment of inertia of the moving assembly about the pivot, kg*m^2 (from the CAD)."""
    return P.MOVING_INERTIA


def omega0(kappa, i):
    return math.sqrt(kappa / i)


def k_eff(kappa, l):
    """Force per displacement at arm radius l, N/m."""
    return kappa / l**2


def damping_c(kappa, i, l, zeta):
    """Viscous damping coefficient at radius l, N*s/m, for damping ratio zeta."""
    m_eff = i / l**2
    return 2 * zeta * math.sqrt(k_eff(kappa, l) * m_eff)


def thermal_force_density(kappa, i, l, zeta, temp=None):
    """Brownian force noise of a viscously damped balance, N/sqrt(Hz): sqrt(4 kB T c)."""
    t = P.T_K if temp is None else temp
    return math.sqrt(4 * P.KB * t * damping_c(kappa, i, l, zeta))


def thermal_torque_density_structural(kappa, q, omega, temp=None):
    """[CR22] Eq. 1: sqrt(4 kB T kappa / (Q omega)), N*m/sqrt(Hz)."""
    t = P.T_K if temp is None else temp
    return math.sqrt(4 * P.KB * t * kappa / (q * omega))


def disc_field_on_axis(z, br=None, radius=None, height=None):
    """B (T) on the axis of an axially magnetized disc, at distance z from one face (standard result)."""
    br = P.N42_BR if br is None else br
    r = (P.N42_DIAMETER / 2) if radius is None else radius
    h = P.N42_THICKNESS if height is None else height
    return br / 2 * ((z + h) / math.sqrt(r**2 + (z + h) ** 2) - z / math.sqrt(r**2 + z**2))


def eddy_damping_estimate(face_gap=None, vane_t=None, vane_radius=0.060, sigma=5.8e7):
    """First-order eddy-current damping of a copper vane between two opposed N42 discs [assume:
    c = sigma B^2 t A with A the disc footprint; right to about a factor of two at best].
    Returns (c at the vane, N*s/m; the damping ratio it gives at the flag radius when the vane
    fully covers the discs; B between the discs, T)."""
    face_gap = (1.5e-3 - 0.0) if face_gap is None else face_gap
    vane_t = P.VANE_THICKNESS if vane_t is None else vane_t
    b = 2 * disc_field_on_axis(face_gap)
    area = math.pi * (P.N42_DIAMETER / 2) ** 2
    c_vane = sigma * b**2 * vane_t * area
    l = P.ARM_HALF_LENGTH
    c_flag = c_vane * (vane_radius / l) ** 2
    kappa = strip_stiffness()
    zeta = c_flag / (2 * math.sqrt(k_eff(kappa, l) * inertia() / l**2))
    return c_vane, zeta, b


def displacement_noise_readout():
    """Flag-and-photodiode readout, m/sqrt(Hz): shot + TIA thermal + ADC, plus LED intensity
    noise after ratiometric rejection, divided by the slope I0/w."""
    i0 = P.LED_PHOTOCURRENT
    shot = math.sqrt(2 * P.Q_E * i0)
    tia = math.sqrt(4 * P.KB * P.T_K / P.TIA_RF)
    adc = P.ADC_NOISE_V / P.TIA_RF
    slope = i0 / P.BEAM_EDGE_WIDTH  # A/m
    x_current = math.sqrt(shot**2 + tia**2 + adc**2) / slope
    x_rin = P.BEAM_EDGE_WIDTH * P.LED_RIN / P.RIN_REJECTION
    return math.sqrt(x_current**2 + x_rin**2), {"shot": shot / slope, "tia": tia / slope, "adc": adc / slope, "rin": x_rin}


def env_scale(f):
    return (P.F_REF / f) ** P.SPECTRAL_SLOPE


def force_terms(f=None):
    """Force-noise density of every term at frequency f, N/sqrt(Hz)."""
    f = P.F_MOD if f is None else f
    kappa = strip_stiffness()
    i = inertia()
    l = P.ARM_HALF_LENGTH
    k = k_eff(kappa, l)
    w0 = omega0(kappa, i)
    # response of displacement to force: x = F / (k |1 - (f/f0)^2 + 2j zeta (f/f0)|)
    r = f / (w0 / (2 * math.pi))
    h = abs(complex(1 - r**2, 2 * P.DAMPING_RATIO * r))
    xr, _ = displacement_noise_readout()
    m_total = P.MOVING_MASS
    s = env_scale(f)
    terms = {
        "readout (shot + electronics + LED)": xr * k * h,
        "thermal (Brownian, eddy damper)": thermal_force_density(kappa, i, l, P.DAMPING_RATIO),
        "floor tilt through centre-of-mass offset": m_total * P.G_ACC * P.COM_OFFSET * P.TILT_NOISE_RAD * s / l,
        "floor acceleration through centre-of-mass offset": m_total * P.SEISMIC_ACC * s * P.COM_OFFSET / l,
        "air currents": 1.2 * 1.0 * P.AIR_AREA * P.AIR_SPEED_RMS * P.AIR_SPEED_FLUCT * s,
        "temperature (arm expansion)": k * P.ARM_EXPANSION * l * P.TEMP_NOISE * s,
        "magnetic (stray moment x field noise)": P.STRAY_MOMENT * P.B_NOISE * s / l,
    }
    return terms


def total_density(terms):
    return math.sqrt(sum(v**2 for v in terms.values()))


def resolution(density, t_int=None):
    """1-sigma force estimate from t_int seconds of lock-in data: density * sqrt(ENBW), ENBW = 1/(2 T)."""
    t = P.INTEGRATION_S if t_int is None else t_int
    return density * math.sqrt(1 / (2 * t))
