import pygame

def create_board(BOARD_SIZE, SQUARE_SIZE):
    """
    Draws the board

    Args:
        screen (pygame.Surface): The screen to draw on
        BOARD_SIZE (int): The size of the board
        SQUARE_SIZE (int): The size of each square

    Returns:
        grid (list): A list of the rectangles that make up the board

    """
    grid = []
    for i in range(BOARD_SIZE): #draw the board
        row = []
        for j in range(BOARD_SIZE):
            rect = pygame.Rect(i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE,
                               SQUARE_SIZE)
            row.append(rect)
        grid.append(row)
    return grid
            

def draw_pieces(screen, logic, SQUARE_SIZE):
    """
    Draws the pieces on the board

    Args:
        screen (pygame.Surface): The screen to draw on
        logic (Reversilogic): The logic to draw the pieces from
        SQUARE_SIZE (int): The size of each square

    Returns:
        None

    """

    radius = SQUARE_SIZE//2 - 5
    colors = ["Black", "White", "Blue", "Red", "Green", "Purple", "Orange",
               "Pink", "Brown"]
    for row_index, row in enumerate(logic.grid):
        for col_index, col in enumerate(row):
            location = logic.grid[row_index][col_index]
            if location != 0 and location is not None:
                pygame.draw.circle(screen, colors[location - 1], ((row_index *
                     SQUARE_SIZE + SQUARE_SIZE//2), (col_index*SQUARE_SIZE + 
                                                     SQUARE_SIZE//2)), radius)

def draw_possible_move(screen, logic, SQUARE_SIZE):
    """
    Draws the possible moves on the board

    Args:
        screen (pygame.Surface): The screen to draw on
        logic (Reversilogic): The logic to draw the pieces from
        SQUARE_SIZE (int): The size of each square

    Returns:
        None

    """

    radius = SQUARE_SIZE//2 - (SQUARE_SIZE//2.5)
    for location in logic.available_moves:
        row, col = location
        pygame.draw.circle(screen, "Yellow", ((row * SQUARE_SIZE +
                                                  SQUARE_SIZE//2),
                                                    (col*SQUARE_SIZE +
                                                        SQUARE_SIZE//2)),
                                                         radius)

def draw_player_turn(screen, logic):
    """
    Draws the player turn on the board
    
    Args:
        screen (pygame.Surface): The screen to draw on
        logic (Reversilogic): The logic to draw the pieces from

    Returns:
        None

    """
    turn = logic.turn
    colors = ["Black", "White", "Blue", "Red", "Green", "Purple", "Orange", 
              "Pink", "Brown"]
    pygame.draw.rect(screen, "Black", (705, 265, 90, 100), 4)
    pygame.draw.circle(screen, colors[turn - 1 ], (750, 325), 30)
    
    font = pygame.font.SysFont("Arial", 20)
    text = font.render("Turn", True, "BLACK")
    screen.blit(text, (730, 270))
    

def draw_winner(screen, logic):
    """
    Draws the winner on the board

    Args:
        screen (pygame.Surface): The screen to draw on
        logic (Reversilogic): The logic to draw the pieces from

    Returns:
        None

    """
    winner = logic.outcome
    colors = ["Black", "White", "Blue", "Red", "Green", "Purple", "Orange",
               "Pink", "Brown"]
    brown = (162,137,88)
    gray = (178, 178, 178)
    if logic.done:
        if len(winner) == 1:
            pygame.draw.rect(screen, gray, (170, 200, 435, 335))
            pygame.draw.rect(screen, brown, (170, 200, 435, 335), 9)

            pygame.draw.circle(screen, colors[winner[0] - 1], (390, 390), 50)

            font = pygame.font.SysFont("Verdana", 55) #draws the text
            text = font.render("!!WINNER!!", True, "White")
            screen.blit(text, (240, 255))
        else:
            pygame.draw.rect(screen, gray, (170, 200, 435, 335))
            pygame.draw.rect(screen, brown, (170, 200, 435, 335), 9) 

            font = pygame.font.SysFont("Verdana", 85) #draws the text
            text = font.render("TIE", True, "White")
            screen.blit(text, (310, 300))
