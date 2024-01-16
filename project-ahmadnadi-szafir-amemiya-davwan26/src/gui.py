import pygame
from pygame import mixer
import click
from reversi import Reversi
from sys import exit
from gui_helpers import *
from bot import use_bot, random_bot, greedy_bot, two_move_search_bot


@click.command()
@click.option("-n", "--num-players", default = 2, help="Number of players")
@click.option('-s', "--board-size", default = 8, help='Board size')
@click.option('--othello/--non-othello', default=True, help='Othello mode')
@click.option("--bot", default=None, help="Bot to play against")
def main(num_players, board_size, othello, bot) -> None:
    """
    Runs the game
    """
    BACKGROUND_GREEN = (59,133,76)
    BOARD_SIZE = board_size
    NUM_PLAYERS = num_players
    ORTHELLO_STATE = othello
    clock = pygame.time.Clock()

    bots = {"random": random_bot, \
        "smart": greedy_bot, \
        "very-smart": two_move_search_bot}
    
    pygame.init()
    screen = pygame.display.set_mode((800, 700))
    screen.fill(BACKGROUND_GREEN)
    pygame.display.set_caption("Reversi")
    clock = pygame.time.Clock()

    mixer.music.load("src/background.mp3") # loads the background music
    mixer.music.play(-1)

    if NUM_PLAYERS < 2 or NUM_PLAYERS > 9:
        raise ValueError("Number of players must be between 2 and 9")
    if BOARD_SIZE < 4 or BOARD_SIZE > 20:
        raise ValueError("Board size must be between 4 and 20")
    
    SQUARE_SIZE = 700 // BOARD_SIZE

    logic = Reversi(BOARD_SIZE, NUM_PLAYERS, ORTHELLO_STATE)
    delay = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if the user presses quit 
                pygame.quit()
                exit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for row in range(BOARD_SIZE):
                    for col in range(BOARD_SIZE):
                        if (grid[row][col].collidepoint(mouse_pos) and
                            (row, col) in logic.available_moves):
                            if not logic.done:
                                logic.apply_move((row, col))

        screen.fill(BACKGROUND_GREEN) #clear the screen

        grid: list
        grid = create_board(BOARD_SIZE, SQUARE_SIZE) # creates the board
        for c_row in grid:
            for rect in c_row:
                pygame.draw.rect(screen, "Black", rect, 1)

        if logic.turn == 2 and bot is not None and not logic.done:
            if delay % 24 == 0: # delays the bot move
                use_bot(logic, bots[bot])
            delay += 1

        draw_pieces(screen, logic, SQUARE_SIZE) # draws the pieces

        draw_possible_move(screen, logic, SQUARE_SIZE) # draws the possible move

        pygame.draw.rect(screen, "Black", (0, 0, 700, 700), 5) #draws the border

        draw_player_turn(screen, logic) # draws the player turn

        draw_winner(screen, logic) # draws the winner

        pygame.display.update()
        clock.tick(24)


if __name__ == "__main__":
    main()
