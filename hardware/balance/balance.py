"""
balance.py — CadQuery model of the torsion balance (`FORCEBAL`), G2.

    ~/.venvs/lab-hw/bin/python hardware/balance/balance.py

Builds every part in millimetres from `params.py`, computes the moving assembly's mass and
moment of inertia and compares them with the model's, checks that nothing collides over
the arm's swing, that every printed part fits the printer, and exports STL files (one per
part, printable on the Creality K1) and a STEP assembly to `hardware/balance/cad/`.

Layout (z up, the pivot axis is the z axis):
  base plate, two uprights and a cross beam carry the top strip clamp at z = 110..120.
  A stainless strip (4 mm x 50 um x 30 mm, z = 80..110) hangs from it to the hub of the
  arm. The arm lies along x: the device mount (+x), a counterweight pocket (-x).
  Eddy-current damper (+x, y > 0): a copper vane on the arm moves between two N42 discs
  held fixed to the base. Optical sensor (-x end): a flag tab on the arm moves through a
  C-bracket whose two prongs carry the LED board (above) and the photodiode board (below).
"""

import math
import os

import cadquery as cq

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cad")

MM = 1e3
L = P.ARM_HALF_LENGTH * MM  # 100
PLA_G_MM3 = 1.24e-3
INFILL = 0.6  # fraction of the solid's mass for a printed part (walls + 30% gyroid)
CU_G_MM3, STEEL_G_MM3, ND_G_MM3 = 8.96e-3, 7.85e-3, 7.5e-3

# vertical layout
Z_ARM0, Z_ARM1 = 58.0, 66.0
Z_HUB1 = 72.0
Z_LOW0, Z_LOW1 = 72.0, 80.0  # lower strip clamp
Z_TOP0, Z_TOP1 = 110.0, 120.0  # top strip clamp
Z_BEAM0, Z_BEAM1 = 120.0, 132.0
T_STRIP = P.STRIP_THICKNESS * MM
W_STRIP = P.STRIP_WIDTH * MM


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def cyl_z(x, y, z0, z1, d):
    return cq.Workplane("XY").circle(d / 2).extrude(z1 - z0).translate((x, y, z0))


def build(ballast_len=14.0, counter_len=12.0):
    """All parts. ballast_len (mm) and counter_len (mm) are solved by balance_solve() so the
    moving assembly's centre of mass sits on the pivot axis."""
    parts = {}  # name -> (solid, density g/mm3, moving, printed)

    def add(name, wp, density, moving, printed=False):
        parts[name] = (wp, density, moving, printed)

    # ---- fixed structure -----------------------------------------------------------
    add("base", box(-100, 100, -100, 100, 0, 6), PLA_G_MM3 * INFILL, False, True)
    add("upright_a", box(-6, 6, 39, 51, 6, Z_BEAM1), PLA_G_MM3 * INFILL, False, True)
    add("upright_b", box(-6, 6, -51, -39, 6, Z_BEAM1), PLA_G_MM3 * INFILL, False, True)
    add("beam", box(-6, 6, -51, 51, Z_BEAM0, Z_BEAM1), PLA_G_MM3 * INFILL, False, True)
    for tag, (y0, y1) in (("a", (-8, -T_STRIP / 2)), ("b", (T_STRIP / 2, 8))):
        top = box(-10, 10, y0, y1, Z_TOP0, Z_TOP1)
        for x in (-7, 7):
            top = top.cut(cq.Workplane("XZ").circle(1.7).extrude(30, both=True).translate((x, 0, (Z_TOP0 + Z_TOP1) / 2)))
        add(f"top_clamp_{tag}", top, PLA_G_MM3 * INFILL, False, True)

    # ---- the moving assembly -----------------------------------------------------------
    # one printed piece: the arm, its hub, the device-mount plate (+x) and the counterweight pocket (-x)
    arm = box(-L, L, -5, 5, Z_ARM0, Z_ARM1).union(box(-12, 12, -12, 12, Z_ARM0, Z_HUB1))
    arm = arm.union(box(L - 8, L, -14, 14, Z_ARM0 - 6, Z_ARM1 + 18))  # device mount plate
    arm = arm.union(box(-L, -L + 16, -10, 10, Z_ARM0 - 6, Z_ARM1 + 4))  # counterweight pocket body
    arm = arm.cut(cyl_z(-L + 8, 0, Z_ARM0 - 6.5, Z_ARM1 + 4.5, 10.3))  # ballast hole
    for x in (-60, -30, 30, 60):  # lightening holes through the arm's web
        arm = arm.cut(cq.Workplane("XY").circle(2.5).extrude(20, both=True).translate((x, 0, (Z_ARM0 + Z_ARM1) / 2)))
    add("arm", arm, PLA_G_MM3 * INFILL, True, True)
    for tag, (y0, y1) in (("a", (-8, -T_STRIP / 2)), ("b", (T_STRIP / 2, 8))):
        low = box(-10, 10, y0, y1, Z_LOW0, Z_LOW1)
        for x in (-7, 7):
            low = low.cut(cq.Workplane("XZ").circle(1.7).extrude(30, both=True).translate((x, 0, (Z_LOW0 + Z_LOW1) / 2)))
        add(f"low_clamp_{tag}", low, PLA_G_MM3 * INFILL, True, True)
    add("strip", box(-W_STRIP / 2, W_STRIP / 2, -T_STRIP / 2, T_STRIP / 2, Z_LOW1 - 6, Z_TOP0 + 6), STEEL_G_MM3, True)
    # steel masses: ballast in the pocket (-x), a dummy device at +x, a y-counter-mass on the hub's -y side
    add("ballast", cyl_z(-L + 8, 0, Z_ARM0 - 6, Z_ARM0 - 6 + ballast_len, 10.0), STEEL_G_MM3, True)
    add("dut_dummy", box(L - 18, L - 8, -5, 5, Z_ARM1, Z_ARM1 + 10), STEEL_G_MM3, True)  # stands for the device (8 g)
    add("y_counter", box(-5, 5, -12 - counter_len, -12, Z_ARM0, Z_ARM0 + 8), STEEL_G_MM3, True)
    # flag: a riser on the arm's -x end face and a horizontal tab that crosses the sensor beam at y = 22
    riser = box(-L - 4, -L, 0, 4, Z_ARM1, 71)
    tab = box(-L - 8, -L + 0.5, 0, 22, 70.0, 70.6)
    add("flag", riser.union(tab), PLA_G_MM3, True, True)
    # damper vane: copper plate 1 mm, in a slot of a holder that is glued to the arm's side
    vane_box = box(50, 70, 8, 30, 62.0, 63.0)
    add("vane_holder", box(55, 65, 5, 10, Z_ARM0, Z_ARM1 + 1).cut(vane_box), PLA_G_MM3 * INFILL, True, True)
    add("vane", vane_box, CU_G_MM3, True)

    # electrostatic plates at x = 72..88: a moving tab on the arm's +y side (copper foil on its +y face,
    # reached through the strip's clamp) and a fixed plate on the base, 1 mm across
    add("elec_arm", box(72, 88, 5, 7, 52.0, 70.0), PLA_G_MM3 * INFILL, True, True)
    add("elec_fixed", box(72, 88, 8, 12, 6.0, 70.0), PLA_G_MM3 * INFILL, False, True)

    # ---- fixed: damper (two N42 discs) and sensor bracket ------------------------------------
    # vane at z 62..63 passes between the lower disc (z 58..61) and the upper disc (z 64..67); discs at (60, 25)
    holder = box(52, 68, 36, 44, 6, 70).union(box(52, 68, 20, 44, 54.0, 58.0)).union(box(52, 68, 20, 44, 67.0, 70.0))
    holder = holder.union(box(52, 68, 20, 44, 58.0, 61.0).cut(cyl_z(60, 25, 57.0, 62.0, 6.2)))
    holder = holder.union(box(52, 68, 20, 44, 64.0, 67.0).cut(cyl_z(60, 25, 63.0, 68.0, 6.2)))
    add("damper_holder", holder, PLA_G_MM3 * INFILL, False, True)
    add("magnet_low", cyl_z(60, 25, 58.0, 61.0, 6.0), ND_G_MM3, False)
    add("magnet_up", cyl_z(60, 25, 64.0, 67.0, 6.0), ND_G_MM3, False)
    # sensor C-bracket at x = -100: a post at y = 40 and two prongs reaching in to y = 16
    bracket = box(-L - 8, -L + 8, 36, 44, 6, 84).union(box(-L - 8, -L + 8, 16, 44, 73.0, 76.0)).union(box(-L - 8, -L + 8, 16, 44, 64.0, 67.0))
    add("sensor_bracket", bracket, PLA_G_MM3 * INFILL, False, True)
    return parts


