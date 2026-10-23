"""
render.py — PNG views of the balance assembly (for review without a CAD viewer).

    ~/.venvs/lab-hw/bin/python hardware/balance/render.py     # writes cad/views.png
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import balance as B

COLORS = {"base": "#c9c9c9", "arm": "#2a7fff", "strip": "#d4a017", "vane": "#b87333", "ballast": "#555555", "dut_dummy": "#555555", "y_counter": "#555555", "flag": "#111111", "magnet_low": "#aa2222", "magnet_up": "#aa2222"}


def draw(ax, parts, elev, azim, title):
    for name, (wp, _, moving, _) in parts.items():
        verts, tris = wp.val().tessellate(0.2)
        v = np.array([(p.x, p.y, p.z) for p in verts])
        t = np.array(tris)
        col = COLORS.get(name, "#2a7fff" if moving else "#9fb6c9")
        poly = Poly3DCollection(v[t], facecolor=col, edgecolor="none", alpha=0.9 if name != "base" else 0.35)
        # simple shading by face normal
        n = np.cross(v[t][:, 1] - v[t][:, 0], v[t][:, 2] - v[t][:, 0])
        n = n / (np.linalg.norm(n, axis=1)[:, None] + 1e-12)
        shade = 0.55 + 0.45 * np.abs(n @ np.array([0.3, -0.5, 0.8]))
        base = np.array(matplotlib.colors.to_rgb(col))
        poly.set_facecolor([tuple(np.clip(base * s, 0, 1)) for s in shade])
        ax.add_collection3d(poly)
    ax.set_xlim(-110, 110)
    ax.set_ylim(-110, 110)
    ax.set_zlim(0, 220)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")


def main():
    bl, cl = B.balance_solve()
    parts = B.build(bl, cl)
    fig = plt.figure(figsize=(14, 7))
    for i, (e, a, t) in enumerate(((24, -55, "oblique"), (90, -90, "top (flag and sensor at -x, damper at +x)"))):
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        draw(ax, parts, e, a, t)
    out = os.path.join(B.OUT, "views.png")
    os.makedirs(B.OUT, exist_ok=True)
    fig.savefig(out, dpi=110, bbox_inches="tight")
    print("wrote", out)


if __name__ == "__main__":
    main()
