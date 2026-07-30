"""
Natural logarithm with rigorous interval bounds.

Uses a 12-term minimax polynomial for ln(1+x) on [0,1),
together with range reduction n = 2^p * m (m ∈ [1,2))
and a conservative truncation error bound.

All arithmetic is performed with fixed-point integers (scale = 60)
via interval_arith.
"""

from .interval_arith import SCALE, ONE,int_to_interval, add_interval, mul_interval 

# Constants ------------------------------------------------------------------

# ln(2) as an interval
LN2_LO = int(0.6931471805599453 * ONE)
LN2_HI = LN2_LO + 1

# 12-term minimax coefficients for ln(1+x), 0 ≤ x < 1
# ln(1+x) ≈ x * (c0 + c1*x + c2*x^2 + ... + c11*x^11)
# The coefficients are scaled by 2^60.
COEFF = [
    int(1.0 * ONE),                          # c0  =  1
    int(-0.5 * ONE),                         # c1  = -1/2
    int(0.3333333333333333 * ONE),           # c2  =  1/3
    int(-0.25 * ONE),                        # c3  = -1/4
    int(0.2 * ONE),                          # c4  =  1/5
    int(-0.1666666666666667 * ONE),          # c5  = -1/6
    int(0.14285714285714285 * ONE),          # c6  =  1/7
    int(-0.125 * ONE),                       # c7  = -1/8
    int(0.1111111111111111 * ONE),           # c8  =  1/9
    int(-0.1 * ONE),                         # c9  = -1/10
    int(0.0909090909090909 * ONE),           # c10 =  1/11
    int(-0.08333333333333333 * ONE),         # c11 = -1/12
]

# Truncation error bound: |R| ≤ x^13 / 13.
# Since 0 ≤ x < 1, the maximum error is 1/13 ≈ 0.076923.
TRUNC_ERROR = int(0.07692307692 * ONE)


# Core function --------------------------------------------------------------

def log_interval(n: int) -> tuple:
    """
    Return an interval (lo, hi) that rigorously contains ln(n).

    Parameters
    ----------
    n : int
        A positive integer (ordinary integer, not scaled).

    Returns
    -------
    (lo, hi) : tuple of int
        Lower and upper bounds of ln(n) as scaled integers.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")

    # 1. Range reduction: n = 2^p * m, where m ∈ [1, 2)
    m = n << SCALE          # m as a scaled integer (initially = n * 2^60)
    p = 0
    while m >= (2 << SCALE):
        m >>= 1
        p += 1
    while m < ONE:
        m <<= 1
        p -= 1
    # Now m ∈ [ONE, 2*ONE), i.e. true value in [1, 2)
    x_lo = m - ONE          # x = m/ONE - 1, in [0, 1)
    x_hi = x_lo + 1         # interval width = 2^{-60}

    # 2. Evaluate polynomial Q(x) = c0 + x*(c1 + x*(c2 + ... + x*c11)...)
    #    using Horner's method.
    y_lo, y_hi = int_to_interval(COEFF[-1])   # c11
    for c in reversed(COEFF[:-1]):            # from c10 down to c0
        y_lo, y_hi = mul_interval(y_lo, y_hi, x_lo, x_hi)
        y_lo, y_hi = add_interval(y_lo, y_hi, c, c)

    # Multiply by x to obtain ln(1+x)
    y_lo, y_hi = mul_interval(y_lo, y_hi, x_lo, x_hi)

    # 3. Add truncation error bound (conservative expansion)
    y_lo -= TRUNC_ERROR
    y_hi += TRUNC_ERROR

    # 4. Add p * ln(2)
    p_lo, p_hi = int_to_interval(p << SCALE)       # p as scaled integer
    term_lo, term_hi = mul_interval(p_lo, p_hi, LN2_LO, LN2_HI)
    result_lo, result_hi = add_interval(y_lo, y_hi, term_lo, term_hi)

    return (result_lo, result_hi)


# Self-test (only executed when run as main) ---------------------------------
if __name__ == "__main__":
    import math

    def to_float(interval):
        lo, hi = interval
        return lo / ONE, hi / ONE

    test_values = [1, 2, 3, 10, 100, 1000]
    all_pass = True
    for n in test_values:
        lo, hi = log_interval(n)
        true_val = math.log(n)
        ok = lo / ONE <= true_val <= hi / ONE
        print(f"ln({n:4d})  true: {true_val:.10f}  interval: [{lo/ONE:.10f}, {hi/ONE:.10f}]  {'OK' if ok else 'FAIL'}")
        if not ok:
            all_pass = False
    if all_pass:
        print("\nAll tests passed.")
    else:
        print("\nSome tests failed.")
