# CMSC 14200 Course Project

Team members:
- Ahmad Nadi (ahmadnadi) QA
- Thomas Szafir (szafir) TUI
- Hans Amemiya (amemiya) GUI
- David Wang (davwan26) BOT

Enhancement:
- GUI Background Music
- Used colored library to display nine unique colors for TUI
- Add bot player support in the GUI



Improvements:
    Game Logic: 
    - This component recieved two S's in Milestone 2
    - Fixed so pieces are placed on the board with no other consequences during 
    the first few moves of non-othello
    - Changed public to private attributes: (row, col, board)
    - Used piece_at rather than board[row][col]

    Gui:
    - This component recieved two S's in Milestone 2

    Tui:
    - This component recieved two S's in Milestone 2

    Bot:
    - This component recieved two S's in Milestone 2

    QA:
    - This component recieved two S's in Milestone 2
        - However per grader comments I added test to check if board has 
        consequences during the first few moves of non-othello 
        - Added 3+ player tests for avalible moves