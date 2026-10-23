"""
balance.py — CadQuery model of the torsion balance (`FORCEBAL`), G2.

    ~/.venvs/lab-hw/bin/python hardware/balance/balance.py

Builds every part in millimetres from `params.py`, computes the moving assembly's mass and moment of
inertia and compares them with the model's, checks that nothing collides over the arm's swing, that every
printed part fits the printer, that the balance sits inside the enclosure with room to spare, derives the
fastener list from the holes it cuts, and exports STL files (one per part, printable on the Creality K1) and
a STEP assembly to `hardware/balance/cad/`.

Layout (z up, the pivot axis is the z axis):
  base plate, two uprights and a cross beam carry the top strip clamp at z = 110..120.
  A stainless strip (4 mm x 50 um x 30 mm, z = 80..110) hangs from it to the hub of the arm. The arm lies
  along x: the device mount (+x), a counterweight pocket (-x).
  Eddy-current damper (+x, y > 0): a 0.3 mm copper vane on the arm moves between two N42 discs held fixed to
  the base. Optical sensor (-x end): a flag tab on the arm moves through a C-bracket whose two prongs carry
  the LED board (above) and the photodiode board (below). Electrostatic plates at x = 72..88.
  Every fixed part stands on a flanged foot bolted through the base with M3 screws into captured nuts; the
  strip clamps' halves are bolted together the same way. A printed frame with five drop-in acrylic panels
  encloses it all.
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
CU_G_MM3, STEEL_G_MM3, ND_G_MM3, ACRYLIC_G_MM3 = 8.96e-3, 7.9e-3, 7.5e-3, 1.18e-3
BRASS_G_MM3 = P.BRASS_DENSITY

# vertical layout
Z_ARM0, Z_ARM1 = 58.0, 66.0
Z_HUB1 = 72.0
Z_LOW0, Z_LOW1 = 72.0, 80.0  # lower strip clamp
Z_TOP0, Z_TOP1 = 110.0, 120.0  # top strip clamp
Z_BEAM0, Z_BEAM1 = 120.0, 132.0
T_STRIP = P.STRIP_THICKNESS * MM
W_STRIP = P.STRIP_WIDTH * MM
VANE_T = P.VANE_THICKNESS * MM
HALF = 5.0  # thickness of each strip-clamp half, mm
BASE_HALF = 109.0  # base plate is 218 x 218 mm (the K1 prints 220 x 220); the sensor bracket reaches x = -108
FOOT_Z0, FOOT_Z1 = 6.0, 10.0  # flange of each foot, on top of the 6 mm base
M3_CLEAR, M3_PILOT, M3_HEAD = 3.4, 2.6, 6.2
NUT_DIA, NUT_DEPTH = 6.35, 2.6  # M3 nut, 5.5 mm across flats (6.35 circumscribed), pocket depth

FASTENERS = []  # (kind, where) appended as holes are cut


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def cyl_z(x, y, z0, z1, d):
    return cq.Workplane("XY").circle(d / 2).extrude(z1 - z0).translate((x, y, z0))


def cyl_y(x, z, y0, y1, d):
    return cq.Workplane("XZ").circle(d / 2).extrude(-(y1 - y0)).translate((x, y0, z))


def nut_pocket_z(x, y, z_top, depth=NUT_DEPTH):
    return cq.Workplane("XY").polygon(6, NUT_DIA).extrude(depth).translate((x, y, z_top - depth))


def nut_pocket_y(x, z, y_face, direction, depth=NUT_DEPTH):
    """Hex pocket in a face normal to y; direction +1 cuts toward +y from y_face, -1 toward -y."""
    w = cq.Workplane("XZ").polygon(6, NUT_DIA).extrude(-depth * direction).translate((x, y_face, z))
    return w


def with_foot(part, x0, x1, y0, y1, hole_xy, base_holes, label):
    """Add a flanged foot under a fixed part: flange y0..y1 (expanded 10 mm along y), one M3 screw from below
    through the base at each hole, into a nut captured in a hex pocket in the flange's top face."""
    foot = box(x0, x1, y0, y1, FOOT_Z0, FOOT_Z1)
    part = part.union(foot)
    for (hx, hy) in hole_xy:
        part = part.cut(cyl_z(hx, hy, FOOT_Z0 - 0.1, FOOT_Z1 + 0.1, M3_CLEAR)).cut(nut_pocket_z(hx, hy, FOOT_Z1))
        base_holes.append((hx, hy))
        FASTENERS.append(("M3x12 pan head screw", f"{label}: from below through the base into the foot"))
        FASTENERS.append(("M3 nut", f"{label}: captured in the foot"))
        FASTENERS.append(("M3 flat washer", f"{label}: under the screw head on the base"))
    return part


