"""
Turing machine simulator.

Provides a simple deterministic Turing machine with a single tape.
Used as input to the compiler that translates the machine into a
finitely presented group (Boone–Novikov construction).

The tape is represented as a list of symbols, with a special blank
symbol 'B' that may appear anywhere on the tape.
"""

from typing import Dict, List, Tuple, Optional

# Type alias for transition table
Transition = Tuple[str, str, str]   # (new_state, new_symbol, direction)
TransitionTable = Dict[Tuple[str, str], Transition]


class TuringMachine:
    """
    A deterministic Turing machine with one tape.

    Parameters
    ----------
    states : list of str
        All state names.
    symbols : list of str
        Tape alphabet (should include the blank symbol 'B').
    transitions : dict
        Keys are (state, symbol); values are (new_state, new_symbol, direction).
        direction must be 'L' or 'R'.
    start_state : str
        Initial state.
    halt_state : str
        Halting state. The machine stops when it enters this state.
    """

    def __init__(self,
                 states: List[str],
                 symbols: List[str],
                 transitions: TransitionTable,
                 start_state: str,
                 halt_state: str):
        self.states = states
        self.symbols = symbols
        self.transitions = transitions
        self.start_state = start_state
        self.halt_state = halt_state

        # Quick validation
        if start_state not in states:
            raise ValueError("start_state must be in states")
        if halt_state not in states:
            raise ValueError("halt_state must be in states")

    def step(self,
             tape: List[str],
             head: int,
             state: str) -> Tuple[List[str], int, Optional[str]]:
        """
        Execute one step of the machine.

        Parameters
        ----------
        tape : list of str
            Current tape contents.
        head : int
            Current head position (index into tape).
        state : str
            Current state.

        Returns
        -------
        (tape, head, new_state) : tuple
            Updated tape, head position, and new state.
            If the new state is the halt_state, returns None as state
            to indicate halting.
        """
        if state == self.halt_state:
            return tape, head, None

        symbol = tape[head]
        key = (state, symbol)
        if key not in self.transitions:
            raise ValueError(f"No transition defined for state={state}, symbol={symbol}")

        new_state, new_symbol, direction = self.transitions[key]
        tape[head] = new_symbol
        if direction == 'R':
            head += 1
        elif direction == 'L':
            head -= 1
        else:
            raise ValueError(f"Direction must be 'L' or 'R', got {direction}")

        # Extend tape if head goes out of bounds (assume blank)
        if head < 0:
            tape.insert(0, 'B')
            head = 0
        elif head >= len(tape):
            tape.append('B')

        if new_state == self.halt_state:
            return tape, head, None
        return tape, head, new_state

    def run(self,
            initial_tape: List[str],
            max_steps: int = 1000000) -> Tuple[List[str], int, Optional[str], int]:
        """
        Run the machine until it halts or max_steps is reached.

        Returns
        -------
        (tape, head, state, steps) : tuple
            Final tape, head position, state (None if halted), and number of steps taken.
        """
        tape = initial_tape[:]
        head = 0
        state = self.start_state
        steps = 0
        while state is not None and steps < max_steps:
            tape, head, state = self.step(tape, head, state)
            steps += 1
        return tape, head, state, steps


# ---------------------------------------------------------------------------
# Self-test with a simple machine: binary increment
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # A simple machine that writes a '1' and halts.
    states = ['q0', 'qH']
    symbols = ['0', '1', 'B']
    trans = {
        ('q0', 'B'): ('qH', '1', 'R'),
    }
    tm = TuringMachine(states, symbols, trans, 'q0', 'qH')
    tape = ['B', 'B', 'B']
    final_tape, head, state, steps = tm.run(tape)
    print("Tape:", final_tape)
    print("Head:", head)
    print("State:", state)
    print("Steps:", steps)
    assert state is None
    assert final_tape[0] == '1'
    print("Self-test passed.")
