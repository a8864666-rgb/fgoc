"""
FGOC Orbit-Fit Mode (Exact Eq.(4)(5)(6) Implementation)
-------------------------------------------------------
Primary SoftwareX contribution: deterministic focal-geometry diagnostics
computed from successive preliminary orbit-fit state vectors.

Implements:
- Appendix A (A.1-A.6): focal reconstruction from (r, v, mu)
- Eq.(4): Delta F_j(t_k) = F_{j,k} - F_{j,k-1}
- Eq.(5): FDR = 1/2 ( < ||ΔF1||/Δt > + < ||ΔF2||/Δt > )
- Eq.(6): FSBI = < | ||F1-F2|| - <||F1-F2||> | > + < || (F1+F2)/2 - <r_CM> || >
- Eq.(7): S = α1 FDR + α2 FSBI
- Eq.(8): P = 1 / (1 + exp(-(S-τ)))

Notes:
- No orbit fitting is performed here. Upstream OD solver supplies states.
- ⟨·⟩ is implemented as simple mean for maximal paper-code consistency.
"""

from __future__ import annotations
import numpy as np


# -------------------------
# Utility helpers
# -------------------------
def _norm(x: np.ndarray, eps: float = 1e-15) -> float:
    return float(np.linalg.norm(x) + eps)


def _unit(x: np.ndarray, eps: float = 1e-15) -> np.ndarray:
    n = np.linalg.norm(x)
    if n < eps:
        return np.zeros_like(x)
    return x / n


def _mean(values: np.ndarray) -> float:
    """Simple mean (paper-aligned)."""
    return float(np.mean(values))


def _vec_mean(vectors: np.ndarray) -> np.ndarray:
    """Vector simple mean."""
    return np.mean(vectors, axis=0)


# -------------------------
# Appendix A: focal reconstruction
# -------------------------
def focal_metrics_from_state(r: np.ndarray, v: np.ndarray, mu: float) -> dict:
    """
    Implementation-oriented focal reconstruction (Appendix A, A.1-A.6).

    Returns:
        dict: h, A, e_hat, e, a, r_cm, F1, F2
    """
    r = np.asarray(r, dtype=float)
    v = np.asarray(v, dtype=float)

    # (A.1) specific angular momentum
    h = np.cross(r, v)

    # (A.2) Laplace–Runge–Lenz vector
    A = np.cross(v, h) - mu * (r / _norm(r))

    # (A.3) eccentricity and unit direction
    e = _norm(A) / mu
    e_hat = _unit(A)

    # semi-major axis from vis-viva: 1/a = 2/r - v^2/mu
    rmag = _norm(r)
    v2 = float(np.dot(v, v))
    inv_a = (2.0 / rmag) - (v2 / mu)
    if abs(inv_a) < 1e-15:
        a = np.inf
    else:
        a = 1.0 / inv_a

    # (A.4) conic center
    if np.isfinite(a):
        r_cm = -a * e * e_hat
    else:
        r_cm = np.zeros(3)

    # (A.5)-(A.6) foci
    if np.isfinite(a):
        F1 = r_cm + a * e * e_hat
        F2 = r_cm - a * e * e_hat
    else:
        F1 = np.zeros(3)
        F2 = np.zeros(3)

    return {
        "h": h,
        "A": A,
        "e_hat": e_hat,
        "e": e,
        "a": a,
        "r_cm": r_cm,
        "F1": F1,
        "F2": F2,
    }


