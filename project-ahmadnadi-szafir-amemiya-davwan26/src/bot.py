"""
Bot implementation for reversi
"""
import random
import sys
import click
from reversi import Reversi
from typing import Callable


def use_bot(game: Reversi, bot: Callable[[Reversi], None]) -> None:
    """
    Chooses a move in the game of reversi according to the strategy implemented
    in bot.

    Input: 
        game (Reversi): gameboard
        bot (Callable): the strategy being used, as implemented in the bot.
    """
    bot(game)


def random_bot(game: Reversi) -> None:
    """
    Implements a random game playing strategy. Bot randomly selects a position
    from the list of available positions and places a piece at that location.

    Input:
        game (Reversi): gameboard
    """
    avbl_pos = game.available_moves
    pos = avbl_pos[random.randint(0, len(avbl_pos) - 1)]

    game.apply_move(pos)


def greedy_bot(game: Reversi) -> None:
    """
    Implements a greedy game playing strategy. Bot chooses the position from the
    list of available positions which maximizes the number of pieces it has
    immediately after playing that move.

    Input:
        game (Reversi): gameboard
    """

    def num_pieces(game: Reversi, player: int) -> int:
        """
        Counts the number of pieces of a given player on the gameboard.

        Input:
            game (Reversi): gameboard
            turn (int): the player whose pieces are being counted
        """
        num = 0
        for row in game.grid:
            for piece in row:
                if piece == player:
                    num += 1
 
        return num

    player = game.turn

    avbl_moves = game.available_moves
    best_move = avbl_moves[0]
    max_n = 0

    for move in avbl_moves:
        simulation = game.simulate_moves([move])
        n = num_pieces(simulation, player)

        if n > max_n:
            max_n = n
            best_move = move

    game.apply_move(best_move)


def two_move_search_bot(game: Reversi) -> None:
    """
    Implements a game-playing strategy which seeks to maximize the average 
    number of pieces that a player has on the board after the next player 
    plays a move, assuming each move occurs with an equal probability. Override
    if playing a given move results in the player winning the game: the bot
    will choose the winning move instead.
    """
    current_player = game.turn
    current_moves = game.available_moves
    best_move = current_moves[0]
    best_score = 0.

    for pos_move in current_moves:
        depth1_simulation = game.simulate_moves([pos_move])
        next_moves = depth1_simulation.available_moves

        if len(next_moves) == 0:
            best_move = pos_move
            break

        pieces = 0
        for move in next_moves:
            depth2_simulation = depth1_simulation.simulate_moves([move])
            pieces += depth2_simulation.num_pieces(current_player)

        avg_pieces = pieces / len(next_moves)

        if avg_pieces > best_score:
            best_score = avg_pieces
            best_move = pos_move

    game.apply_move(best_move)


@click.command()
@click.option("-n", "--num-games", default = 100, help = "Number of games")
@click.option("-1", "--player1", default = "random", help = "Bot of player 1")
@click.option("-2", "--player2", default = "random", help = "Bot of player 2")
def main(num_games, player1, player2) -> None:
    NUM_GAMES = num_games # Tracks the number of games being played
    PLAYER_1 = player1
    PLAYER_2 = player2

    bot = {"random": random_bot,\
           "smart": greedy_bot,\
           "very-smart": two_move_search_bot}

    p1_wins = 0 # Number of times player 1 wins
    p2_wins = 0 # Number of times player 2 wins
    ties = 0 # Number of ties

    for _ in range(NUM_GAMES):
        game = Reversi(side=8, players=2, othello=True)
        while not game.done:
            if game.turn == 1:
                use_bot(game, bot[PLAYER_1])
            else:
                use_bot(game, bot[PLAYER_2])
   
        if game.outcome == [1, 2]:
            ties += 1
        if game.outcome == [1]:
            p1_wins += 1
        if game.outcome == [2]:
            p2_wins += 1

    ### Print number of wins for each player, and number of draws
    print(f"Player 1 wins: {p1_wins / NUM_GAMES * 100:.2f}%\n \
            Player 2 wins: {p2_wins / NUM_GAMES * 100:.2f}%\n \
            Ties: {ties / NUM_GAMES * 100:.2f}%")


if __name__ == "__main__":
    main()
