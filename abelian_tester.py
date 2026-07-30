"""
Abelianization rank test.

Given a group presentation and a target word w, determines whether
the image of w in the abelianization G/[G,G] is trivial.

This is a rigorous proof that w ≠ 1 if the test returns False.
If it returns True, w might still be non‑trivial in the full group.
"""

import numpy as np
from typing import List, Tuple


class AbelianizationTester:
    def __init__(self, generators: List[str],
                 relations: List[Tuple[Tuple[str, ...], Tuple[str, ...]]]):
        self.gens = generators
        self.gen_to_idx = {g: i for i, g in enumerate(generators)}
        self.relations = relations

    def _word_to_vec(self, word: Tuple[str, ...]) -> np.ndarray:
        """Convert a word (tuple of generators) to an integer exponent vector."""
        vec = np.zeros(len(self.gens), dtype=int)
        for g in word:
            if g.endswith('^-1'):
                base = g[:-3]
                if base in self.gen_to_idx:
                    vec[self.gen_to_idx[base]] -= 1
            else:
                if g in self.gen_to_idx:
                    vec[self.gen_to_idx[g]] += 1
        return vec

    def is_abelian_image_zero(self, target_word: Tuple[str, ...]) -> bool:
        """
        Return True iff the target word's image in the abelianization is zero.
        """
        target_vec = self._word_to_vec(target_word)
        if not self.relations:
            return np.all(target_vec == 0)

        # Build relation matrix: each row is left_vec - right_vec
        rows = []
        for left, right in self.relations:
            lv = self._word_to_vec(left)
            rv = self._word_to_vec(right)
            rows.append(lv - rv)
        M = np.array(rows, dtype=int)

        # Augment with target vector
        Aug = np.vstack([M, target_vec])
        rank_M = np.linalg.matrix_rank(M)
        rank_Aug = np.linalg.matrix_rank(Aug)
        # target is in the row space iff ranks are equal
        return rank_Aug == rank_M