def clamp_pair(prefix, z0, z1):
    """Two clamp halves, each HALF thick either side of the strip, bolted together by two M3 screws along y at
    x = +-7 (head and washer on half a, nut captured in half b). Returns {name: solid}."""
    out = {}
    ya = (-T_STRIP / 2 - HALF, -T_STRIP / 2)
    yb = (T_STRIP / 2, T_STRIP / 2 + HALF)
    zc = (z0 + z1) / 2
    for tag, (y0, y1) in (("a", ya), ("b", yb)):
        h = box(-10, 10, y0, y1, z0, z1)
        for x in (-7, 7):
            h = h.cut(cyl_y(x, zc, y0 - 1, y1 + 1, M3_CLEAR))
            if tag == "b":
                h = h.cut(nut_pocket_y(x, zc, y1, -1))
        out[f"{prefix}_clamp_{tag}"] = h
    for x in (-7, 7):
        FASTENERS.append(("M3x12 pan head screw", f"{prefix} strip clamp bolt"))
        FASTENERS.append(("M3 nut", f"{prefix} strip clamp bolt, captured in half b"))
        FASTENERS.append(("M3 flat washer", f"{prefix} strip clamp bolt, under the head"))
    return out


def build(ballast_len=14.0, ballast_y=0.0):
    """All parts. ballast_len and ballast_y (mm) are solved by balance_solve() so the moving assembly's centre of
    mass sits on the pivot axis: the length balances x, the hole's offset in y balances the vane's side-load."""
    FASTENERS.clear()
    parts = {}  # name -> (solid, density g/mm3, moving, printed)
    base_holes = []

    def add(name, wp, density, moving, printed=False):
        parts[name] = (wp, density, moving, printed)

    pla = PLA_G_MM3 * INFILL
    # ---- fixed structure, each on a flanged foot -------------------------------------------------
    # the gantry is one printed piece (two legs and the cross beam), lying on its side on the bed; each leg has a flanged foot
    gantry = box(-6, 6, 39, 51, 6, Z_BEAM1).union(box(-6, 6, -51, -39, 6, Z_BEAM1)).union(box(-6, 6, -51, 51, Z_BEAM0, Z_BEAM1))
    # the top clamp's half a is screwed up into the beam from above: M3x12 through a counterbored hole in the beam
    for x in (-7, 7):
        gantry = gantry.cut(cyl_z(x, -2.5, Z_BEAM0 - 0.1, Z_BEAM1 + 0.1, M3_CLEAR)).cut(cyl_z(x, -2.5, Z_BEAM1 - 6, Z_BEAM1 + 0.1, M3_HEAD))
        FASTENERS.append(("M3x12 pan head screw", "top strip clamp half a, from above through the beam"))
        FASTENERS.append(("M3 flat washer", "top strip clamp half a, under the screw head"))
    gantry = with_foot(gantry, -16, 16, 39, 51, [(-11, 45), (11, 45)], base_holes, "gantry leg +y")
    gantry = with_foot(gantry, -16, 16, -51, -39, [(-11, -45), (11, -45)], base_holes, "gantry leg -y")
    add("gantry", gantry, pla, False, True)
    top = clamp_pair("top", Z_TOP0, Z_TOP1)
    for name, solid in top.items():
        if name.endswith("_a"):
            for x in (-7, 7):
                solid = solid.cut(cyl_z(x, -2.5, Z_TOP1 - 6, Z_TOP1 + 0.1, M3_PILOT))
        add(name, solid, pla, False, True)

    # ---- the moving assembly -----------------------------------------------------------------
    # one printed piece: the arm, its hub, the device-mount plate (+x) and the counterweight pocket (-x)
    arm = box(-L, L, -5, 5, Z_ARM0, Z_ARM1).union(box(-12, 12, -12, 12, Z_ARM0, Z_HUB1))
    arm = arm.union(box(L - 8, L, -14, 14, Z_ARM0 - 6, Z_ARM1 + 18))  # device mount plate
    arm = arm.union(box(-L, -L + 16, -10, 10, Z_ARM0 - 6, Z_ARM1 + 4))  # counterweight pocket body
    arm = arm.cut(cyl_z(-L + 8, ballast_y, Z_ARM0 - 6.5, Z_ARM1 + 4.5, 10.3))  # ballast hole
    for x in (-60, -30, 30, 60):  # lightening holes through the arm's web
        arm = arm.cut(cq.Workplane("XY").circle(2.5).extrude(20, both=True).translate((x, 0, (Z_ARM0 + Z_ARM1) / 2)))
    # the lower clamp's half a is screwed down into the hub from below: counterbored M3x12
    for x in (-7, 7):
        arm = arm.cut(cyl_z(x, -2.5, Z_ARM0 - 0.1, Z_HUB1 + 0.1, M3_CLEAR)).cut(cyl_z(x, -2.5, Z_ARM0 - 0.1, Z_ARM0 + 8, M3_HEAD))
        FASTENERS.append(("M3x12 pan head screw", "lower strip clamp half a, from below through the hub"))
        FASTENERS.append(("M3 flat washer", "lower strip clamp half a, under the screw head"))
    add("arm", arm, pla, True, True)
    low = clamp_pair("low", Z_LOW0, Z_LOW1)
    for name, solid in low.items():
        if name.endswith("_a"):
            for x in (-7, 7):
                solid = solid.cut(cyl_z(x, -2.5, Z_LOW0 - 0.1, Z_LOW0 + 6, M3_PILOT))
        add(name, solid, pla, True, True)
    add("strip", box(-W_STRIP / 2, W_STRIP / 2, -T_STRIP / 2, T_STRIP / 2, Z_LOW1 - 6, Z_TOP0 + 6), STEEL_G_MM3, True)
    # brass masses (non-magnetic): ballast in the pocket (-x), a dummy device at +x
    add("ballast", cyl_z(-L + 8, ballast_y, Z_ARM0 - 6, Z_ARM0 - 6 + ballast_len, 10.0), BRASS_G_MM3, True)
    add("dut_dummy", box(L - 18, L - 8, -5, 5, Z_ARM1, Z_ARM1 + 10), BRASS_G_MM3, True)  # stands for the device
    # flag: a riser on the arm's -x end face and a horizontal tab that crosses the sensor beam at y = 22
    riser = box(-L - 4, -L, 0, 4, Z_ARM1, 71)
    tab = box(-L - 8, -L + 0.5, 0, 22, 70.0, 70.6)
    add("flag", riser.union(tab), PLA_G_MM3, True, True)
    # damper vane: 0.3 mm copper plate centred at z = 62.5 between the discs, in a slot of a holder glued to the arm's side
    vane_box = box(50, 70, 8, 30, 62.5 - VANE_T / 2, 62.5 + VANE_T / 2)
    add("vane_holder", box(55, 65, 5, 10, Z_ARM0, Z_ARM1 + 1).cut(vane_box), pla, True, True)
    add("vane", vane_box, CU_G_MM3, True)
    # electrostatic plates at x = 72..88: a moving tab on the arm's +y side (copper foil tape on its +y face, reached
    # through the strip's clamp) and a fixed plate on the base, 1 mm across
    add("elec_arm", box(72, 88, 5, 7, 52.0, 70.0), pla, True, True)
    elec = box(72, 88, 8, 12, 6.0, 70.0)
    add("elec_fixed", with_foot(elec, 72, 88, -2, 22, [(80, 3), (80, 17)], base_holes, "elec_fixed"), pla, False, True)

    # ---- fixed: damper (two N42 discs) and sensor bracket ------------------------------------------
    holder = box(52, 68, 36, 44, 6, 70).union(box(52, 68, 20, 44, 54.0, 58.0)).union(box(52, 68, 20, 44, 67.0, 70.0))
    holder = holder.union(box(52, 68, 20, 44, 58.0, 61.0).cut(cyl_z(60, 25, 57.0, 62.0, 6.2)))
    holder = holder.union(box(52, 68, 20, 44, 64.0, 67.0).cut(cyl_z(60, 25, 63.0, 68.0, 6.2)))
    holder = with_foot(holder, 52, 68, 26, 54, [(60, 31), (60, 49)], base_holes, "damper_holder")
    add("damper_holder", holder, pla, False, True)
    add("magnet_low", cyl_z(60, 25, 58.0, 61.0, 6.0), ND_G_MM3, False)
    add("magnet_up", cyl_z(60, 25, 64.0, 67.0, 6.0), ND_G_MM3, False)
    bracket = box(-L - 8, -L + 8, 36, 44, 6, 84).union(box(-L - 8, -L + 8, 16, 44, 73.0, 76.0)).union(box(-L - 8, -L + 8, 16, 44, 64.0, 67.0))
    bracket = with_foot(bracket, -L - 8, -L + 8, 26, 54, [(-L, 31), (-L, 49)], base_holes, "sensor_bracket")
    add("sensor_bracket", bracket, pla, False, True)

    # the base, with a clearance hole under every foot
    base = box(-BASE_HALF, BASE_HALF, -BASE_HALF, BASE_HALF, 0, 6)
    for (hx, hy) in base_holes:
        base = base.cut(cyl_z(hx, hy, -0.1, 6.1, M3_CLEAR))
    add("base", base, pla, False, True)

    # ---- enclosure: four corner posts with slots, four pinwheel side panels, a lid ------------------
    wi, di, hi = (v * MM for v in P.ENCL_INNER)
    t = P.PANEL_T * MM
    slot_clear = 0.4
    hx, hy = wi / 2, di / 2
    # a pinwheel: the y panels run the full width plus one thickness at one end, the x panels butt against them,
    # so the four corner squares each belong to exactly one panel
    panels = {
        "panel_px": box(hx, hx + t, -hy, hy, 0, hi),
        "panel_nx": box(-hx - t, -hx, -hy, hy, 0, hi),
        "panel_py": box(-hx, hx + t, hy, hy + t, 0, hi),
        "panel_ny": box(-hx - t, hx, -hy - t, -hy, 0, hi),
    }
    lid = box(-hx - t - 10, hx + t + 10, -hy - t - 10, hy + t + 10, hi, hi + t)
    pw = P.ENCL_POST * MM
    for sx in (1, -1):
        for sy in (1, -1):
            cx, cy = sx * (hx + t / 2), sy * (hy + t / 2)
            post = box(cx - pw / 2, cx + pw / 2, cy - pw / 2, cy + pw / 2, 0, hi)
            for pn, pnl in panels.items():
                bb = pnl.val().BoundingBox()
                grown = box(bb.xmin - slot_clear / 2, bb.xmax + slot_clear / 2, bb.ymin - slot_clear / 2, bb.ymax + slot_clear / 2, bb.zmin - 1, bb.zmax + 1)
                post = post.cut(grown)
            add(f"encl_post_{'p' if sx > 0 else 'n'}{'p' if sy > 0 else 'n'}", post, pla, False, True)
    for pn, pnl in panels.items():
        add(pn, pnl, ACRYLIC_G_MM3, False, False)
    add("encl_lid", lid, ACRYLIC_G_MM3, False, False)
    return parts


