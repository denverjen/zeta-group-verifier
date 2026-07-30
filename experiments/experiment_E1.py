# experiments/experiment_E1.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.turing_machine import TuringMachine
from src.compiler import machine_to_group
from src.abelian_tester import AbelianizationTester

states = ['q_init', 'q_gen', 'q_verify', 'q_clear', 'q_inc', 'q_loop', 'qH']
symbols = ['0', '.', '5', '#', '1', 'B']

transitions = {}
# Initial counter = '1'
transitions[('q_init', 'B')] = ('q_gen', '1', 'R')
# Generate "#0.5"
transitions[('q_gen', 'B')] = ('q_verify', '#', 'R')
transitions[('q_verify', '#')] = ('q_verify', '0', 'R')
transitions[('q_verify', '0')] = ('q_verify', '.', 'R')
transitions[('q_verify', '.')] = ('q_verify', '5', 'R')
transitions[('q_verify', '5')] = ('q_clear', 'B', 'R')
# Clear work area (just move right until B)
transitions[('q_clear', 'B')] = ('q_inc', 'B', 'R')
transitions[('q_clear', '#')] = ('q_clear', 'B', 'R')
transitions[('q_clear', '0')] = ('q_clear', 'B', 'R')
transitions[('q_clear', '.')] = ('q_clear', 'B', 'R')
transitions[('q_clear', '5')] = ('q_clear', 'B', 'R')
# Increment counter: add '1' at end
transitions[('q_inc', '1')] = ('q_inc', '1', 'R')
transitions[('q_inc', 'B')] = ('q_loop', '1', 'R')
# Loop back to generate
transitions[('q_loop', '1')] = ('q_gen', '1', 'R')

tm = TuringMachine(states, symbols, transitions, 'q_init', 'qH')
initial_tape = ['B', 'B']
generators, relations, W_init, W_halt = machine_to_group(tm, initial_tape)
w = tuple(W_init) + tuple(f"{g}^-1" for g in reversed(W_halt))

tester = AbelianizationTester(generators, relations)
result = tester.is_abelian_image_zero(w)
print("===== Experiment E1: Counter + generate #0.5 =====")
print(f"Generators: {len(generators)}")
print(f"Abelianization image of w == 0? {result}  => w {'=' if result else '≠'} 1")
if not result:
    print("Conclusion: Machine never halts (all generated zeros OK).")
else:
    print("Warning: w vanished.")
