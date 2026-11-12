"""Vanilla CFR for Kuhn Poker (3-card toy imperfect-information game).

This is an independent algorithm demonstration. It is not a Cockroach Poker solver.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List
import random

CARDS = (1, 2, 3)  # J, Q, K
ACTIONS = ("p", "b")  # pass/check, bet/call abstraction handled by history

@dataclass
class Node:
    regret_sum: List[float] = field(default_factory=lambda: [0.0, 0.0])
    strategy_sum: List[float] = field(default_factory=lambda: [0.0, 0.0])

    def strategy(self, reach: float) -> List[float]:
        positive = [max(0.0, x) for x in self.regret_sum]
        total = sum(positive)
        strat = [x / total for x in positive] if total > 0 else [0.5, 0.5]
        for i in range(2):
            self.strategy_sum[i] += reach * strat[i]
        return strat

    def average_strategy(self) -> List[float]:
        total = sum(self.strategy_sum)
        return [x / total for x in self.strategy_sum] if total > 0 else [0.5, 0.5]

class KuhnCFR:
    def __init__(self, seed: int = 7):
        self.nodes: Dict[str, Node] = {}
        self.rng = random.Random(seed)

    def _cfr(self, cards, history: str, p0: float, p1: float) -> float:
        plays = len(history)
        player = plays % 2
        opponent = 1 - player

        # Terminal histories: pp, bp, bb, pbp, pbb
        if history.endswith("pp"):
            return 1.0 if cards[player] > cards[opponent] else -1.0
        if history.endswith("bp"):
            return 1.0
        if history.endswith("bb"):
            return 2.0 if cards[player] > cards[opponent] else -2.0
        if history.endswith("pbp"):
            return -1.0
        if history.endswith("pbb"):
            return 2.0 if cards[player] > cards[opponent] else -2.0

        info = f"{cards[player]}:{history}"
        node = self.nodes.setdefault(info, Node())
        strategy = node.strategy(p0 if player == 0 else p1)
        util = [0.0, 0.0]
        node_util = 0.0
        for a, action in enumerate(ACTIONS):
            next_history = history + action
            if player == 0:
                util[a] = -self._cfr(cards, next_history, p0 * strategy[a], p1)
            else:
                util[a] = -self._cfr(cards, next_history, p0, p1 * strategy[a])
            node_util += strategy[a] * util[a]
        for a in range(2):
            regret = util[a] - node_util
            node.regret_sum[a] += (p1 if player == 0 else p0) * regret
        return node_util

    def train(self, iterations: int = 100_000) -> dict:
        for _ in range(iterations):
            cards = list(CARDS)
            self.rng.shuffle(cards)
            self._cfr(cards, "", 1.0, 1.0)
        return self.export()

    def export(self) -> dict:
        return {key: node.average_strategy() for key, node in sorted(self.nodes.items())}
