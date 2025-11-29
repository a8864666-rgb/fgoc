# FGOC: Focal-Geometry and Curvature Classifier  
A deterministic, <1 ms/arc classifier for LSST DIASource-level short-arc geometry and curvature diagnostics.

FGOC provides an ultra-lightweight geometric–curvature analysis designed for early identification of dynamically unusual DIASource tracklets during LSST Prompt Processing.  
The module runs directly on short-arc RA/DEC/MJD data, performs no orbit fitting, introduces no side effects, and requires zero modifications to existing AP/MOPS code paths.

FGOC is designed to complement existing LSST pipelines by supplying a deterministic, fast, fully reversible diagnostic layer for early anomaly detection and shadow-mode evaluation of astrometric stability.

---

## 🚀 Features

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

## 🔧 Installation

FGOC depends only on NumPy.

```bash
pip install numpy

