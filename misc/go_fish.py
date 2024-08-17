from homeworkdmiller import Deck
import random
from time import sleep

LONG_PAUSE = 1.0
SHORT_PAUSE = 0.2

class Player:
    """ A Go Fish player.
    
    This class works for both human and computer players.
    
    Attributes:
        hand (dict of str: list of cards.Card): the player's hand. Each
            key is a card name; each value is a list of cards.
        books (list of str): the books (sets) made by the player. Each
            value is a card name. At the end of the game, the player
            with the most books wins.
        seen (set of str): cards previously requested by the player's
            opponent. Used by computer player.
        is_human (bool): True if the player is human, otherwise False.
    """
    def __init__(self, is_human=True):
        """ Initialize the player's attributes. """
        self.hand = dict()
        self.books = list()
        self.seen = set()
        self.is_human = is_human
        
    def get_cards(self, cards):
        """ Receive cards from the dealer or from another player. For
        human players, print the new cards.
        
        Side effects:
            Writes to stdout.
            Modifies self.hand.
        """
        if self.is_human:
            print("You received the following cards:")
            print(", ".join(str(card) for card in cards))
            sleep(LONG_PAUSE)
            print()
        for card in cards:
            if card.name not in self.hand:
                self.hand[card.name] = list()
            self.hand[card.name].append(card)
            if len(self.hand[card.name]) == 4:
                self.make_book(card.name)
    
    def make_book(self, cardname):
        """ Remove a book from the player's hand and store it in their
        list of books.

        Args:
            cardname (str): the card name for which the player has a
                book.
        
        Side effects:
            Writes to stdout.
            Modifies self.books and self.hand.
        """
        self.books.append(cardname)
        del self.hand[cardname]
        
        who = "You" if self.is_human else "The computer"
        verb = "have" if self.is_human else "has"
        punct = "!" if self.is_human else "."
        pl = "" if len(self.books) == 1 else "s"
        print(f"{who} made a book of {cardname}s{punct}")
        print(f"{who} now {verb} {len(self.books)} book{pl}{punct}")
        sleep(LONG_PAUSE)
        print()
    
    def lose_cards(self, cardname):
        """ Remove cards from a player's hand because their opponent has
        requested them.
        
        Args:
            cardname (str): the card name to be removed from the
                player's hand.
        
        Returns:
            list of cards.Card: the cards the opponent asked for, if the
            player has them; otherwise, returns None.
        
        Side effects:
            Writes to stdout.
            Modifies self.seen and self.hand.
        """
        self.seen.add(cardname)
        if cardname in self.hand:
            if self.is_human:
                print(f"You've lost your {cardname}s.")
                sleep(LONG_PAUSE)
                print()
            return self.hand.pop(cardname)
        else:
            if self.is_human:
                print(f"The computer asked for your {cardname}s, but"
                      " you don't have any.")
                sleep(LONG_PAUSE)
                print()
            return None
    
    def take_turn(self):
        """ Take a turn.
        
        Returns:
            str: the card name the player is asking for.
        
        Side effects:
            Modifies self.seen.
        """
        if self.is_human:
            while True:
                print("You have")
                for cardname in sorted(self.hand, key=lambda x:
                                                  self.hand[x][0].value):
                    cards = self.hand[cardname]
                    pl = "" if len(cards) == 1 else "s"
                    print(f"{len(cards)} card{pl} of value {cardname}")
                    sleep(SHORT_PAUSE)
                cardname = input("What card do you want to ask for? ")
                print()
                cardname = cardname.capitalize().strip().rstrip("s")
                if cardname not in self.hand:
                    print("Sorry, you can only ask for cards you have.")
                    sleep(LONG_PAUSE)
                    print()
                else:
                    break
        else:
            seen = self.seen & set(self.hand)
            if seen and random.random() > 0.8:
                cardname = seen.pop()
            else:
                cardname = random.choice(list(self.hand))
        self.seen.discard(cardname)
        return cardname
    
    def go_fish(self):
        """ Prints "Go fish" if the user is human. """
        if self.is_human:
            print("Go fish...")
            sleep(LONG_PAUSE)
            
    def win(self):
        """ Tells the human player they won. """
        if self.is_human:
            print("You won! Congratulations!")
    
    def lose(self):
        """ Tells the human player they lost. """
        if self.is_human:
            print("You lost. Better luck next time.")
            
    def tie(self):
        """ Tells the human player they tied. """
        if self.is_human:
            print("You and the computer tied!")

def main():
    """ Set up and play a game of Go Fish.
    
    Side effects:
        Writes to stdout.
        Asks user for input.
    """
    deck = Deck()
    human = Player()
    computer = Player(is_human=False)
    players = [human, computer]
    random.shuffle(players)
    for player in players:
        cards = [deck.draw() for i in range(7)]
        player.get_cards(cards)
    player, opponent = players
    
    while True:
        if len(player.hand) == 0:
            try:
                card = deck.draw()
                player.get_cards([card])
            except RuntimeError:
                break
        cardname = player.take_turn()
        cards = opponent.lose_cards(cardname)
        if cards is None:
            player.go_fish()
            try:
                card = deck.draw()
                player.get_cards([card])
            except RuntimeError:
                break
            opponent, player = player, opponent
        else:
            player.get_cards(cards)
    
    print(f"Final score: human: {len(human.books)}"
          f" computer: {len(computer.books)}")
    if len(human.books) > len(computer.books):
        human.win()
    elif len(human.books) == len(computer.books):
        human.tie()
    else:
        human.lose()

if __name__ == "__main__":
    main()
