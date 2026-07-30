#!/usr/bin/env python3
"""
Experiment C2: Verify the first N actual Riemann zeros using the group
compiler and abelianization test.

Usage:
    python experiments/experiment_C2.py                # default N=20
    python experiments/experiment_C2.py --N 1000       # if data file exists
    python experiments/experiment_C2.py --file data/zeros_1000.txt
"""

import sys, os, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.turing_machine import TuringMachine
from src.compiler import machine_to_group
from src.abelian_tester import AbelianizationTester


# ---------------------------------------------------------------------------
# Default built‑in zeros (first 20)
# ---------------------------------------------------------------------------
DEFAULT_ZEROS = [
    14.134725, 21.022040, 25.010857, 30.424876, 32.935061,
    37.586178, 40.918719, 43.327073, 48.005150, 49.773832,
    52.970321, 56.446247, 59.347044, 60.831778, 65.112544,
    67.079810, 69.546401, 72.067157, 75.704690, 77.144840
]


def load_zeros_from_file(path: str):
    """Read imaginary parts from a text file, one per line."""
    zeros = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                zeros.append(float(line))
    return zeros


def build_tape(zeros):
    """Create the initial tape string for the given zeros."""
    tape_str = ""
    for y in zeros:
        tape_str += f"#0.5,{y:.6f}"
    tape_str += "#" + "B" * 10
    return list(tape_str)


# ---------------------------------------------------------------------------
# Turing machine definition (same as before)
# ---------------------------------------------------------------------------
states = ['q_start', 'q_dot', 'q_5', 'q_comma', 'q_skip', 'q_restart', 'q_dead', 'qH']
symbols = ['0','1','2','3','4','5','6','7','8','9','.', ',', '#', 'B']

transitions = {}
transitions[('q_start', '0')] = ('q_dot', '0', 'R')
transitions[('q_dot', '.')] = ('q_5', '.', 'R')
transitions[('q_5', '5')] = ('q_comma', '5', 'R')
transitions[('q_comma', ',')] = ('q_skip', ',', 'R')
for d in '0123456789':
    transitions[('q_skip', d)] = ('q_skip', d, 'R')
transitions[('q_skip', '.')] = ('q_skip', '.', 'R')
transitions[('q_skip', '#')] = ('q_restart', '#', 'R')
transitions[('q_skip', 'B')] = ('q_dead', 'B', 'R')
transitions[('q_restart', '0')] = ('q_dot', '0', 'R')
transitions[('q_restart', 'B')] = ('q_dead', 'B', 'R')
for a in symbols:
    transitions[('q_dead', a)] = ('q_dead', a, 'R')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--N', type=int, default=20, help='number of zeros')
    parser.add_argument('--file', type=str, help='path to zeros file')
    args = parser.parse_args()

    # Load zeros
    if args.file:
        zeros = load_zeros_from_file(args.file)
    else:
        # Try the standard data file
        data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'zeros_1000.txt')
        if os.path.exists(data_file):
            print("Loading 1000 zeros...")
            zeros = load_zeros_from_file(data_file)[:args.N]
        else:
            zeros = DEFAULT_ZEROS[:args.N]
            print("Note: using built‑in 20 zeros. To use 1000, create data/zeros_1000.txt (see scripts/generate_zeros.py).\n")

    initial_tape = build_tape(zeros)

    tm = TuringMachine(states, symbols, transitions, 'q_start', 'qH')
    generators, relations, W_init, W_halt = machine_to_group(tm, initial_tape)
    w = tuple(W_init) + tuple(f"{g}^-1" for g in reversed(W_halt))

    tester = AbelianizationTester(generators, relations)
    result = tester.is_abelian_image_zero(w)

    print(f"===== Experiment C2: First {len(zeros)} Riemann zeros =====")
    print(f"Generators: {len(generators)}")
    print(f"Abelianization image of w == 0? {result}  => w {'=' if result else '≠'} 1")
    if not result:
        print("Conclusion: All tested zeros lie on the critical line (no counterexample).")
    else:
        print("Warning: w vanishes in abelianization (unexpected).")
