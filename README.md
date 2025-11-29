# FGOC: Focal-Geometry and Curvature Classifier  
A deterministic, <1 ms/arc classifier for LSST DIASource-level short-arc geometry and curvature diagnostics.

FGOC provides an ultra-lightweight geometric–curvature analysis designed for early identification of dynamically unusual DIASource tracklets during LSST Prompt Processing.  
The module runs directly on short-arc RA/DEC/MJD data, performs no orbit fitting, introduces no side effects, and requires zero modifications to existing AP/MOPS code paths.

FGOC is designed to complement existing LSST pipelines by supplying a deterministic, fast, fully reversible diagnostic layer for early anomaly detection and shadow-mode evaluation of astrometric stability.

---

##  Features

- **Deterministic** — No orbit fitting, no stochastic sampling, no optimization.  
- **Ultra-fast** — <1 ms per short arc.  
- **Non-invasive** — Reads only DIASource RA/DEC/MJD.  
- **Reversible and isolated** — Safe for shadow-mode execution.  
- **Pipeline-compatible** — Designed to sit before or alongside the MOPS Pre-Linker.  
- **Geometry-driven outputs**:  
  - `fgoc_flag` — Boolean anomaly indicator  
  - `fgoc_score` — Normalized anomaly score  
  - `focal_axis` — Estimated great-circle axis  
  - `curvature_sign` — +1 or –1  

---

## Installation

FGOC depends only on NumPy.

```bash
pip install numpy


Quick Start
from fgoc import fgoc

ra  = [10.0, 10.002, 10.004]
dec = [20.0, 20.001, 20.002]
mjd = [60000.0, 60000.01, 60000.02]

flag, score, axis, sign = fgoc(ra, dec, mjd)

print("FGOC flag:", flag)
print("FGOC score:", score)
print("Axis:", axis)
print("Curvature sign:", sign)


Typical runtime:

0.3–0.8 ms per arc

Method Overview

FGOC operates entirely in spherical focal-plane geometry:

1. RA/DEC → unit vectors

Standard spherical→Cartesian conversion.

2. Segment vectors

Directional tangent estimates.

3. Great-circle axis estimation

Summed cross-products give a stable normal vector.

4. Angular residuals

Deviation from inertial motion.

5. Curvature sign and magnitude

Using triple products and second-difference operators.

6. Combined anomaly score

Deterministic; no iteration.

Outputs
Output	Description
fgoc_flag	Boolean anomaly indicator
fgoc_score	Combined geometry–curvature score
focal_axis	Estimated great-circle axis
curvature_sign	+1 or –1
LSST Integration Notes

FGOC is designed specifically for LSST Prompt Processing and short-arc diagnostics.

✔ Integration point
DIASource  →  FGOC  →  Pre-Linker  →  MOPS

✔ Perfect for shadow-mode

FGOC requires no schema modification and performs no fitting, making it suitable for:

commissioning tests

astrometric stability diagnostics

AOS closed-loop behavior evaluation

early anomaly detection

pre-linking prioritization

✔ No impact on existing LSST/AP/MOPS logic

FGOC does not modify:

DIASource tables

Pre-linker heuristics

Alert Production rules

orbit fitting routines

🧪 Benchmark Performance
Arc length	Runtime	Notes
2 detections	~0.20 ms	minimum geometry
3 detections	0.30–0.50 ms	full curvature metrics
4–5 detections	0.60–0.80 ms	highly stable

FGOC remains robust under realistic astrometric noise.

Use Cases
1. Early ISO identification

Detects non-Keplerian curvature quickly.

2. Anomalous NEO motion

Flags unusual non-sidereal patterns.

3. Astrometric diagnostics

Sensitive to subtle RA/DEC systematics (useful for AOS closed-loop stability).

4. Pre-linking prioritization

Use fgoc_score to weight short arcs.

Repository Structure
fgoc/
 ├── fgoc.py
 ├── README.md
 ├── LICENSE
 └── .gitignore

Citation

Until ASCL assigns a permanent ID:

Lâu Thiat-uí, FGOC: Focal-Geometry and Curvature classifier, ASCL (submitted 2025).


After assignment:

Lâu Thiat-uí 2025, FGOC, ascl:25xx.xxx

Contact
Lâu Thiat-uí  
a8864666@gmail.com
