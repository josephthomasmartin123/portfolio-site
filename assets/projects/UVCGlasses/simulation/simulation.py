"""
Far-UVC Glasses — Kill Efficacy Simulation
==========================================
Three questions, answered in order:
  Q1  How much dose does a pathogen need to receive?
  Q2  What irradiance and power does that require, given the geometry?
  Q3  Can current 222 nm LEDs actually deliver it in a glasses form factor?

Outputs (saved to ./output/):
  fig1_kill_physics.png      — dose thresholds and dwell time landscape
  fig2_feasibility_map.png   — LED count required across operating conditions (3 k scenarios)
  fig3_operating_window.png  — the answer chart: N required vs breathing speed
  fig4_distance_sensitivity.png — how much close range helps (inverse square)
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from matplotlib.colors import BoundaryNorm, LogNorm
from pathlib import Path

# ─── Output ──────────────────────────────────────────────────────────────────
OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

# ─── Global style ─────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":         "sans-serif",
    "font.sans-serif":     ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "font.size":           10,
    "axes.spines.top":     False,
    "axes.spines.right":   False,
    "axes.grid":           True,
    "grid.color":          "#E5E7EB",
    "grid.linewidth":      0.7,
    "axes.labelcolor":     "#374151",
    "axes.labelsize":      10,
    "axes.titlecolor":     "#111827",
    "axes.titlesize":      12,
    "axes.titleweight":    "bold",
    "xtick.color":         "#6B7280",
    "ytick.color":         "#6B7280",
    "xtick.labelsize":     9,
    "ytick.labelsize":     9,
    "figure.facecolor":    "white",
    "axes.facecolor":      "white",
    "text.color":          "#374151",
    "savefig.dpi":         200,
    "savefig.bbox":        "tight",
    "savefig.pad_inches":  0.25,
    "savefig.facecolor":   "white",
    "legend.frameon":      False,
    "legend.fontsize":     9,
    "lines.linewidth":     2.0,
})

# Palette
RED    = "#DC2626"
AMBER  = "#D97706"
GREEN  = "#16A34A"
BLUE   = "#2563EB"
PURPLE = "#7C3AED"
LGRAY  = "#E5E7EB"
GRAY   = "#9CA3AF"
DKGRAY = "#374151"

# ─── Physical parameters ──────────────────────────────────────────────────────
# LED: FBH Berlin 2024 — 1×1 mm AlGaN chip, 200 mA, 20 °C
P_PER_LED_mW = 0.2     # mW optical at 222 nm per chip
mA_PER_LED   = 200     # mA drive current per chip
H_NOM        = 10.0    # nominal LED → veil distance (cm)

# Pathogen inactivation constants at 222 nm (cm²/mJ, base-e, aerosol)
# Source: Blueprint for Far-UVC v1.0 (2025)
K_SCENARIOS = [
    ("Pessimistic\n(SARS-CoV-2)",  2.6,   RED),
    ("Conservative\n(HCoV-229E)", 4.1,   AMBER),
    ("Optimistic\n(HCoV-OC43)",  14.26,  GREEN),
]

# ─── Parameter grids ──────────────────────────────────────────────────────────
T_mm  = np.linspace(1, 10, 300)      # veil thickness (mm)
V_cms = np.linspace(0.3, 15, 300)    # air velocity (cm/s)
H_cm  = np.linspace(1, 20, 200)      # LED→veil distance (cm) — goes to 1 cm
TV, VA = np.meshgrid(T_mm, V_cms)    # shape (V, T)

# ─── Physics ──────────────────────────────────────────────────────────────────
def dwell_s(t_mm, v_cms):
    """Time (s) a particle spends crossing the veil."""
    return (t_mm / 10.0) / v_cms

def irradiance_mW_cm2(P_mW, h_cm):
    """On-axis irradiance from a Lambertian source (mW/cm²)."""
    return P_mW / (np.pi * h_cm ** 2)

def dose_mJ_cm2(P_mW, h_cm, t_mm, v_cms):
    I = irradiance_mW_cm2(P_mW, h_cm)
    return I * dwell_s(t_mm, v_cms)

def N_for_log_red(log_red, k, t_mm, v_cms, h_cm=H_NOM):
    """Number of LEDs to achieve `log_red` log reductions at given conditions."""
    D_req = log_red * np.log(10) / k          # mJ/cm²
    I_req = D_req / dwell_s(t_mm, v_cms)      # mW/cm²
    P_req = I_req * np.pi * h_cm ** 2         # mW
    return P_req / P_PER_LED_mW

# ─── Colormap for N_required maps ─────────────────────────────────────────────
# Green = achievable / feasible, red = not with current tech
N_BOUNDS = [0, 5, 15, 50, 150, 500, 2000, 10000]
N_COLORS = ["#15803D", "#4ADE80", "#A3E635", "#FDE68A", "#FBBF24", "#F87171", "#991B1B"]
cmap_N   = mcolors.ListedColormap(N_COLORS)
norm_N   = BoundaryNorm(N_BOUNDS, cmap_N.N)

# ─── Helpers ──────────────────────────────────────────────────────────────────
def add_feasibility_bands(ax, ymax=50000, label_x=None, label_ha="right"):
    """Horizontal green/amber/red bands for LED count feasibility."""
    ax.axhspan(0.1,   15,    alpha=0.07, color=GREEN, zorder=1)
    ax.axhspan(15,    50,    alpha=0.07, color=AMBER, zorder=1)
    ax.axhspan(50,    ymax,  alpha=0.05, color=RED,   zorder=1)
    if label_x is not None:
        for y_pos, txt, col in [
            (5,    "Feasible  (≤15 LEDs)",          GREEN),
            (28,   "Challenging  (15–50 LEDs)",      AMBER),
            (800,  "Impractical with current SOTA",  RED),
        ]:
            ax.text(label_x, y_pos, txt, ha=label_ha, va="center",
                    color=col, fontsize=8.5, fontweight="semibold", zorder=7)


# ══════════════════════════════════════════════════════════════════════════════
#  FIGURE 1 — Q1: Kill Physics
#  Left:  D90 / D99 dose thresholds for each k scenario
#  Right: dwell time landscape (t_veil × v_air) — the "time budget"
# ══════════════════════════════════════════════════════════════════════════════
fig1, (ax1a, ax1b) = plt.subplots(
    1, 2, figsize=(13, 5.2),
    gridspec_kw={"width_ratios": [1, 1.4]}
)
fig1.suptitle(
    "Q1 — What dose does a pathogen need to receive?",
    fontsize=14, fontweight="bold", color="#111827", y=1.01,
)

# ── Dose threshold bars ───────────────────────────────────────────────────────
ks     = [s[1] for s in K_SCENARIOS]
colors = [s[2] for s in K_SCENARIOS]
d90    = [np.log(10) / k for k in ks]
d99    = [2 * np.log(10) / k for k in ks]
y      = np.arange(len(ks))

ax1a.barh(y + 0.22, d90, height=0.38, color=colors, alpha=0.90, zorder=3)
ax1a.barh(y - 0.22, d99, height=0.38, color=colors, alpha=0.38, zorder=3)

ax1a.set_yticks(y)
ax1a.set_yticklabels([s[0].replace("\n", "  ") for s in K_SCENARIOS], fontsize=9.5)
ax1a.set_xlabel("Dose required  (mJ/cm²)")
ax1a.set_title("Lethal dose thresholds: D90 and D99")
max_d99 = max(d99)
ax1a.set_xlim(0, max_d99 * 1.35)   # headroom for value labels
ax1a.axvline(0, color=DKGRAY, linewidth=0.6)
ax1a.grid(axis="x", zorder=0)
ax1a.grid(axis="y", alpha=0)
ax1a.set_axisbelow(True)

for i, (d9, d99v, col) in enumerate(zip(d90, d99, colors)):
    ax1a.text(d9  + 0.02, i + 0.22, f"{d9:.3f}  mJ/cm²",
              va="center", fontsize=8.5, color=DKGRAY)
    ax1a.text(d99v + 0.02, i - 0.22, f"{d99v:.3f}  mJ/cm²",
              va="center", fontsize=8.5, color=DKGRAY)

ax1a.legend(
    handles=[
        mpatches.Patch(color=DKGRAY, alpha=0.9,  label="D90  (1-log / 90% kill)"),
        mpatches.Patch(color=DKGRAY, alpha=0.38, label="D99  (2-log / 99% kill)"),
    ],
    loc="lower right", fontsize=8.5,
)

# ── Dwell time heatmap ────────────────────────────────────────────────────────
DWELL = dwell_s(TV, VA)

im1b = ax1b.imshow(
    DWELL, origin="lower", aspect="auto",
    extent=[T_mm[0], T_mm[-1], V_cms[0], V_cms[-1]],
    cmap="viridis",
    norm=LogNorm(vmin=0.005, vmax=2.0),
)
cb1b = fig1.colorbar(im1b, ax=ax1b, shrink=0.84, pad=0.02)
cb1b.set_label("Dwell time  (s)", fontsize=9)
cb1b.ax.tick_params(labelsize=8)

CS = ax1b.contour(
    TV, VA, DWELL,
    levels=[0.01, 0.03, 0.1, 0.25, 0.5, 1.0],
    colors="white", linewidths=0.9, alpha=0.75,
)
ax1b.clabel(CS, fmt="%.2f s", fontsize=7.5, colors="white")

# Breathing zone highlight
ax1b.axhspan(V_cms[0], 3.0, alpha=0.15, color="white", zorder=2)
ax1b.text(5.5, 1.65, "Typical sedentary\nbreathing zone",
          color="white", fontsize=8.5, va="center", ha="center",
          fontweight="semibold", zorder=3)

ax1b.set_xlabel("Veil thickness  (mm)")
ax1b.set_ylabel("Air velocity through veil  (cm/s)")
ax1b.set_title("Time air spends in the veil  (the dose opportunity)")

plt.tight_layout()
fig1.savefig(OUT / "fig1_kill_physics.png")
plt.close(fig1)
print("✓  fig1_kill_physics.png")


# ══════════════════════════════════════════════════════════════════════════════
#  FIGURE 2 — Q2/Q3: Feasibility Maps
#  Three panels (one per k scenario) — N LEDs required for D90 at h = 10 cm.
#  This is the main result: how hard is the engineering challenge?
# ══════════════════════════════════════════════════════════════════════════════
fig2, axes2 = plt.subplots(1, 3, figsize=(16, 5.4), sharey=True)
fig2.suptitle(
    "Q2/Q3 — How many LEDs are needed for 90% kill?   (h = 10 cm)",
    fontsize=14, fontweight="bold", color="#111827", y=1.01,
)

for ax, (label, k, kcolor) in zip(axes2, K_SCENARIOS):
    N_map = np.clip(N_for_log_red(1.0, k, TV, VA, H_NOM), 0, 9999)

    ax.imshow(
        N_map, origin="lower", aspect="auto",
        extent=[T_mm[0], T_mm[-1], V_cms[0], V_cms[-1]],
        cmap=cmap_N, norm=norm_N,
    )

    # Contour lines at key thresholds
    for n_thresh, lw, ls in [(15, 1.6, "-"), (50, 1.2, "--")]:
        cs = ax.contour(TV, VA, N_map, levels=[n_thresh],
                        colors="white", linewidths=lw, linestyles=ls, alpha=0.85)
        ax.clabel(cs, fmt=f"N = {n_thresh}", fontsize=7.5, colors="white", inline=True)

    # Breathing zone
    ax.axhspan(V_cms[0], 3.0, alpha=0.10, color="white", zorder=2)
    if ax is axes2[1]:
        ax.text(5.5, 1.65, "Sedentary\nbreathing",
                color="white", fontsize=8, va="center", ha="center",
                fontweight="semibold", zorder=3)

    ax.set_xlabel("Veil thickness  (mm)")
    ax.set_title(label.replace("\n", "   "), color=kcolor, fontsize=11, pad=8)

axes2[0].set_ylabel("Air velocity  (cm/s)")

# Shared colorbar
sm = mpl.cm.ScalarMappable(cmap=cmap_N, norm=norm_N)
sm.set_array([])
cb2 = fig2.colorbar(sm, ax=axes2, shrink=0.72, pad=0.02,
                    ticks=N_BOUNDS)
cb2.ax.set_title("N LEDs\nfor D90", fontsize=9, pad=6, color=DKGRAY)
cb2.ax.set_yticklabels(
    ["0", "5", "15", "50", "150", "500", "2 000", "10 000+"], fontsize=8
)

# Legend for contour lines
legend_items = [
    Line2D([0],[0], color="white", lw=1.6, ls="-",  label="N = 15  (feasibility boundary)"),
    Line2D([0],[0], color="white", lw=1.2, ls="--", label="N = 50"),
    mpatches.Patch(facecolor="white", alpha=0.2, label="Sedentary breathing zone"),
]
axes2[2].legend(
    handles=legend_items, loc="upper right", fontsize=8,
    facecolor="#1F2937", labelcolor="white",
    frameon=True, framealpha=0.8, edgecolor="none",
)

fig2.subplots_adjust(left=0.06, right=0.86, wspace=0.08, top=0.90)
fig2.savefig(OUT / "fig2_feasibility_map.png")
plt.close(fig2)
print("✓  fig2_feasibility_map.png")


# ══════════════════════════════════════════════════════════════════════════════
#  FIGURE 3 — Q3: Operating Window  (the Answer)
#  N_required vs breathing velocity for all three k scenarios.
#  Shaded bands show veil thickness range (1–10 mm).
#  Answers: "under what conditions, if any, is this device feasible?"
# ══════════════════════════════════════════════════════════════════════════════
fig3, ax3 = plt.subplots(figsize=(12, 7))

V_PLOT = np.linspace(0.3, 15, 600)

for (label, k, kcolor), ls in zip(K_SCENARIOS, ["-", "--", "-."]):
    N_mid = N_for_log_red(1.0, k, 5,  V_PLOT, H_NOM)   # t = 5 mm (nominal)
    N_lo  = N_for_log_red(1.0, k, 10, V_PLOT, H_NOM)   # thick veil → fewer LEDs
    N_hi  = N_for_log_red(1.0, k, 1,  V_PLOT, H_NOM)   # thin veil  → more LEDs

    ax3.fill_between(V_PLOT, N_lo, N_hi, color=kcolor, alpha=0.10, zorder=3)
    short = label.replace("\n", "  ")
    ax3.plot(V_PLOT, N_mid, color=kcolor, lw=2.8, ls=ls,
             label=short, zorder=5)

# Feasibility bands
ax3.axhspan(0.1,  15,    alpha=0.07, color=GREEN, zorder=1)
ax3.axhspan(15,   50,    alpha=0.07, color=AMBER, zorder=1)
ax3.axhspan(50,   80000, alpha=0.05, color=RED,   zorder=1)

for y_pos, txt, col in [
    (5,     "Feasible  (≤15 LEDs)",          GREEN),
    (28,    "Challenging  (15–50 LEDs)",      AMBER),
    (3000,  "Impractical with current SOTA",  RED),
]:
    ax3.text(14.8, y_pos, txt, ha="right", va="center",
             color=col, fontsize=9.5, fontweight="semibold", zorder=7)

# Breathing regime shading
ax3.axvspan(0.3, 3.0, alpha=0.04, color=BLUE, zorder=1)
ax3.axvline(3.0, color=BLUE, lw=1.0, ls=":", alpha=0.5, zorder=4)
ax3.text(1.65, 40000, "Sedentary\nbreathing", color=BLUE, fontsize=8.5,
         ha="center", va="bottom", alpha=0.9, zorder=7)
ax3.text(8.5,  40000, "Active / talking", color=GRAY, fontsize=8.5,
         ha="center", va="bottom", alpha=0.8, zorder=7)

# Wearable current draw limit line
WEARABLE_mA     = 500
N_WEARABLE_LIMIT = WEARABLE_mA / mA_PER_LED  # = 2.5
ax3.axhline(N_WEARABLE_LIMIT, color=DKGRAY, lw=1.4, ls=":", alpha=0.55, zorder=6)
ax3.text(4.5, N_WEARABLE_LIMIT * 0.45,
         f"500 mA wearable limit  ({N_WEARABLE_LIMIT:.0f} LEDs @ 200 mA each)",
         color=DKGRAY, fontsize=8, va="top", ha="center", alpha=0.75, zorder=7)

# Annotation: band explanation
ax3.text(0.015, 0.02,
         "Shaded bands = veil thickness range  1 to 10 mm  "
         "(thicker veil = longer dwell time = fewer LEDs needed)",
         transform=ax3.transAxes, fontsize=8, color=GRAY, va="bottom")

ax3.set_yscale("log")
ax3.set_ylim(0.5, 80000)
ax3.set_xlim(0.3, 15)
ax3.set_xlabel("Air velocity through veil  (cm/s)", labelpad=8)
ax3.set_ylabel("LEDs required for D90   [h = 10 cm, t_veil = 5 mm nominal]", labelpad=8)
ax3.set_title(
    "Operating window — is 90% kill achievable with current 222 nm LEDs?",
    pad=12,
)
ax3.legend(loc="lower right", fontsize=10, title="k scenario  (t_veil = 5 mm line)",
           title_fontsize=8.5)

# Secondary y-axis: current draw in mA
ax3r = ax3.twinx()
ax3r.set_yscale("log")
ax3r.set_ylim(0.5 * mA_PER_LED, 80000 * mA_PER_LED)
ax3r.set_ylabel("Total LED current draw  (mA)", color=GRAY, fontsize=9, labelpad=8)
ax3r.tick_params(colors=GRAY, labelsize=8)
ax3r.spines["right"].set_visible(True)
ax3r.spines["right"].set_color(LGRAY)
ax3r.spines["top"].set_visible(False)

plt.tight_layout()
fig3.savefig(OUT / "fig3_operating_window.png")
plt.close(fig3)
print("✓  fig3_operating_window.png")


# ══════════════════════════════════════════════════════════════════════════════
#  FIGURE 4 — Q2: Distance Sensitivity
#  How much does bringing the LEDs closer help? (inverse square law)
#  Left panel:  all 3 k scenarios, t_veil = 5 mm, v = 2 cm/s
#  Right panel: conservative k, 4 t_veil values, v = 2 cm/s
#  h range extended to 1 cm to reveal the close-range sweet spot
# ══════════════════════════════════════════════════════════════════════════════
fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(13, 5.5))
fig4.suptitle(
    "Q2 — Effect of distance: how much does moving the LED closer help?   "
    "(v = 2 cm/s, D90)",
    fontsize=13, fontweight="bold", color="#111827", y=1.01,
)

V_NOM    = 2.0
T_FIXED  = 5.0   # mm — fixed for left panel
T_SCAN   = [1, 2, 5, 10]
T_ALPHAS = [0.40, 0.58, 0.78, 1.0]

# ── Left: k scenarios, t fixed ───────────────────────────────────────────────
for (label, k, kcolor), ls in zip(K_SCENARIOS, ["-", "--", "-."]):
    N_h = N_for_log_red(1.0, k, T_FIXED, V_NOM, H_cm)
    ax4a.plot(H_cm, N_h, color=kcolor, lw=2.5, ls=ls,
              label=label.replace("\n", "  "), zorder=5)

add_feasibility_bands(ax4a, ymax=5000, label_x=19.5, label_ha="right")
ax4a.axvline(H_NOM, color=GRAY, lw=1.2, ls="--", alpha=0.55, zorder=4)
ax4a.text(H_NOM + 0.3, 0.8, "h = 10 cm\n(nominal)",
          fontsize=8, color=GRAY, va="bottom")
ax4a.set_yscale("log")
ax4a.set_ylim(0.5, 5000)
ax4a.set_xlim(H_cm[0], H_cm[-1])
ax4a.set_xlabel("LED-to-veil distance  h  (cm)")
ax4a.set_ylabel("LEDs required for D90")
ax4a.set_title(f"All k scenarios  |  t_veil = {T_FIXED:.0f} mm")
ax4a.legend(fontsize=9, loc="upper left")

# ── Right: veil thickness sweep, conservative k ───────────────────────────────
k_cons  = K_SCENARIOS[1][1]   # 4.1
col_cons = K_SCENARIOS[1][2]  # AMBER

for t_v, alpha in zip(T_SCAN, T_ALPHAS):
    N_h = N_for_log_red(1.0, k_cons, t_v, V_NOM, H_cm)
    ax4b.plot(H_cm, N_h, color=col_cons, alpha=alpha, lw=2.2,
              label=f"t = {t_v} mm", zorder=5)

add_feasibility_bands(ax4b, ymax=5000, label_x=19.5, label_ha="right")
ax4b.axvline(H_NOM, color=GRAY, lw=1.2, ls="--", alpha=0.55, zorder=4)
ax4b.text(H_NOM + 0.3, 0.8, "h = 10 cm\n(nominal)",
          fontsize=8, color=GRAY, va="bottom")
ax4b.set_yscale("log")
ax4b.set_ylim(0.5, 5000)
ax4b.set_xlim(H_cm[0], H_cm[-1])
ax4b.set_xlabel("LED-to-veil distance  h  (cm)")
ax4b.set_title(f"Conservative  k = {k_cons}  |  veil thickness sweep")
ax4b.legend(title="Veil thickness", fontsize=9, title_fontsize=8.5, loc="upper left")

plt.tight_layout()
fig4.savefig(OUT / "fig4_distance_sensitivity.png")
plt.close(fig4)
print("✓  fig4_distance_sensitivity.png")


# ══════════════════════════════════════════════════════════════════════════════
#  FIGURE 5 — Technology Gap
#  What optical power per chip is needed to make the device feasible?
#  Maps current SOTA (FBH Berlin) onto the requirement curve.
#  Answers: how far away are we, and what does the improvement path look like?
# ══════════════════════════════════════════════════════════════════════════════

# FBH Berlin reference points: (wavelength_nm, P_optical_mW, EQE_pct, label)
FBH_REFS = [
    (222, 0.2,  0.02, "222 nm\n(current SOTA)"),
    (226, 2.1,  0.30, "226 nm"),
    (229, 4.2,  0.50, "229 nm"),
    (233, 10.7, 1.10, "233 nm"),
]
V_FORWARD_V = 5.5      # approximate AlGaN forward voltage (V)
I_DRIVE_A   = 0.200    # drive current (A)
P_ELEC_mW   = V_FORWARD_V * I_DRIVE_A * 1000  # = 1100 mW electrical per chip

P_CHIP = np.logspace(np.log10(0.1), np.log10(80), 400)  # mW sweep

fig5, ax5 = plt.subplots(figsize=(11, 6.5))

for (label, k, kcolor), ls in zip(K_SCENARIOS, ["-", "--", "-."]):
    # N required at nominal conditions as function of P_per_LED
    # N = P_required_total / P_per_LED
    P_total_needed = N_for_log_red(1.0, k, 5.0, 2.0, H_NOM) * P_PER_LED_mW
    N_curve = P_total_needed / P_CHIP
    ax5.plot(P_CHIP, N_curve, color=kcolor, lw=2.5, ls=ls,
             label=label.replace("\n", "  "), zorder=5)

# Feasibility bands
ax5.axhspan(0.1,  15,    alpha=0.08, color=GREEN, zorder=1)
ax5.axhspan(15,   50,    alpha=0.08, color=AMBER, zorder=1)
ax5.axhspan(50,   80000, alpha=0.05, color=RED,   zorder=1)
for y_pos, txt, col in [
    (5,    "Feasible  (N ≤ 15)",         GREEN),
    (28,   "Challenging  (15–50)",        AMBER),
    (3000, "Impractical",                 RED),
]:
    ax5.text(72, y_pos, txt, ha="right", va="center",
             color=col, fontsize=9, fontweight="semibold", zorder=7)

# FBH reference lines
for wl, p_opt, eqe, lbl in FBH_REFS:
    col = RED if wl == 222 else GRAY
    lw  = 2.0 if wl == 222 else 1.2
    ax5.axvline(p_opt, color=col, lw=lw, ls="--", alpha=0.7, zorder=4)
    ax5.text(p_opt, 25000,
             f"{lbl}\n({eqe}% EQE)",
             ha="center", va="top", fontsize=7.8, color=col,
             zorder=6, linespacing=1.4)

# Current SOTA shaded "where we are" region
ax5.axvspan(0.1, 0.2, alpha=0.10, color=RED, zorder=2)
ax5.text(0.13, 0.18, "Current\n222 nm", ha="center", va="bottom",
         fontsize=7.5, color=RED, transform=ax5.get_xaxis_transform(),
         zorder=7)

# Required P_per_LED annotation for feasibility (N=15, conservative k)
k_cons = K_SCENARIOS[1][1]
P_total_cons = N_for_log_red(1.0, k_cons, 5.0, 2.0, H_NOM) * P_PER_LED_mW
P_needed_15  = P_total_cons / 15
eqe_needed   = P_needed_15 / P_ELEC_mW * 100
ax5.axvline(P_needed_15, color=AMBER, lw=1.5, ls=":", alpha=0.8, zorder=4)
ax5.text(P_needed_15 * 1.05, 0.7,
         f"Need ~{P_needed_15:.0f} mW/chip\n({eqe_needed:.1f}% EQE) for N=15\n(conservative k)",
         ha="left", va="bottom", fontsize=8, color=AMBER, zorder=7)

ax5.set_xscale("log")
ax5.set_yscale("log")
ax5.set_ylim(0.3, 50000)
ax5.set_xlim(0.1, 80)
ax5.set_xlabel("Optical power per 222 nm chip  (mW)", labelpad=8)
ax5.set_ylabel("LEDs required for D90   [h = 10 cm, t = 5 mm, v = 2 cm/s]", labelpad=8)
ax5.set_title(
    "Technology gap — what LED performance does the device need?",
    pad=12,
)
ax5.legend(loc="lower left", fontsize=9.5,
           title="k scenario", title_fontsize=8.5)

# Secondary x-axis: EQE %
ax5t = ax5.twiny()
ax5t.set_xscale("log")
ax5t.set_xlim(0.1 / P_ELEC_mW * 100, 80 / P_ELEC_mW * 100)
ax5t.set_xlabel("Approximate EQE at 222 nm  (%)", labelpad=8, color=GRAY)
ax5t.tick_params(colors=GRAY, labelsize=8)
ax5t.spines["top"].set_color(LGRAY)
ax5t.spines["right"].set_visible(False)
ax5t.spines["left"].set_visible(False)
ax5t.spines["bottom"].set_visible(False)

plt.tight_layout()
fig5.savefig(OUT / "fig5_technology_gap.png")
plt.close(fig5)
print("✓  fig5_technology_gap.png")


# ─── Console summary of key operating points ─────────────────────────────────
print("\n── Key numerical results ──────────────────────────────────────────────")
cases = [
    ("Nominal (h=10, t=5mm, v=2 cm/s)",   H_NOM, 5.0, 2.0),
    ("Close range (h=5, t=5mm, v=2 cm/s)", 5.0,  5.0, 2.0),
    ("Very close (h=2, t=5mm, v=2 cm/s)",  2.0,  5.0, 2.0),
    ("Thick veil (h=10, t=10mm, v=1 cm/s)", H_NOM, 10.0, 1.0),
    ("Thin veil (h=10, t=1mm, v=5 cm/s)",  H_NOM,  1.0, 5.0),
]
print(f"{'Scenario':<42} {'k=2.6':>8} {'k=4.1':>8} {'k=14.3':>8}  LEDs  (D90)")
print("─" * 72)
for desc, h, t, v in cases:
    ns = [N_for_log_red(1.0, k, t, v, h) for _, k, _ in K_SCENARIOS]
    print(f"  {desc:<40} {ns[0]:>8.0f} {ns[1]:>8.0f} {ns[2]:>8.0f}")

print("\n── Wearable power budget ──────────────────────────────────────────────")
for N in [2, 5, 10, 20, 50]:
    P_opt = N * P_PER_LED_mW
    I_tot = N * mA_PER_LED
    print(f"  N={N:>3} LEDs → {P_opt:.1f} mW optical, {I_tot} mA total draw")

print(f"\nAll figures saved → {OUT}/\n")
