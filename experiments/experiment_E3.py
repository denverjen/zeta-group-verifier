# experiments/experiment_E3.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.turing_machine import TuringMachine
from src.compiler import machine_to_group
from src.abelian_tester import AbelianizationTester

states = ['q_init', 'q_gen', 'q_copy', 'q_verify', 'q_skip', 'q_clear', 'q_inc', 'q_loop', 'qH']
symbols = ['0','.','5',',','#','1','B']

transitions = {}
transitions[('q_init', 'B')] = ('q_gen', '1', 'R')
# Generate "#0.5,"
transitions[('q_gen', 'B')] = ('q_copy', '#', 'R')
transitions[('q_copy', '#')] = ('q_copy', '0', 'R')
transitions[('q_copy', '0')] = ('q_copy', '.', 'R')
transitions[('q_copy', '.')] = ('q_copy', '5', 'R')
transitions[('q_copy', '5')] = ('q_copy', ',', 'R')
transitions[('q_copy', ',')] = ('q_verify', '1', 'R')   # simplified copy
# Verify
transitions[('q_verify', '1')] = ('q_skip', '1', 'R')
transitions[('q_skip', '1')] = ('q_skip', '1', 'R')
transitions[('q_skip', '#')] = ('q_clear', '#', 'R')
transitions[('q_skip', 'B')] = ('q_clear', 'B', 'R')
# Clear
for c in ['#','0','.','5',',','1']:
    transitions[('q_clear', c)] = ('q_clear', 'B', 'R')
transitions[('q_clear', 'B')] = ('q_inc', 'B', 'R')
# Increment
transitions[('q_inc', '1')] = ('q_inc', '1', 'R')
transitions[('q_inc', 'B')] = ('q_loop', '1', 'R')
# Loop
transitions[('q_loop', '1')] = ('q_gen', '1', 'R')

tm = TuringMachine(states, symbols, transitions, 'q_init', 'qH')
initial_tape = ['B', 'B']
generators, relations, W_init, W_halt = machine_to_group(tm, initial_tape)
w = tuple(W_init) + tuple(f"{g}^-1" for g in reversed(W_halt))

tester = AbelianizationTester(generators, relations)
result = tester.is_abelian_image_zero(w)
print("===== Experiment E3: Counter + variable imaginary part (copy) =====")
print(f"Generators: {len(generators)}")
print(f"Abelianization image of w == 0? {result}  => w {'=' if result else '≠'} 1")
if not result:
    print("Conclusion: Machine never halts.")
else:
    print("Warning: w vanished.")
