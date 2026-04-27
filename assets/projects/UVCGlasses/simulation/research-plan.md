# Far-UVC Glasses — Kill Efficacy: Research Plan

**Central question: can a head-mounted 222nm UVC veil kill airborne pathogens fast enough to protect the wearer during normal breathing?**

This plan works through three questions in order, from biology to engineering:

1. Can a thin UVC veil kill pathogens at all — and how much dose does it need?
2. What optical power at the veil does that require, and how does geometry affect it?
3. Can current 222nm LED technology actually deliver that power in a glasses form factor?

---

## Question 1 — Can a veil kill pathogens? What dose is required?

### Kill model

Far-UVC inactivation follows a single-hit exponential:

```
Survival fraction S = exp(−k × D)
Log reduction      = k × D / ln(10)
```

where `D` (mJ/cm²) is the delivered dose and `k` (cm²/mJ) is the pathogen's susceptibility constant.

**Target dose thresholds:**

| Kill level | Dose required (conservative k=4.1) | Dose required (optimistic k=14.26) |
|---|---|---|
| D90 (1 log reduction) | 0.56 mJ/cm² | 0.16 mJ/cm² |
| D99 (2 log reductions) | 1.12 mJ/cm² | 0.32 mJ/cm² |

### Dose delivered by the veil

A particle passes through the veil in one dimension. Dwell time = veil thickness / air velocity. Dose accumulates at the rate of the local irradiance:

```
t_dwell = t_veil / v_air       [s]
D       = I × t_dwell          [mJ/cm²]
```

**Key insight:** normal sedentary breathing pulls ~250 mL/s through ~200 cm² of face area, giving an air velocity at the veil of roughly 1–3 cm/s. This is slow. A 5mm-thick veil at 2 cm/s gives a dwell time of **0.25 seconds** — which is the primary lever available.

Sneezing (~100 mph, 4500 cm/s) gives a dwell time of ~0.001s through the same veil. The device cannot realistically protect against sneezes.

### Simulation output for Q1

- Required irradiance `I_required = D_target / t_dwell` as a function of veil thickness and breathing velocity
- This gives the **target irradiance number** that engineering must hit

---

## Question 2 — What optical power does that require?

### Geometry and irradiance model

LEDs on the glasses frame point toward the breathing zone. At distance `h` from LED to veil, treating the array as a Lambertian source (no focusing optics — conservative baseline):

```
I(h) = P_total / (π × h²)     [mW/cm²]
```

Within the veil (1–10 mm thick at h ≈ 10 cm), the variation in h across the veil depth is <1%, so irradiance is constant through the veil. The inverse square law sensitivity to h matters when comparing different device geometries.

**Rearranging to find required power:**

```
P_required = I_required × π × h²    [mW]
```

### Simulation output for Q2

- `P_required` for D90 and D99 as a function of: h (distance), t_veil (thickness), v_air (breathing speed)
- Sensitivity heatmaps: how much does P_required change as each variable shifts?
- This gives the **target optical power** that the LED array must deliver

---

## Question 3 — Can current LEDs deliver it?

### State of the art at 222nm

Source: FBH Berlin (2024)

| Wavelength | Optical power/chip | EQE  | Drive conditions |
|---|---|---|---|
| 222 nm | **0.2 mW** | 0.02% | 200 mA, 20°C, 1×1 mm chip |
| 226 nm | 2.1 mW | 0.3% | same |
| 229 nm | 4.2 mW | 0.5% | same |
| 233 nm | 10.7 mW | 1.1% | same |

EQE plummets exponentially toward 222nm. 222nm is ~15× less powerful than 229nm per chip.

Array output: `P_total = N × 0.2 mW`

Power draw: each chip draws 200 mA. N chips → `I_draw = N × 200 mA` — this is the form-factor constraint.

### Simulation output for Q3

- N chips required for D90/D99 across the breathing/geometry parameter space
- Power draw (mA total) at that N — does it fit in a wearable battery budget?
- **Go/no-go assessment**: is there a plausible operating point (realistic N, h, t_veil, v) where the device achieves D90?

---

## Kill constant reference data

Source: Blueprint for Far-UVC v1.0 (2025)

| Pathogen | k (cm²/mJ) | Scenario | Study |
|---|---|---|---|
| SARS-CoV-2 | 2.6 | pessimistic | Kitagawa 2023 |
| HCoV-229E | 4.1 | conservative | Buonanno 2020 |
| HCoV-OC43 | 14.26 | optimistic | Lu 2025 |
| S. epidermidis | 3.05 | bacteria, conservative | Lu 2024 |
| E. coli | 21.93 | bacteria, susceptible | Lu 2024 |