# -------------------------
# Eq.(4)(5)(6): FDR and FSBI
# -------------------------
def compute_fdr_fsbi(
    states: list[tuple[np.ndarray, np.ndarray]],
    mu: float,
    times: list[float] | None = None,
) -> dict:
    """
    Compute FDR and FSBI exactly per manuscript Eq.(4)(5)(6).

    Parameters
    ----------
    states : list of (r, v)
        Successive preliminary orbit-fit state vectors.
    mu : float
        Gravitational parameter in consistent units.
    times : optional list of float
        Epochs for each state. If None, assumes Δt = 1 between successive states.

    Returns
    -------
    dict including:
        FDR, FSBI,
        F1_series, F2_series, rCM_series,
        dF1_dt_series, dF2_dt_series,
        sep_series, sep_mean, rCM_mean,
        term_sep, term_cm
    """
    K = len(states)
    if K < 2:
        raise ValueError("Orbit-fit mode requires at least two successive state vectors.")

    if times is not None and len(times) != K:
        raise ValueError("If provided, 'times' must have the same length as 'states'.")

    metrics = [focal_metrics_from_state(r, v, mu) for (r, v) in states]

    F1 = np.array([m["F1"] for m in metrics], dtype=float)     # (K,3)
    F2 = np.array([m["F2"] for m in metrics], dtype=float)     # (K,3)
    rCM = np.array([m["r_cm"] for m in metrics], dtype=float)  # (K,3)

    # Eq.(4): ΔF_j(t_k) = F_{j,k} - F_{j,k-1}
    dF1 = np.diff(F1, axis=0)  # (K-1,3)
    dF2 = np.diff(F2, axis=0)  # (K-1,3)

    # Δt handling
    if times is None:
        dt = np.ones(K - 1, dtype=float)
    else:
        dt = np.diff(np.asarray(times, dtype=float))
        dt = np.where(np.abs(dt) < 1e-15, 1.0, dt)  # avoid division by zero

    # ||ΔF|| / Δt
    dF1_dt = np.linalg.norm(dF1, axis=1) / dt
    dF2_dt = np.linalg.norm(dF2, axis=1) / dt

    # Eq.(5): FDR
    FDR = 0.5 * (_mean(dF1_dt) + _mean(dF2_dt))

    # Eq.(6): FSBI components
    # separation series: ||F1 - F2||
    sep = np.linalg.norm(F1 - F2, axis=1)              # (K,)
    sep_mean = _mean(sep)

    # term 1: < | sep_k - <sep> | >
    term_sep = _mean(np.abs(sep - sep_mean))

    # term 2: < || (F1+F2)/2 - <rCM> || >
    rCM_mean = _vec_mean(rCM)
    mid = 0.5 * (F1 + F2)
    term_cm = _mean(np.linalg.norm(mid - rCM_mean, axis=1))

    FSBI = term_sep + term_cm

    return {
        "FDR": float(FDR),
        "FSBI": float(FSBI),
        "metrics": metrics,
        "F1_series": F1,
        "F2_series": F2,
        "rCM_series": rCM,
        "dF1_dt_series": dF1_dt,
        "dF2_dt_series": dF2_dt,
        "sep_series": sep,
        "sep_mean": float(sep_mean),
        "rCM_mean": rCM_mean,
        "term_sep": float(term_sep),
        "term_cm": float(term_cm),
        "times": None if times is None else list(times),
    }


# -------------------------
# Eq.(7)(8): score and probability
# -------------------------
def fgoc_orbitfit(
    states: list[tuple[np.ndarray, np.ndarray]],
    mu: float,
    times: list[float] | None = None,
    alpha1: float = 1.0,
    alpha2: float = 1.0,
    tau: float = 0.0,
    flag_threshold: float = 0.5,
) -> tuple[bool, float, float, dict]:
    """
    Primary orbit-fit FGOC API (paper-aligned).

    Returns:
        fgoc_flag : bool
        fgoc_score : float   (S)
        fgoc_prob : float    (P)
        diagnostics : dict   (FDR/FSBI and intermediate focal series)
    """
    diag = compute_fdr_fsbi(states=states, mu=mu, times=times)
    FDR = diag["FDR"]
    FSBI = diag["FSBI"]

    # Eq.(7)
    S = float(alpha1 * FDR + alpha2 * FSBI)

    # Eq.(8)
    P = float(1.0 / (1.0 + np.exp(-(S - tau))))

    flag = bool(P >= flag_threshold)

    diagnostics = dict(diag)
    diagnostics.update({
        "S": S,
        "P": P,
        "alpha1": alpha1,
        "alpha2": alpha2,
        "tau": tau,
        "flag_threshold": flag_threshold,
    })

    return flag, S, P, diagnostics
