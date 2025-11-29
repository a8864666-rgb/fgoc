import numpy as np

def spherical_to_unit(ra_deg, dec_deg):
    """Convert RA/DEC in degrees to a 3D unit vector."""
    ra = np.radians(ra_deg)
    dec = np.radians(dec_deg)
    x = np.cos(dec) * np.cos(ra)
    y = np.cos(dec) * np.sin(ra)
    z = np.sin(dec)
    return np.array([x, y, z])


def fgoc(ra_list, dec_list, mjd_list, alpha=8.0, beta=4.0, threshold=0.25):
    """
    FGOC: Focal-Geometry and Curvature classifier for short-arc astrometry.

    Inputs:
        ra_list   : list of RA values in degrees
        dec_list  : list of DEC values in degrees
        mjd_list  : list of MJD timestamps

    Returns:
        fgoc_flag      : Boolean anomaly flag
        fgoc_score     : Combined geometry–curvature anomaly score
        focal_axis     : 3D unit vector (best great-circle axis)
        curvature_sign : +1 or -1
    """

    # Convert to unit vectors
    X = [spherical_to_unit(ra, dec) for ra, dec in zip(ra_list, dec_list)]
    X = np.array(X)
    N = len(X)

    if N < 2:
        raise ValueError("FGOC requires at least 2 detections.")

    # Segment vectors
    D = X[1:] - X[:-1]  # d_i = x_{i+1} - x_i

    # Estimate great-circle axis
    cross_terms = np.array([np.cross(X[i], X[i+1]) for i in range(N - 1)])
    n = np.sum(cross_terms, axis=0)
    norm_n = np.linalg.norm(n)
    if norm_n == 0:
        focal_axis = np.array([0, 0, 0])
    else:
        focal_axis = n / norm_n

    # Angular residuals from great circle
    r_i = np.abs(np.dot(X, focal_axis))
    r_max = np.max(r_i)

    # Curvature sign and magnitude
    curvature_signs = []
    k_vals = []

    if N >= 3:
        for i in range(1, N - 1):
            d_prev = D[i - 1]
            d_curr = D[i]
            triple = np.dot(np.cross(d_prev, d_curr), X[i])

            if triple > 0:
                curvature_signs.append(+1)
            else:
                curvature_signs.append(-1)

            # Second difference curvature magnitude
            k_vals.append(np.linalg.norm(X[i + 1] - 2 * X[i] + X[i - 1]))
    else:
        curvature_signs = [+1]
        k_vals = [0.0]

    # Majority sign
    curvature_sign = +1 if sum(curvature_signs) >= 0 else -1

    # Mean curvature
    k = np.mean(k_vals)

    # Final FGOC score
    fgoc_score = 1 - np.exp(-alpha * r_max - beta * k)

    # Boolean anomaly flag
    fgoc_flag = fgoc_score > threshold

    return fgoc_flag, fgoc_score, focal_axis, curvature_sign


# Example usage
if __name__ == "__main__":
    ra = [10.0, 10.002, 10.004]
    dec = [20.0, 20.001, 20.002]
    mjd = [60000.0, 60000.01, 60000.02]

    result = fgoc(ra, dec, mjd)
    print("FGOC result:", result)