def balance_solve():
    """Ballast length and y offset (mm) that put the moving centre of mass on the z axis. The ballast's x moment is
    linear in its length and its y offset then cancels the rest's y moment, so no search over rebuilt solids is
    needed: build once with a stub ballast and solve."""
    bl, by = 14.0, 0.0
    rho_b = BRASS_G_MM3 * math.pi * 25  # ballast: diameter 10 at x = -L + 8
    for _ in range(4):  # the hole's own position shifts the arm's centre of mass a little, so iterate
        parts = build(bl, by)
        mx = my = 0.0
        for name, (wp, rho, moving, _) in parts.items():
            if not moving or name == "ballast":
                continue
            s_ = wp.val()
            m = s_.Volume() * rho
            c = s_.Center()
            mx += m * c.x
            my += m * c.y
        bl = mx / (rho_b * (L - 8))
        by = -my / (rho_b * bl)
    return bl, by


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


def _disjoint(ba, bb):
    return ba.xmax < bb.xmin or ba.xmin > bb.xmax or ba.ymax < bb.ymin or ba.ymin > bb.ymax or ba.zmax < bb.zmin or ba.zmin > bb.zmax


def interference(parts, angles_deg=(-1.5, 0, 1.5), skip_pairs=(("elec_arm", "elec_fixed"), ("arm", "elec_fixed")), narrow=(("elec_arm", "elec_fixed", 0.4), ("arm", "elec_fixed", 0.4))):
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
            for fn, fs in fixed:
                if (n, fn) in skip_pairs:
                    continue
                if _disjoint(bb, fs.BoundingBox()):
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


