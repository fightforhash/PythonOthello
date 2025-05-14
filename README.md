# Othello Game Project

<p align="center">
  <img src="othello.ico" alt="Othello Game Icon" width="120" height="120">
</p>

## 🎮 Alpha-Beta Pruning AI

**This project implements an optimized AI using the advanced Alpha-Beta Pruning algorithm.**

Alpha-Beta Pruning is an improved version of the minimax algorithm used to find optimal moves in zero-sum games like chess and Othello, enhancing efficiency by eliminating unnecessary search paths.

```python
def alpha_beta_search(self, board, player, max_depth, alpha=-float('inf'), beta=float('inf')):
    # Termination condition: maximum depth reached or game over
    if max_depth == 0 or is_game_over(board):
        return eval_board(board, player), None

    # MAX player (Black)
    if player == BLACK:
        max_eval, best_move = -float('inf'), None
        for move in get_legal_moves(board, player):
            new_board = make_move(copy.deepcopy(board), move, player)
            eval = self.alpha_beta_search(new_board, WHITE, max_depth - 1, alpha, beta)[0]
            if eval > max_eval:
                max_eval, best_move = eval, move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Pruning
        return max_eval, best_move
    # MIN player (White)
    else:
        min_eval, best_move = float('inf'), None
        for move in get_legal_moves(board, player):
            new_board = make_move(copy.deepcopy(board), move, player)
            eval = self.alpha_beta_search(new_board, BLACK, max_depth - 1, alpha, beta)[0]
            if eval < min_eval:
                min_eval, best_move = eval, move
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Pruning
        return min_eval, best_move
```

## 📋 Project Overview

An Othello game application featuring a modern interface and AI opponents with various difficulty levels.

- **Game Modes**: User vs. User, User vs. AI
- **AI Difficulty Levels**: Easy, Medium, Hard, Expert (depths: 2, 4, 6, 8)
- **Hint System**: Feature that recommends optimal moves
- **User Statistics**: Records game results and win rates

## 🚀 Key Features

- **Intuitive GUI**: Tkinter-based graphical interface
- **Current Player Display**: Shows whose turn it is (Black/White)
- **Move Highlighting**: Displays possible positions for the current player
- **Game Statistics Storage**: MySQL database integration
- **User Authentication**: Login and registration functionality
- **Surrender and Hint Features**: Options to give up or request assistance at any time

## 💻 Technology Stack

- **Language**: Python
- **GUI**: Tkinter
- **Database**: MySQL
- **AI Algorithm**: Alpha-Beta Pruning

## 🔧 Installation and Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Install required packages:
   ```
   pip install mysql-connector-python tkinter
   ```

3. MySQL Database Setup:
   - **Important**: You must download and install MySQL Workbench to manage the SQL file locally. The game will not run without setting up the database properly.
   - Open MySQL Workbench and connect to your local MySQL server
   - Run the SQL commands from `othello_revised.sql` to create the necessary database and tables
   - Configure the database connection in `database.py` with your MySQL credentials

4. Run the game:
   ```
   python GUI_Execute_to_Play.py
   ```

## 📁 Project Structure

- **AI.py**: Alpha-Beta Pruning algorithm implementation
- **backend.py**: Game logic and rule handling
- **constants.py**: Game constant definitions
- **database.py**: Database connection and statistics management
- **GUI_Execute_to_Play.py**: Graphical interface and main execution file
- **othello_revised.sql**: Database schema

## 👨‍💻 Developer Information

NingYuan Sun<br>
Thomas Ha<br>
Yonghee Han<br>
Ethan Mckellips<br>
Osase-Noma Owens<br>
-> classmates from the FA23 CS506 course in University of Wisconsin - Madison.

## 📜 License

MIT License

Copyright (c) 2023 NingYuan Sun, Thomas Ha, Yonghee Han, Ethan Mckellips, Osase-Noma Owens

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the “Software”), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.
