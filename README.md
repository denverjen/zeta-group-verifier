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


RH is true ⇔ the Turing machine never halts ⇔ w ≠ 1 in G


where `w` is a specific word in the group `G`.

This is a **constructive reduction**: the group `G` and the word `w` can be explicitly written down.

---

## 📦 What's inside?

| Directory/File | Description |
|----------------|-------------|
| `src/interval_arith.py` | Fixed-point interval arithmetic with conservative outward rounding |
| `src/log_interval.py` | Natural logarithm module (12-term minimax polynomial + error bound) |
| `src/cordic.py` | CORDIC sine/cosine with interval output |
| `src/sqrt_interval.py` | Square root via Newton's method with interval bounds |
| `src/turing_machine.py` | A simple Turing machine simulator |
| `src/compiler.py` | Turing machine → finitely presented group compiler |
| `src/abelian_tester.py` | Abelianization rank test (decides if `w = 1` in the abelian quotient) |
| `experiments/` | Reproducible scripts for all experiments in the paper |
| `tests/` | Unit tests for arithmetic modules |
| `docs/` | Implementation blueprint and references |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or later
- NumPy

### Installation
```bash
git clone https://github.com/denverjen/zeta-group-verifier.git
cd zeta-group-verifier
pip install -r requirements.txt