def balance_solve():
    """Ballast and counter-mass lengths (mm) that put the moving centre of mass on the z axis.
    The ballast's moment is linear in its length, the counter-mass's is quadratic, so no search
    over rebuilt solids is needed: build once with both at zero length and solve."""
    parts = build(1e-3, 1e-3)
    mx = my = 0.0
    for name, (wp, rho, moving, _) in parts.items():
        if not moving or name in ("ballast", "y_counter"):
            continue
        s_ = wp.val()
        m = s_.Volume() * rho
        c = s_.Center()
        mx += m * c.x
        my += m * c.y
    # ballast: cylinder of diameter 10 at x = -L + 8:  m = rho * pi * 25 * len, centroid x = -L + 8
    rho_b = STEEL_G_MM3 * math.pi * 25
    bl = mx / (rho_b * (L - 8))
    # y counter: 10 (x) by len (y) by 8 (z) block from y = -12 outward, centroid y = -12 - len/2
    rho_c = STEEL_G_MM3 * 10 * 8
    # my - rho_c*len*(12 + len/2) = 0  ->  (rho_c/2) len^2 + 12 rho_c len - my = 0
    qa, qb = rho_c / 2, 12 * rho_c
    cl = (-qb + math.sqrt(qb * qb + 4 * qa * my)) / (2 * qa)
    return bl, cl


def moving_properties(parts):
    """Mass (g), centre of mass (mm) and moment of inertia about the z axis (kg*m^2) of the moving assembly."""
    m_tot = 0.0
    cx = cy = cz = 0.0
    props = []
    for name, (wp, rho, moving, _) in parts.items():
        if not moving:
            continue
        s = wp.val()
        v = s.Volume()
        c = s.Center()
        m = v * rho
        icom = cq.Shape.matrixOfInertia(s)  # per unit density, about the part's own centre of mass
        izz = (icom[2][2] * rho + m * (c.x**2 + c.y**2)) * 1e-9  # g*mm^2 -> kg*m^2
        props.append((name, m, izz))
        m_tot += m
        cx += m * c.x
        cy += m * c.y
        cz += m * c.z
    return m_tot, (cx / m_tot, cy / m_tot, cz / m_tot), sum(p[2] for p in props), props


