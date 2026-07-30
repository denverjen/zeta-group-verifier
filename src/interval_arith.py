"""
Fixed-point interval arithmetic with conservative outward rounding.
All real numbers are represented as scaled integers: x ≈ m * 2^{-60}.

An interval [a, b] is stored as a tuple (lo, hi) of two integers.
All operations guarantee that the true mathematical result is contained
in the returned interval.
"""

SCALE = 60
ONE = 1 << SCALE


def int_to_interval(m: int) -> tuple:
    """Convert an integer m (representing m * 2^{-60}) to a point interval."""
    return (m, m)


def add_interval(a_lo: int, a_hi: int, b_lo: int, b_hi: int) -> tuple:
    """
    Return [a_lo, a_hi] + [b_lo, b_hi] with conservative rounding.
    Lower bound: truncated sum (automatic floor for positive ints, but works
    correctly for signed integers as Python ints have arbitrary precision).
    Upper bound: sum + 1 to absorb rounding errors.
    """
    lo = a_lo + b_lo
    hi = a_hi + b_hi + 1
    return (lo, hi)


def sub_interval(a_lo: int, a_hi: int, b_lo: int, b_hi: int) -> tuple:
    """
    Return [a_lo, a_hi] - [b_lo, b_hi] with conservative rounding.
    """
    lo = a_lo - b_hi
    hi = a_hi - b_lo + 1
    return (lo, hi)


def mul_interval(a_lo: int, a_hi: int, b_lo: int, b_hi: int) -> tuple:
    """
    Return [a_lo, a_hi] * [b_lo, b_hi] with conservative rounding.
    Computes all four products of endpoints and takes min/max.
    """
    p1 = (a_lo * b_lo) >> SCALE
    p2 = (a_lo * b_hi) >> SCALE
    p3 = (a_hi * b_lo) >> SCALE
    p4 = (a_hi * b_hi) >> SCALE
    lo = min(p1, p2, p3, p4)
    hi = max(p1, p2, p3, p4) + 1
    return (lo, hi)


def div_interval(a_lo: int, a_hi: int, b_lo: int, b_hi: int) -> tuple:
    """
    Return [a_lo, a_hi] / [b_lo, b_hi] with conservative rounding.
    Assumes 0 < b_lo <= b_hi (denominator interval is strictly positive).
    """
    if b_lo <= 0:
        raise ValueError("Denominator interval must be strictly positive.")
    lo = (a_lo << SCALE) // b_hi   # a_lo / b_hi, rounded down
    hi = (a_hi << SCALE) // b_lo + 1  # a_hi / b_lo, rounded up
    return (lo, hi)


def contains(interval: tuple, value: float) -> bool:
    """
    Check if the true real value is contained in the given interval.
    Utility for testing.
    """
    lo, hi = interval
    return lo / ONE <= value <= hi / ONE


def interval_to_float(interval: tuple) -> tuple:
    """Convert interval to floating point representation for display."""
    lo, hi = interval
    return (lo / ONE, hi / ONE)