def fixed_overlaps(parts):
    """Overlap volumes between fixed parts that are not meant to merge (clamp halves, enclosure, balance)."""
    names = [n for n, p in parts.items() if not p[2]]
    bad = []
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            va, vb = parts[a][0].val(), parts[b][0].val()
            if _disjoint(va.BoundingBox(), vb.BoundingBox()):
                continue
            vol = va.intersect(vb).Volume()
            if vol > 1e-3:
                bad.append((a, b, round(vol, 3)))
    return bad


def moving_internal_overlaps(parts):
    """Overlap volumes between moving parts that are not meant to merge (the strip sits in the clamps' gap)."""
    names = [n for n, p in parts.items() if p[2]]
    bad = []
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            va = parts[a][0].val()
            vb = parts[b][0].val()
            if _disjoint(va.BoundingBox(), vb.BoundingBox()):
                continue
            vol = va.intersect(vb).Volume()
            if vol > 1e-3:
                bad.append((a, b, vol))
    return bad


def enclosure_clearance(parts):
    """Smallest gap (mm) between any balance part (everything not part of the enclosure) and the enclosure's clear volume's walls."""
    wi, di, hi = (v * MM for v in P.ENCL_INNER)
    gap = 1e9
    for n, (wp, _, _, _) in parts.items():
        if n.startswith(("panel_", "encl_")):
            continue
        bb = wp.val().BoundingBox()
        gap = min(gap, wi / 2 - bb.xmax, wi / 2 + bb.xmin, di / 2 - bb.ymax, di / 2 + bb.ymin, hi - bb.zmax)
    return gap


