"""
Contains the piece class that is used in the reversi implementation.
"""
class Piece:
    """
    Class to represent a piece.

    Attributes:
        player (str): the string representation of who the player is
        
    Methods:
        get_player: gets a pieces player
        set_player: sets a pieces player to another player
    """
    player: str

    def __init__(self, player):
        self.player = player

    def get_player(self):
        """
        Gets a pieces player
        """
        return self.player
    
    def set_player(self, new_player: str):
        """
        Sets a pieces player to another player
        """
        self.player = new_player
    
    def __str__(self):
        """ 
        Returns string representation of a piece
        """
        return "Player: "+ self.player
    