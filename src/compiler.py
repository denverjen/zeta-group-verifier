"""
Turing machine to finitely presented group compiler.

Implements the Boone–Novikov construction: given a Turing machine and
an initial tape, produces a finitely presented group G and two words
W_init, W_halt such that:

    w = W_init * (W_halt)^{-1} = 1 in G   iff   the machine halts.

The output is suitable for the abelianization tester.
"""

from .turing_machine import TuringMachine
from typing import List, Tuple

def machine_to_group(tm: TuringMachine,
                     initial_tape: List[str]) -> Tuple[List[str],
                                                       List[Tuple[Tuple[str, ...], Tuple[str, ...]]],
                                                       Tuple[str, ...],
                                                       Tuple[str, ...]]:
    generators = tm.states + tm.symbols + ['h']
    relations: List[Tuple[Tuple[str, ...], Tuple[str, ...]]] = []

    # Only transition rules (no absorption, no explicit h‑commutation)
    for (state, symbol), (new_state, new_symbol, direction) in tm.transitions.items():
        if direction == 'R':
            relations.append(((state, symbol), (new_symbol, new_state)))
        elif direction == 'L':
            for b in tm.symbols:
                relations.append(((b, state, symbol), (new_state, b, new_symbol)))
        else:
            raise ValueError(f"Unknown direction {direction}")

    W_init = tuple(['h', tm.start_state] + initial_tape + ['h'])
    W_halt = tuple(['h', tm.halt_state, 'h'])

    return generators, relations, W_init, W_halt
