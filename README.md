
# FGOC: Focal-Geometry and Curvature Classifier

A deterministic, <1 ms/arc classifier for LSST DIASource-level short-arc geometry and curvature diagnostics.

FGOC provides an ultra-lightweight geometric–curvature analysis designed for early identification of dynamically unusual DIASource tracklets during LSST Prompt Processing.  
The module runs directly on short-arc RA/DEC/MJD data, performs no orbit fitting, introduces no side effects, and requires zero modifications to existing AP/MOPS code paths.

FGOC is designed to complement existing LSST pipelines by supplying a deterministic, fast, fully reversible diagnostic layer for early anomaly detection and shadow-mode evaluation of astrometric stability.

---

## Features

- **Deterministic** — No orbit fitting, no stochastic sampling, no optimization.  
- **Ultra-fast** — <1 ms per short arc.  
- **Non-invasive** — Reads only DIASource RA/DEC/MJD.  
- **Reversible and isolated** — Safe for shadow-mode execution.  
- **Pipeline-compatible** — Designed to sit before or alongside the MOPS Pre-Linker.

### Geometry-driven outputs

- `fgoc_flag` — Boolean anomaly indicator  
- `fgoc_score` — Normalized anomaly score  
- `focal_axis` — Estimated great-circle axis  
- `curvature_sign` — +1 or −1  

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
Typical runtime: 0.3–0.8 ms per arc


Method Overview

FGOC operates entirely in spherical focal-plane geometry:

RA/DEC → unit vectors

Segment vectors

Great-circle axis estimation

Angular residuals

Curvature sign & magnitude

Combined anomaly score (deterministic; no iteration)


Outputs
| Output           | Description                      |
| ---------------- | -------------------------------- |
| `fgoc_flag`      | Boolean anomaly indicator        |
| `fgoc_score`     | Geometry–curvature anomaly score |
| `focal_axis`     | Estimated great-circle axis      |
| `curvature_sign` | +1 or −1                         |


LSST Integration Notes

FGOC is designed specifically for LSST Prompt Processing and short-arc diagnostics.

Integration point
DIASource → FGOC → Pre-Linker → MOPS


Perfect for shadow-mode

Useful for:

commissioning tests

astrometric stability diagnostics

AOS closed-loop behavior evaluation

early anomaly detection

pre-linking prioritization

No impact on existing LSST/AP/MOPS logic

FGOC does NOT modify:

DIASource tables

Pre-Linker heuristics

Alert Production rules

orbit fitting routines


Benchmark Performance
| Arc length     | Runtime      | Notes            |
| -------------- | ------------ | ---------------- |
| 2 detections   | ~0.20 ms     | minimum geometry |
| 3 detections   | 0.30–0.50 ms | full curvature   |
| 4–5 detections | 0.60–0.80 ms | highly stable    |


Use Cases

Early ISO identification

Anomalous NEO motion detection

Astrometric diagnostics (RA/DEC systematics, AOS stability)

Pre-linking prioritization for MOPS

Repository Structure
fgoc/
 ├── fgoc.py
 ├── README.md
 ├── LICENSE
 └── .gitignore

def fgoc(ra, dec, mjd):
    """
    Parameters
    ----------
    ra : list[float]
        Right Ascension in degrees.
    dec : list[float]
        Declination in degrees.
    mjd : list[float]
        Observation time in MJD.

    Returns
    -------
    fgoc_flag : bool
    fgoc_score : float
    focal_axis : np.ndarray
    curvature_sign : int  (+1 or -1)
    """


Citation

Until ASCL assigns a permanent ID, please cite FGOC as:

Lâu Thiat-uí (2025),
FGOC: Focal-Geometry and Curvature Classifier for Early Identification of Non-Keplerian and Interstellar Trajectories,
Astrophysics Source Code Library (submitted).

GitHub URL: https://github.com/a8864666-rgb/fgoc

License: MIT
Version: v1.0

BibTeX

@misc{Lau2025FGOC,
  author       = {Lâu, Thiat-uí},
  title        = {FGOC: Focal-Geometry and Curvature Classifier for Early Identification of Non-Keplerian and Interstellar Trajectories},
  year         = {2025},
  howpublished = {Astrophysics Source Code Library, submitted},
  url          = {https://github.com/a8864666-rgb/fgoc},
  note         = {Version 1.0, MIT License},
}

Contact

Lâu Thiat-uí
a8864666@gmail.com




