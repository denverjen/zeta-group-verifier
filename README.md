# zeta-group-verifier
 A Group-Theoretic Approach to the Riemann Hypothesis: Encoding Zero Verification as a Word Problem

# Zeta Group Verifier

A pure algebraic approach to verify the Riemann Hypothesis using combinatorial group theory.
We encode zero‑checking Turing machines into finitely presented groups and decide the word problem via abelianization (and deeper invariants).

## 🧠 Core Idea
- Design a Turing machine that halts iff a counterexample to RH is found.
- Compile the machine into a group presentation and a distinguished word \(w\).
- If \(w \neq 1\) in the group, the machine never halts → RH holds (for the checked zeros).

## ⚙️ Structure
- `src/interval_arith.py` – Fixed‑point interval arithmetic with rigorous rounding.
- `src/log_interval.py` – Natural logarithm via minimax polynomial + truncation error.
- `src/cordic.py` – CORDIC sine/cosine with conservative interval output.
- `src/sqrt_interval.py` – Newton square root with interval bounds.
- `src/turing_machine.py` – A simple Turing machine simulator (states, symbols, transitions).
- `src/compiler.py` – Converts a Turing machine into a group presentation and word.
- `src/abelian_tester.py` – Decides whether \(w=1\) using abelianization (rank test).
- `experiments/` – Reproduces all experiments from the paper (A, C2, E2, F, ...).

## 🚀 Quick Start
```bash
pip install -r requirements.txt
python experiments/experiment_F.py
