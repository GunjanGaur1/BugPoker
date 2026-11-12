from app.game.engine import new_game, offer_card, resolve_offer, CREATURES

def test_new_game_has_five_cards_each():
    game = new_game(seed=1)
    assert len(game.human_hand) == 5
    assert len(game.bot_hand) == 5
    assert game.status == "active"

def test_offer_requires_valid_card_and_claim():
    game = new_game(seed=2)
    offer_card(game, 0, CREATURES[0])
    assert game.current_offer["claim"] == CREATURES[0]

def test_resolve_offer_reveals_and_clears_offer():
    game = new_game(seed=3)
    offer_card(game, 0, CREATURES[0])
    result = resolve_offer(game, "accept")
    assert result["decision"] == "accept"
    assert result["revealed_card"] in CREATURES
    assert game.current_offer is None

def test_invalid_offer_index():
    game = new_game(seed=4)
    try:
        offer_card(game, 99, CREATURES[0])
        assert False
    except ValueError:
        assert True
