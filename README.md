
# zeta-group-verifier

[![HAL](https://img.shields.io/badge/HAL-hal--05707491-blue)](https://hal.science/hal-05707491)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**An algebraic reduction of the Riemann Hypothesis to a word problem in a finitely presented group, with a Turing-machine compiler and abelianization verifier.**

## 🧠 What is this?

The Riemann Hypothesis (RH) asserts that all non-trivial zeros of the Riemann zeta function ζ(s) lie on the critical line Re(s) = 1/2.

This project does **not** attempt to prove RH with traditional analytic number theory. Instead, it takes a completely different path:

1. **Encode** the search for a counterexample to RH into a Turing machine.
2. **Compile** that Turing machine into a finitely presented group `G` using the classical Boone–Novikov construction.
3. **Reduce** the truth of RH to a single algebraic question:

---

## What is this?

The Riemann Hypothesis (RH) asserts that all non-trivial zeros of the Riemann zeta function ζ(s) lie on the critical line Re(s) = 1/2.

This project **reduces** RH to a purely algebraic problem:

1. Encode the search for a counterexample to RH into a Turing machine.
2. Compile that Turing machine into a finitely presented group `G` using the Boone–Novikov construction.
3. The truth of RH becomes a word problem:

```
RH is true  ⇔  the Turing machine never halts  ⇔  w ≠ 1 in G

where `w` is a specific word in the group `G`. This reduction is **constructive**: `G` and `w` can be explicitly written down.

---

## Project Structure

| Directory/File | Description |
|----------------|-------------|
| `src/interval_arith.py` | Fixed-point interval arithmetic (conservative outward rounding) |
| `src/log_interval.py` | Natural logarithm (12-term minimax polynomial + error bound) |
| `src/cordic.py` | CORDIC sine/cosine with interval output |
| `src/sqrt_interval.py` | Square root via Newton's method with interval bounds |
| `src/turing_machine.py` | Turing machine simulator |
| `src/compiler.py` | Turing machine → finitely presented group compiler |
| `src/abelian_tester.py` | Abelianization rank test (decides if `w = 1` in the abelian quotient) |
| `experiments/` | Reproducible scripts for all experiments in the paper |
| `tests/` | Unit tests for arithmetic modules |
| `docs/` | Implementation blueprint and references |

---

## Quick Start

### Prerequisites
- Python 3.8+
- NumPy

### Installation
```bash
git clone https://github.com/denverjen/zeta-group-verifier.git
cd zeta-group-verifier
pip install -r requirements.txt
```

### Run an experiment
```bash
python experiments/experiment_C2.py
```
Expected output:
```
===== Experiment C2: First 1000 actual Riemann zeros =====
Abelianization image of w == 0 ? False  => w ≠ 1
Conclusion: All 1000 zeros lie on the critical line (no counterexample).
```

---

## Experiments

| Experiment | Description | Generators | Result |
|------------|-------------|------------|--------|
| Micro NT/T | Halting vs. non-halting micro-machines | 5 | Correctly discriminated |
| C2 | First 1000 actual zeros (hard-coded tape) | 23 | `w ≠ 1` ✅ |
| D | Self-generating `"0.5"` loop | 15 | `w ≠ 1` ✅ |
| E1 | Counter + generate `#0.5` | 23 | `w ≠ 1` ✅ |
| E2 | Counter + fixed imaginary part | 45 | `w ≠ 1` ✅ |
| E3 | Counter + variable imaginary part (copy) | 24 | `w ≠ 1` ✅ |
| F | Asymptotic zero-generation formula | 23 | `w ≠ 1` ✅ |

All experiments confirm that the abelianization correctly detects non-halting behaviour.

---

## Reference

The full paper is available on HAL:

> **An Algebraic Reduction of the Riemann Hypothesis to a Word Problem in a Finitely Presented Group**  
> Jen Yau Cheong  
> HAL-ID: `hal-05707491`  
> [https://hal.science/hal-05707491](https://hal.science/hal-05707491)

Please cite the paper if you use this code.

---

## Contributing

Contributions are welcomed!

- Implement the full Riemann–Siegel sum in `src/riemann_siegel.py`
- Improve the compiler (reduce output size)
- Add deeper invariants (nilpotent quotients, finite quotients, matrix representations)
- Write tests and documentation

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit and push
4. Open a Pull Request

---

## License

MIT License. See `LICENSE` for details.

---

## Author

**Jen Yau Cheong**  
Email: denverjen95@gmail.com  
HAL: [hal-05707491](https://hal.science/hal-05707491)

---

> *"The compiler is the axe; the reduction is the tree. This project invites everyone to help cut it down."*
```
