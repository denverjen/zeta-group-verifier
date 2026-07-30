#!/usr/bin/env python3
import sys, os
# 将项目根目录加入 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

from src.turing_machine import TuringMachine
from src.compiler import machine_to_group
from src.abelian_tester import AbelianizationTester

states = ['q0', 'q1', 'q2', 'q3', 'qH']
symbols = ['0', '.', '5', 'B']

transitions = {}
transitions[('q0', 'B')] = ('q1', '0', 'R')
transitions[('q1', 'B')] = ('q2', '.', 'R')
transitions[('q2', 'B')] = ('q3', '5', 'R')
transitions[('q3', 'B')] = ('q0', 'B', 'R')   # 无限循环

tm = TuringMachine(states, symbols, transitions, 'q0', 'qH')
initial_tape = ['B']
generators, relations, W_init, W_halt = machine_to_group(tm, initial_tape)
w = tuple(W_init) + tuple(f"{g}^-1" for g in reversed(W_halt))

tester = AbelianizationTester(generators, relations)
result = tester.is_abelian_image_zero(w)
print("===== Experiment D: Self-generating \"0.5\" loop =====")
print(f"Generators: {len(generators)}")
print(f"Abelianization image of w == 0? {result}  => w {'=' if result else '≠'} 1")
if not result:
    print("Conclusion: Machine never halts (infinite loop verified).")
else:
    print("Warning: w vanished (unexpected).")