Use k = {2.6, 4.1, 14.26} as the scenario set throughout.

---

## Safety constraint (not the focus — tracked as a bound)

ACGIH 8-hour TLV at 222nm: **3 mJ/cm²/day** (eye/mucous membrane).

The simulation will check: at the N required for D90, does continuous-wear daily dose approach this limit? This is a design constraint, not a showstopper at this stage.

---

## Appendix — open questions (not addressed in this phase)

- Focusing optics: what lens concentration factor is physically realistic at glasses scale? Could reduce N_required significantly.
- CFD: is the breathing velocity estimate (bulk flow / face area) representative, or are local velocities at the veil plane higher?
- Duty cycle: how many hours/day of use is assumed?
- Veil geometry: horizontal vs. vertical orientation, and whether all inspired air actually passes through the veil.
- Sneeze mitigation: is there a separate mode (triggered by sound/pressure sensor) that ramps intensity for a sneeze event?
- LED roadmap: at what efficiency improvement does 222nm LED technology become viable for this application?

---

## Visual output style

All plots: clean, modern — minimal gridlines, no chart junk, tight layouts, considered colour palette (e.g. viridis for heatmaps, curated discrete colours for line plots). Publication/dashboard quality.

---

## Key findings (simulation v1)

All figures saved to `simulation/output/`.

### Q1 — Dose required
- D90 ranges from **0.161 mJ/cm²** (optimistic, k=14.26) to **0.886 mJ/cm²** (pessimistic, k=2.6)
- Dwell time through a 5 mm veil at sedentary breathing (2 cm/s): **~0.25 s** — a generous time budget

### Q2 — Power required at h = 10 cm
- Nominal conditions (h=10 cm, t=5 mm, v=2 cm/s): requires **3 500–5 600 mW** (conservative to pessimistic)
- Even with optimistic k=14.26: still requires **~1 000 mW** = 1 W of 222 nm optical power

### Q3 — LED feasibility
| Scenario | k=2.6 | k=4.1 | k=14.3 | Comment |
|---|---|---|---|---|
| h=10 cm, t=5 mm, v=2 cm/s | 5 564 | 3 529 | 1 015 | Nominal — completely infeasible |
| h=5 cm, t=5 mm, v=2 cm/s | 1 391 | 882 | 254 | Closer — still infeasible |
| h=2 cm, t=5 mm, v=2 cm/s | 223 | 141 | **41** | Very close — marginal (optimistic k only) |
| h=10 cm, t=10 mm, v=1 cm/s | 1 391 | 882 | 254 | Thick slow veil — still infeasible |

### Wearable power budget
At 200 mA/chip drive current, even 10 LEDs draws 2 A — a significant wearable power challenge.
A realistic "glasses" current budget of 500 mA permits only **2 LEDs** (0.4 mW optical) — roughly **3 orders of magnitude** below what's needed at nominal geometry.

### Answer to the central question
**No — current 222 nm LED technology cannot power a glasses-mounted UVC veil that achieves meaningful pathogen kill at breathing distances.** The gap is 2–3 orders of magnitude in optical power. The only borderline scenario requires: optimistic k values, LED-to-veil distance ≤ 2 cm, very slow breathing (≤ 1 cm/s), and still draws ~8 A.

The device concept is not ruled out permanently — it is a technology readiness problem. 222 nm LED efficiency needs to improve from ~0.02% EQE to ~2–5% (100–250× improvement) before the wearable form factor becomes viable.

---

## Simulation status

- [x] Research plan structured
- [x] Kill model defined
- [x] Kill constants sourced (Blueprint for Far-UVC 2025)
- [x] LED baseline sourced (FBH Berlin 2024)
- [x] Safety limit identified
- [x] Q1 simulation: dose thresholds and dwell time landscape
- [x] Q2/Q3 simulation: N_required feasibility maps and operating window
- [x] Distance sensitivity (inverse square law)
- [x] Key results written up
- [x] Technology gap analysis: fig5 — ~47 mW/chip (4.3% EQE) needed for conservative k, 235× improvement on current SOTA
- [x] Results written up on project page (UVCGlasses/index.html)
- [x] Homepage feed entry added

---

## References

1. FBH Berlin — https://www.fbh-berlin.de/forschung/forschungsnews/origin-of-the-efficiency-drop-in-far-uvc-light-emitting-diodes
2. Blueprint for Far-UVC v1.0, Blueprint Biosecurity (2025) — DOI: 10.64046/5j7b3nac
3. Buonanno et al. (2020) — HCoV inactivation constants, aerosol
4. Lu et al. (2024, 2025) — wavelength-specific k values, aerosolised pathogens
5. Kitagawa Presentation (2023) — SARS-CoV-2 aerosol susceptibility
