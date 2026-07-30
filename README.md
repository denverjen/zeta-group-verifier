# zeta-group-verifier

[![HAL](https://img.shields.io/badge/HAL-hal--05707491-blue)](https://hal.science/hal-05707491)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**An algebraic reduction of the Riemann Hypothesis to a word problem in a finitely presented group, with a Turing-machine compiler and abelianization verifier.**

---

## 🧠 What is this?

The Riemann Hypothesis (RH) asserts that all non-trivial zeros of the Riemann zeta function ζ(s) lie on the critical line Re(s) = 1/2.

This project does **not** attempt to prove RH with traditional analytic number theory. Instead, it takes a completely different path:

1. **Encode** the search for a counterexample to RH into a Turing machine.
2. **Compile** that Turing machine into a finitely presented group `G` using the classical Boone–Novikov construction.
3. **Reduce** the truth of RH to a single algebraic question:

