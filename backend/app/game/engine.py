from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional
import random
import uuid

CREATURES = ["bat", "beetle", "cockroach", "fly", "frog", "scorpion", "spider", "toad"]
COPIES_PER_CREATURE = 8
HAND_LOSS_COUNT = 4

@dataclass
class Game:
    id: str
    status: str
    deck: list[str]
    human_hand: list[str]
    bot_hand: list[str]
    current_offer: Optional[dict]
    history: list[dict]
    winner: Optional[str] = None
    last_result: Optional[dict] = None

    def public(self):
        return {
            "id": self.id,
            "status": self.status,
            "human_hand": self.human_hand,
            "bot_hand_count": len(self.bot_hand),
            "current_offer": self.current_offer,
            "history": self.history[-20:],
            "winner": self.winner,
            "last_result": self.last_result,
        }

def new_game(seed: Optional[int] = None) -> Game:
    rng = random.Random(seed)
    deck = [c for c in CREATURES for _ in range(COPIES_PER_CREATURE)]
    rng.shuffle(deck)
    human = [deck.pop() for _ in range(5)]
    bot = [deck.pop() for _ in range(5)]
    return Game(str(uuid.uuid4()), "active", deck, human, bot, None, [])

def _check_loss(game: Game) -> Optional[str]:
    for owner, hand in (("human", game.human_hand), ("bot", game.bot_hand)):
        for creature in CREATURES:
            if hand.count(creature) >= HAND_LOSS_COUNT:
                return owner
    return None

def offer_card(game: Game, card_index: int, claim: str) -> dict:
    if game.status != "active":
        raise ValueError("Game is already finished")
    if game.current_offer is not None:
        raise ValueError("Resolve the current offer first")
    if not 0 <= card_index < len(game.human_hand):
        raise ValueError("Invalid card index")
    if claim not in CREATURES:
        raise ValueError("Unknown creature claim")
    card = game.human_hand.pop(card_index)
    game.current_offer = {"card": card, "claim": claim, "from": "human"}
    return {"type": "offer_created", "claim": claim}

def resolve_offer(game: Game, decision: str, rng: Optional[random.Random] = None) -> dict:
    if game.current_offer is None:
        raise ValueError("There is no pending offer")
    if decision not in ("accept", "challenge"):
        raise ValueError("Decision must be accept or challenge")
    rng = rng or random.Random()
    offer = game.current_offer
    actual = offer["card"]
    claim = offer["claim"]
    lied = actual != claim

    # In this simplified two-player version, the bot receives an accepted card.
    # On a challenge, the liar receives the revealed card.
    if decision == "accept":
        recipient = "bot"
        outcome = "accepted"
    else:
        recipient = "human" if lied else "bot"
        outcome = "challenge_won" if lied else "challenge_lost"

    hand = game.human_hand if recipient == "human" else game.bot_hand
    hand.append(actual)
    result = {
        "decision": decision,
        "claim": claim,
        "revealed_card": actual,
        "was_bluff": lied,
        "recipient": recipient,
        "outcome": outcome,
    }
    game.history.append(result)
    game.last_result = result
    game.current_offer = None
    loser = _check_loss(game)
    if loser:
        game.status = "completed"
        game.winner = "bot" if loser == "human" else "human"
    if len(game.deck) >= 2 and game.status == "active":
        game.human_hand.append(game.deck.pop())
        game.bot_hand.append(game.deck.pop())
    return result

def bot_decision(claim: str, bot_hand: list[str], rng: Optional[random.Random] = None) -> str:
    """Simple baseline policy; not claimed to be a learned equilibrium strategy."""
    rng = rng or random.Random()
    matching = bot_hand.count(claim)
    # Challenge more often when the bot already holds many of the claimed creature.
    challenge_probability = min(0.82, 0.22 + 0.17 * matching)
    return "challenge" if rng.random() < challenge_probability else "accept"
