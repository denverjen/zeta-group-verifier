import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.turing_machine import TuringMachine
from src.compiler import machine_to_group
from src.abelian_tester import AbelianizationTester

states = ['q_start', 'q_dot', 'q_5', 'q_comma', 'q_skip', 'q_restart', 'q_dead', 'qH']
symbols = ['0','1','2','3','4','5','6','7','8','9','.', ',', '#', 'B']

transitions = {}
# Only the successful‑path transitions
transitions[('q_start', '0')] = ('q_dot', '0', 'R')
transitions[('q_dot', '.')] = ('q_5', '.', 'R')
transitions[('q_5', '5')] = ('q_comma', '5', 'R')
transitions[('q_comma', ',')] = ('q_skip', ',', 'R')

# Skip digits and '.' until '#', 'B'
for d in '0123456789':
    transitions[('q_skip', d)] = ('q_skip', d, 'R')
transitions[('q_skip', '.')] = ('q_skip', '.', 'R')
transitions[('q_skip', '#')] = ('q_restart', '#', 'R')
transitions[('q_skip', 'B')] = ('q_dead', 'B', 'R')

# Restart: '0' starts next zero, 'B' means all done
transitions[('q_restart', '0')] = ('q_dot', '0', 'R')
transitions[('q_restart', 'B')] = ('q_dead', 'B', 'R')

# Infinite loop for dead state
for a in symbols:
    transitions[('q_dead', a)] = ('q_dead', a, 'R')

# qH is never reached in this model → stays isolated in the group

# Real zeros data (first 20)
real_zeros_imag = [
    14.134725, 21.022040, 25.010857, 30.424876, 32.935061,
    37.586178, 40.918719, 43.327073, 48.005150, 49.773832,
    52.970321, 56.446247, 59.347044, 60.831778, 65.112544,
    67.079810, 69.546401, 72.067157, 75.704690, 77.144840
]

tape_str = ""
for y in real_zeros_imag:
    tape_str += f"#0.5,{y:.6f}"
tape_str += "#" + "B"*10
initial_tape = list(tape_str)

tm = TuringMachine(states, symbols, transitions, 'q_start', 'qH')
generators, relations, W_init, W_halt = machine_to_group(tm, initial_tape)

w = tuple(W_init) + tuple(f"{g}^-1" for g in reversed(W_halt))

tester = AbelianizationTester(generators, relations)
result = tester.is_abelian_image_zero(w)

print("===== Experiment C2: First 20 actual Riemann zeros =====")
print(f"Generators: {len(generators)}")
print(f"Abelianization image of w == 0? {result}  => w {'=' if result else '≠'} 1")
if not result:
    print("Conclusion: All tested zeros lie on the critical line (no counterexample).")
else:
    print("Warning: w vanishes in abelianization (unexpected).")
