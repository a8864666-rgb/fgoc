
# FGOC: Focal-Geometry and Curvature Classifier

A deterministic, sub-millisecond classifier for LSST DIASource short-arc geometry and curvature diagnostics.

Overview

FGOC is an ultra-lightweight Python module for rapid, geometry-based analysis of short-arc astrometric detections.
It operates directly on RA/DEC/MJD triplets and provides early, deterministic diagnostics useful for LSST Prompt Processing pipelines.

The classifier performs no orbit fitting, uses no stochastic sampling, and introduces no changes to existing LSST AP or MOPS workflows.
It is suitable for shadow-mode testing, early anomaly flagging, and rapid triage of unusual astrometric motions.
---

## Key Features

Deterministic — No orbit fitting, no optimization, no randomization.
Ultra-fast — Typically 0.3–0.8 ms per arc.
Non-invasive — Reads only DIASource-level RA/DEC/MJD data.
Reversible & isolated — Safe for commissioning and shadow-mode execution.
Pipeline-compatible — Designed to sit before or alongside the LSST MOPS Pre-Linker.nker.

### Outputs

| Output           | Description                               |
| ---------------- | ----------------------------------------- |
| `fgoc_flag`      | Boolean indicator of geometric anomaly    |
| `fgoc_score`     | Normalized geometry–curvature score       |
| `focal_axis`     | Estimated great-circle axis (unit vector) |
| `curvature_sign` | Sign of local curvature (+1 or −1)        |

---

## Requirements

- Python >= 3.9
- NumPy >= 1.20


## Installation

pip install numpy
Clone this repository or copy fgoc.py into your project.

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

Typical runtime: 0.3–0.8 ms for arcs of 3–5 detections.


Method Summary

FGOC works entirely in spherical focal-plane geometry:

1. Convert RA/DEC to unit vectors  
2. Construct segment directions  
3. Estimate great-circle axis  
4. Compute angular residuals  
5. Determine curvature sign  
6. Produce normalized score  


No iteration, fitting, or dynamical modeling is used.


Outputs
| Output           | Description                      |
| ---------------- | -------------------------------- |
| `fgoc_flag`      | Boolean anomaly indicator        |
| `fgoc_score`     | Geometry–curvature anomaly score |
| `focal_axis`     | Estimated great-circle axis      |
| `curvature_sign` | +1 or −1                         |


LSST Integration Notes

FGOC is designed for:

Prompt Processing commissioning tests

Astrometric stability checks

Shadow-mode anomaly detection

Pre-linking prioritization

Early triage of unusual tracklets

Suggested placement:
DIASource → FGOC → Pre-Linker → MOPS
FGOC does not modify:

DIASource tables

Pre-Linker heuristics

Alert Production logic

Orbit fitting routines


Repository Structure
fgoc/
 ├── fgoc.py
 ├── README.md
 ├── LICENSE
 └── .gitignore


Citation
Please cite: Lâu Thiat-uí (2025), FGOC, Astrophysics Source Code Library, ascl:2512.003.


BibTeX:
@misc{Lau2025FGOC,
  author       = {Lâu, Thiat-uí},
  title        = {FGOC: Focal-Geometry and Curvature Classifier for Early Identification of Non-Keplerian and Interstellar Trajectories},
  year         = {2025},
  howpublished = {Astrophysics Source Code Library, submitted},
  url          = {https://github.com/a8864666-rgb/fgoc},
  note         = {Version 1.0, MIT License},
}


After approval:
Lâu Thiat-uí, 2025, FGOC, ascl:2512.003


### Rubin / LSST Usage Statement

FGOC is intentionally designed as an **external, non-invasive, LSST-compatible module**.  
It does **not** modify any Rubin/LSST data products, tables, schemas, or pipeline stages.  
Instead, FGOC operates strictly as an **advisory geometric–curvature classifier** that can be:

- run beneath **DIASource**,
- consumed by **Prompt Processing (AP) notebooks**,  
- optionally used by **MOPS Pre-Linker** as a soft-priority signal,
- ignored without side effects by any LSST subsystem.

FGOC **does not overwrite** any LSST fields,  
**does not require** any changes to AP/MOPS logic,  
and **does not depend** on Rubin-internal data models or proprietary software.

This design ensures:

- full compatibility with LSST Data Management (DM),
- zero operational risk to AP or Alert Production,
- zero impact on MOPS orbit linking,
- easy evaluation within the Rubin Science Platform (RSP),
- and straightforward future integration if LSST chooses to adopt FGOC.

> **Rubin Observatory and the LSST Project are granted  
> perpetual, unrestricted MIT-licensed rights to use, modify, integrate, or ignore FGOC at any time.**




### FGOC Patent Non-Assertion and MIT License Assurance

**FGOC (Focal-Geometry and Curvature Classifier)** — including the core algorithm, numerical heuristics, scoring logic, and the implementation published in this repository — is released under the **MIT License**, which grants Rubin Observatory, LSST Data Management, and all LSST Science Collaborations unrestricted and perpetual rights to use, modify, distribute, integrate, and deploy the software.

The author provides the following additional **Patent Non-Assertion Guarantee**:

> “Regardless of the existence or future outcome of any patent application related to geometric–curvature classification methods, the author hereby irrevocably agrees not to assert any patent claims against Rubin Observatory, the LSST Project, or any Rubin/LSST-affiliated institutions for the use, implementation, modification, evaluation, or deployment of FGOC as released under the MIT License.”


---

### License

MIT License  
Copyright © 2025 Lâu Thiat-uí

---

### Contact

Lâu Thiat-uí  
a8864666@gmail.com

---

### Patent Status

FGCC / FGOC — Patent Pending  
(*Patent pending does **not** restrict the MIT-licensed FGOC implementation nor the Non-Assertion guarantee above.*)