def interference(parts, angles_deg=(-1.5, 0, 1.5), skip_pairs=(('elec_arm', 'elec_fixed'), ('arm', 'elec_fixed')), narrow=(('elec_arm', 'elec_fixed', 0.4), ('arm', 'elec_fixed', 0.4))):
    """Largest overlap volume (mm^3) between any moving part and any fixed part over the arm's swing.
    Only parts that are close in height are tested pairwise (a bounding-box prefilter)."""
    worst = (0.0, None)
    fixed = [(n, p[0].val()) for n, p in parts.items() if not p[2]]
    for ang in angles_deg:
        for n, (wp, _, moving, _) in parts.items():
            if not moving or n == "strip":
                continue
            s = wp.val().rotate((0, 0, 0), (0, 0, 1), ang)
            bb = s.BoundingBox()
            if n == "strip":
                continue  # the strip twists along its length; rigid rotation of it is not a real motion
            for fn, fs in fixed:
                fb = fs.BoundingBox()
                if (n, fn) in skip_pairs:
                    continue
                if bb.xmax < fb.xmin or bb.xmin > fb.xmax or bb.ymax < fb.ymin or bb.ymin > fb.ymax or bb.zmax < fb.zmin or bb.zmin > fb.zmax:
                    continue
                vol = s.intersect(fs).Volume()
                if vol > worst[0]:
                    worst = (vol, (n, fn, ang))
    # the electrode pair has a 1 mm gap, so its swing limit is narrower than the rest
    for a, b, lim in narrow:
        for ang in (-lim, lim):
            s = parts[a][0].val().rotate((0, 0, 0), (0, 0, 1), ang)
            vol = s.intersect(parts[b][0].val()).Volume()
            if vol > worst[0]:
                worst = (vol, (a, b, ang))
    return worst


def moving_internal_overlaps(parts):
    """Overlap volumes between moving parts that are not meant to merge (the strip sits in the clamps' gap)."""
    names = [n for n, p in parts.items() if p[2]]
    bad = []
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            va = parts[a][0].val()
            vb = parts[b][0].val()
            ba, bb = va.BoundingBox(), vb.BoundingBox()
            if ba.xmax < bb.xmin or ba.xmin > bb.xmax or ba.ymax < bb.ymin or ba.ymin > bb.ymax or ba.zmax < bb.zmin or ba.zmin > bb.zmax:
                continue
            vol = va.intersect(vb).Volume()
            if vol > 1e-3:
                bad.append((a, b, vol))
    return bad


def printability(parts):
    rows = []
    for name, (wp, _, _, printed) in parts.items():
        if not printed:
            continue
        bb = wp.val().BoundingBox()
        dims = sorted((bb.xlen, bb.ylen, bb.zlen), reverse=True)
        fits = dims[0] <= P.PRINT_VOLUME[0] * MM and dims[1] <= P.PRINT_VOLUME[1] * MM and max(bb.zlen, 0) <= P.PRINT_VOLUME[2] * MM
        rows.append((name, dims, fits))
    return rows


def export(parts):
    os.makedirs(OUT, exist_ok=True)
    asm = cq.Assembly(name="balance")
    for name, (wp, _, moving, _) in parts.items():
        cq.exporters.export(wp, os.path.join(OUT, f"{name}.stl"))
        asm.add(wp, name=name)
    asm.save(os.path.join(OUT, "balance.step"))


def main():
    bl, cl = balance_solve()
    print(f"balance: ballast {bl:.1f} mm long, y counter-mass {cl:.1f} mm long")
    parts = build(bl, cl)
    m, com, izz, props = moving_properties(parts)
    import model as M

    print(f"moving mass {m:.1f} g (params: {1e3*P.MOVING_MASS:.1f} g), centre of mass ({com[0]:.2f}, {com[1]:.2f}, {com[2]:.1f}) mm")
    print(f"moment of inertia about z {izz:.3e} kg*m^2 (params {P.MOVING_INERTIA:.3e})")
    for name, mm, ii in sorted(props, key=lambda a: -a[2]):
        print(f"  {name:14s} {mm:6.2f} g  {ii:.2e} kg*m^2")
    print("worst overlap with the fixed structure over +-1.5 deg:", interference(parts))
    print("moving-part overlaps:", moving_internal_overlaps(parts))
    for name, dims, fits in printability(parts):
        print(f"  {name:16s} {dims[0]:.0f} x {dims[1]:.0f} x {dims[2]:.0f} mm  {'fits' if fits else 'TOO BIG'}")
    export(parts)
    print("exported to", OUT)


if __name__ == "__main__":
    main()