def printability(parts):
    rows = []
    for name, (wp, _, _, printed) in parts.items():
        if not printed:
            continue
        bb = wp.val().BoundingBox()
        dims = sorted((bb.xlen, bb.ylen, bb.zlen), reverse=True)
        fits = bb.xlen <= P.PRINT_VOLUME[0] * MM and bb.ylen <= P.PRINT_VOLUME[1] * MM and bb.zlen <= P.PRINT_VOLUME[2] * MM
        rows.append((name, dims, fits))
    return rows


def fastener_totals():
    """{kind: count} from the holes the CAD cut."""
    totals = {}
    for kind, _ in FASTENERS:
        totals[kind] = totals.get(kind, 0) + 1
    return totals


def panel_cut_list(parts):
    """Acrylic panels to buy: {(w, h, t): count}, in mm."""
    out = {}
    for n, (wp, _, _, printed) in parts.items():
        if n.startswith(("panel_", "encl_lid")):
            bb = wp.val().BoundingBox()
            dims = sorted((round(bb.xlen, 1), round(bb.ylen, 1), round(bb.zlen, 1)), reverse=True)
            out[tuple(dims)] = out.get(tuple(dims), 0) + 1
    return out


def export(parts):
    os.makedirs(OUT, exist_ok=True)
    asm = cq.Assembly(name="balance")
    for name, (wp, _, moving, _) in parts.items():
        cq.exporters.export(wp, os.path.join(OUT, f"{name}.stl"))
        asm.add(wp, name=name)
    asm.save(os.path.join(OUT, "balance.step"))


def main():
    bl, cl = balance_solve()
    print(f"balance: brass ballast {bl:.1f} mm long, hole offset {cl:+.2f} mm in y")
    parts = build(bl, cl)
    m, com, izz, props = moving_properties(parts)
    print(f"moving mass {m:.1f} g (params: {1e3*P.MOVING_MASS:.1f} g), centre of mass ({com[0]:.2f}, {com[1]:.2f}, {com[2]:.1f}) mm")
    print(f"moment of inertia about z {izz:.3e} kg*m^2 (params {P.MOVING_INERTIA:.3e})")
    for name, mm, ii in sorted(props, key=lambda a: -a[2]):
        print(f"  {name:14s} {mm:6.2f} g  {ii:.2e} kg*m^2")
    print("worst overlap with the fixed structure over +-1.5 deg:", interference(parts))
    print("moving-part overlaps:", moving_internal_overlaps(parts))
    print("fixed-part overlaps:", fixed_overlaps(parts))
    print(f"enclosure clearance: {enclosure_clearance(parts):.1f} mm")
    print("fasteners:", fastener_totals())
    print("acrylic cut list (w x h x t mm: count):", panel_cut_list(parts))
    for name, dims, fits in printability(parts):
        print(f"  {name:16s} {dims[0]:.0f} x {dims[1]:.0f} x {dims[2]:.0f} mm  {'fits' if fits else 'TOO BIG'}")
    export(parts)
    print("exported to", OUT)


if __name__ == "__main__":
    main()
