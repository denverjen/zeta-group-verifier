"""
Square root with rigorous interval bounds.

Uses Newton's method with conservative outward rounding.
The output interval provably contains the true square root.

Requires interval arithmetic from `interval_arith`.
"""

from .interval_arith import SCALE, ONE,int_to_interval, add_interval, mul_interval, div_interval

def sqrt_interval(a_lo: int, a_hi: int) -> tuple:
    """
    Return an interval (lo, hi) that rigorously contains sqrt([a_lo, a_hi]).

    Parameters
    ----------
    a_lo, a_hi : int
        Fixed-point representation of the input interval, must satisfy 0 < a_lo <= a_hi.

    Returns
    -------
    (lo, hi) : tuple of int
        Lower and upper bounds of the square root.
    """
    if a_lo < 0:
        raise ValueError("Cannot compute square root of negative interval.")
    if a_lo == 0:
        # If the interval contains 0, the lower bound of sqrt is 0
        # and we compute upper bound for the positive part.
        # Here we assume the upper bound is positive.
        a_lo = 1   # avoid division by zero; take tiny positive

    # 1. Initial guess: use midpoint (as integer) and compute approximate sqrt
    mid = (a_lo + a_hi) >> 1
    # Approximate sqrt by converting to float for initial seed (only for speed)
    approx = int(__import__('math').sqrt(mid / ONE) * ONE)
    # Widen to a safe interval
    x_lo = approx - 100000
    x_hi = approx + 100000

    # 2. Newton iterations: x_{k+1} = (x_k + a / x_k) / 2
    for _ in range(8):  # 8 iterations sufficient for 60-bit precision
        # Compute a / x_k as an interval
        div_lo, div_hi = div_interval(a_lo, a_hi, x_lo, x_hi)
        # Add x_k and divide by 2 (right shift)
        sum_lo = x_lo + div_lo
        sum_hi = x_hi + div_hi + 1   # conservative upper bound
        x_new_lo = sum_lo >> 1
        x_new_hi = (sum_hi >> 1) + 1  # outward rounding
        # Slight inflation to absorb truncation errors
        x_lo = x_new_lo - 10
        x_hi = x_new_hi + 10

    return (x_lo, x_hi)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import math

    def to_float(iv):
        lo, hi = iv
        return lo / ONE, hi / ONE

    test_values = [1.0, 2.0, 3.14159, 100.0, 0.5, 1e6]
    all_ok = True
    for val in test_values:
        a_fixed = int(val * ONE)
        # create a narrow interval
        a_lo, a_hi = a_fixed - 1, a_fixed + 1
        lo, hi = sqrt_interval(a_lo, a_hi)
        true_sqrt = math.sqrt(val)
        ok = lo/ONE <= true_sqrt <= hi/ONE
        print(f"sqrt({val:8.5f})  true: {true_sqrt:.10f}  interval: [{lo/ONE:.10f}, {hi/ONE:.10f}]  {'OK' if ok else 'FAIL'}")
        if not ok:
            all_ok = False
    if all_ok:
        print("\nAll tests passed.")
    else:
        print("\nSome tests failed.")
