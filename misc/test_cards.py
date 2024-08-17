# in the line below, change cards to the name of your module

from cards import Card, Deck
import pytest


def test_card_init():
    """ Test the __init__() method of the Card class. """
    c = Card(5, "Clubs")
    for attr in ["suit", "value", "name"]:
        assert hasattr(c, attr), f"Card object should have a {attr} attribute"
    assert c.suit == "Clubs"
    assert c.value == 5
    assert c.name == "5"
    
    c2 = Card(11, "Diamonds")
    assert c2.suit == "Diamonds"
    assert c2.value == 11
    assert c2.name == "Jack"
    
    c3 = Card(12, "Hearts")
    assert c3.suit == "Hearts"
    assert c3.value == 12
    assert c3.name == "Queen"
    
    c4 = Card(13, "Spades")
    assert c4.suit == "Spades"
    assert c4.value == 13
    assert c4.name == "King"
    
    c5 = Card(14, "Clubs")
    assert c5.suit == "Clubs"
    assert c5.value == 14
    assert c5.name == "Ace"


def test_card_str():
    """ Test the __str__() method of the Card class. """
    assert hasattr(Card(2, "Spades"), "__str__"), \
        "Card object should have a __str__() method"
    assert str(Card(5, "Clubs")) == "5 of Clubs"
    assert str(Card(11, "Diamonds")) == "Jack of Diamonds"
    assert str(Card(12, "Hearts")) == "Queen of Hearts"
    assert str(Card(13, "Spades")) == "King of Spades"
    assert str(Card(14, "Clubs")) == "Ace of Clubs"


def test_deck_init():
    """ Test the __init__() method of the Deck class. """
    d = Deck()
    assert hasattr(d, "cards"), \
        "Deck object should have a cards attribute"
    assert isinstance(d.cards, list), "cards attribute should be a list"
    assert len(d.cards) == 52, "cards attribute should contain 52 cards"
    assert isinstance(d.cards[0], Card), \
        "cards attribute should be a list of Card objects"
    values1 = [(c.value, c.suit) for c in d.cards]
    assert len(set(values1)) == len(d.cards), \
        "cards attribute should not contain duplicates"
    d2 = Deck()
    values2 = [(c.value, c.suit) for c in d2.cards]
    assert values1 != values2, "cards are not shuffled"
    

def test_deck_draw():
    """ Test the draw() method of the Deck class. """
    # create a deck
    d = Deck()
    l1 = len(d.cards)
    
    # draw one card
    c = d.draw()
    assert isinstance(c, Card), "draw() did not return an instance of Card"
    assert c not in d.cards and len(d.cards) == l1 - 1, \
        "draw() did not remove the returned Card from the deck"
    
    # try to draw the other 51 cards from the deck--this shouldn't raise
    # an exception
    try:
        for i in range(51):
            d.draw()
    except RuntimeError:
        pytest.fail("premature RuntimeError: deck ran out of cards too early")
        
    # now the deck should be empty; the next call to draw() should raise
    # a RuntimeError
    with pytest.raises(RuntimeError):
        d.draw()
