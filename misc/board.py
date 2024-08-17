""" Provides a tic tac toe board. """
from exercises.claimed_square_error import ClaimedSquareError

class Board:
    """ A tic tac toe board.
    
    Attributes:
        squares (list of Player): the squares of the board, implemented
            as a list with nine values. The value of a claimed square
            will be a reference to the player who claimed that square;
            the value of an unclaimed square will be None.
    """
    def __init__(self):
        self.squares = [None] * 9
        
    def get_unclaimed_squares(self):
        """ Return indices of all unclaimed squares on the board. """
        return [n for n, sq in enumerate(self.squares) if sq is None]
    
    def is_unclaimed(self, index):
        """ Return True if square at index is unclaimed. """
        return self.squares[index] is None
    
    def claim_square(self, player, index):
        """ Claim square at index for player if square is unclaimed.
        
        Args:
            player (Player): the player attempting to claim the square.
            index (int): an index of a square. Should have a value
                between 0 and 8, inclusive.
        
        Side effects:
            Claims square at index for player.
        
        Raises:
            RuntimeError: the square in question is already
                claimed.
            ValueError: index is not an integer between 0 and 8.
        """
        if not isinstance(index, int):
            raise ValueError("index is not an int")
        if not (0 <= index <= 8):
            raise ValueError("index is not between 0 and 8")
        if self.is_unclaimed(index):
            self.squares[index] = player
        else:
            raise ClaimedSquareError(f"Square {index} is claimed")
    
    def get_winner(self):
        """ Return the winner of the game, if any.
        
        Returns:
            Player: the player who won the game, or None if there is no
            winner.
        """
        # define all groups of indices where a win is possible
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                 (0, 3, 6), (1, 4, 7), (2, 5, 8),
                 (0, 4, 8), (2, 4, 6)]
        for i1, i2, i3 in lines:
            if ((self.squares[i1] == self.squares[i2] == self.squares[i3]) and
                (self.squares[i1] is not None)):
                return self.squares[i1]
        # if we get this far, there was no winner
        return None
    
    def game_over(self):
        """ Returns True if the game is over. """
        return bool(self.get_winner() or None not in self.squares)

    def __str__(self):
        """ Return a string representation of the board. """
        strings = [str(n) if p is None else p.letter
                   for n, p in enumerate(self.squares)]
        rows = []
        for i in range(0, 9, 3):
            rows.append(" ".join(strings[i:i+3]))
        return "\n".join(rows)
